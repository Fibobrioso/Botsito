"""Feedback solo-anadir en el historial de git y trazabilidad de los cambios de spec/casos (F09)."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from botsito.comun.historial import (
    ANCLA_FUENTE,
    DIRECTORIO_FEEDBACK,
    ancla_desviada,
    commits_sin_fuente,
    fuentes_de_mensaje,
    hay_git,
    historial_evaluable,
    modificaciones_en_historial,
    modificaciones_preparadas,
    resolver,
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
    problemas = commits_sin_fuente(repo, None, ids_validos={"ev-v4-001533-1a2b3c4d", "ADR-0002"})
    assert len(problemas or []) == 1 and "sin trailer" in (problemas or [""])[0]
    # Un ADR que no existe no es una fuente, aunque tenga formato de ADR.
    solo_ev = commits_sin_fuente(repo, None, ids_validos={"ev-v4-001533-1a2b3c4d"}) or []
    assert any("fuente inexistente ADR-0002" in p for p in solo_ev)
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
    # Un mensaje con mayuscula acentuada (bytes fuera de cp1252) no anula la comprobacion.
    spec.write_text("reglas: [3]\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "\u00cdNDICE de la spec, sin Fuente \u00c1vila")
    ultimos = [p for p in commits_sin_fuente(repo, None) or [] if _head(repo) in p]
    assert ultimos == [f"{_head(repo)}: toca spec/cases sin trailer 'Fuente:'"]


def test_fuentes_de_mensaje() -> None:
    assert fuentes_de_mensaje("x\n\nFuente: a, b c\nFuente: d") == ["a", "b", "c", "d"]
    assert fuentes_de_mensaje("sin trailer") == []
    # El asunto no es un trailer.
    assert fuentes_de_mensaje("Fuente: ADR-0001") == []
    assert fuentes_de_mensaje("Fuente: ADR-0001\n\nFuente: ADR-0002") == ["ADR-0002"]


@pytest.mark.contract
def test_digitos_unicode_no_son_fuente(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    spec = repo / "knowledge" / "spec" / "s.yaml"
    spec.parent.mkdir(parents=True)
    spec.write_text("a: 1\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "x\n\nFuente: ADR-\u0660\u0660\u0660\u0661")
    problemas = commits_sin_fuente(repo, None, ids_validos={"ADR-0001"}) or []
    assert any("formato invalido" in p for p in problemas)


@pytest.mark.contract
def test_tag_movido_se_detecta(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    sha = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, encoding="utf-8", check=True
    ).stdout.strip()
    assert ancla_desviada(repo, "stable/F06", sha) is None  # sin tag: nada que comprobar
    _git(repo, "tag", "stable/F06")
    assert ancla_desviada(repo, "stable/F06", sha) is None
    (repo / "x.txt").write_text("x", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "otro")
    _git(repo, "tag", "-f", "stable/F06")
    desviado = ancla_desviada(repo, "stable/F06", sha)
    assert desviado is not None and "alguien lo movio" in desviado


@pytest.mark.contract
def test_clon_superficial_no_es_evaluable(tmp_path: Path) -> None:
    (tmp_path / "origen").mkdir()
    origen = _repo(tmp_path / "origen")
    (origen / FB).write_text("id: y\n", encoding="utf-8")  # edicion commiteada en el origen
    _git(origen, "commit", "-q", "-am", "edit")
    (origen / "k.txt").write_text("k", encoding="utf-8")
    _git(origen, "add", "-A")
    _git(origen, "commit", "-q", "-m", "otro")
    assert modificaciones_en_historial(origen, DIRECTORIO_FEEDBACK)
    clon = tmp_path / "clon"
    subprocess.run(
        ["git", "clone", "-q", "--depth", "1", f"file://{origen.as_posix()}", str(clon)],
        check=True,
        capture_output=True,
    )
    motivo = historial_evaluable(clon)
    assert motivo is not None and "superficial" in motivo
    # "No evaluable" y no "sin violaciones": el clon superficial no ve la edicion.
    assert modificaciones_en_historial(clon, DIRECTORIO_FEEDBACK) is None
    assert commits_sin_fuente(clon, None) is None


@pytest.mark.contract
def test_proyecto_anidado_en_otro_repo_no_es_evaluable(tmp_path: Path) -> None:
    exterior = _repo(tmp_path)
    interior = exterior / "proyecto"
    (interior / FB).parent.mkdir(parents=True)
    (interior / FB).write_text("id: x\n", encoding="utf-8")
    _git(exterior, "add", "-A")
    _git(exterior, "commit", "-q", "-m", "anidado")
    motivo = historial_evaluable(interior)
    assert motivo is not None and "no es la raiz" in motivo
    assert modificaciones_en_historial(interior, DIRECTORIO_FEEDBACK) is None
    assert historial_evaluable(exterior) is None


@pytest.mark.contract
def test_repositorio_real(repo: Path) -> None:
    v = modificaciones_en_historial(repo, DIRECTORIO_FEEDBACK)
    if v is None:
        assert not hay_git(repo), "hay git pero la guardia no se pudo evaluar"
        pytest.skip("sin git")
    assert v == []
    ancla = resolver(repo, *ANCLA_FUENTE)
    assert ancla is not None, "ni el tag stable/F06 ni su SHA existen: clon superficial o sin tags"
    sin_fuente = commits_sin_fuente(repo, ancla)
    assert sin_fuente is not None, "la comprobacion de trailers no se pudo evaluar"
    assert sin_fuente == [], "\n".join(sin_fuente)


def _primero(repo: Path, ruta: str) -> str:
    out = subprocess.run(
        ["git", "log", "--format=%H", "--diff-filter=A", "--", ruta],
        cwd=repo,
        capture_output=True,
        encoding="utf-8",
        check=True,
    ).stdout.split()
    return out[-1][:7]


def _head(repo: Path) -> str:
    return subprocess.run(
        ["git", "rev-parse", "--short=7", "HEAD"],
        cwd=repo,
        capture_output=True,
        encoding="utf-8",
        check=True,
    ).stdout.strip()
