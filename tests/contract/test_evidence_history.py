"""La evidencia es inmutable en el historial de git (F06, seccion H).

Los hooks se saltan con --no-verify; este test no. Se ejecuta sobre repositorios temporales
(modificar, borrar, renombrar, editar dentro de un merge, editar sin commitear) y sobre el real.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from botsito.comun.historial import (
    hay_git,
    modificaciones_en_historial,
    modificaciones_preparadas,
)

EV = "knowledge/evidence/v1/ev-v1-000001-aaaaaaaa.yaml"


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def _repo(tmp_path: Path) -> Path:
    _git(tmp_path, "init", "-q", "-b", "main")
    _git(tmp_path, "config", "user.email", "t@t")
    _git(tmp_path, "config", "user.name", "t")
    _git(tmp_path, "config", "core.autocrlf", "false")
    (tmp_path / "knowledge" / "evidence" / "v1").mkdir(parents=True)
    (tmp_path / EV).write_text("id: x\n", encoding="utf-8")
    (tmp_path / "knowledge" / "evidence" / "_contradicciones.yaml").write_text(
        "c\n", encoding="utf-8"
    )
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "add")
    return tmp_path


@pytest.mark.contract
def test_anadir_y_regenerar_son_legitimos(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    assert modificaciones_en_historial(repo) == []
    (repo / "knowledge" / "evidence" / "_contradicciones.yaml").write_text("d\n", encoding="utf-8")
    _git(repo, "add", "-A")
    assert modificaciones_preparadas(repo) == []
    _git(repo, "commit", "-q", "-m", "regen")
    assert modificaciones_en_historial(repo) == []


@pytest.mark.contract
def test_modificar_se_detecta_en_indice_e_historial(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    (repo / EV).write_text("id: y\n", encoding="utf-8")
    assert modificaciones_en_historial(repo) == [f"modificado en el arbol de trabajo: {EV}"]
    _git(repo, "add", "-A")
    assert any(v.startswith("indice: M") for v in modificaciones_preparadas(repo) or [])
    _git(repo, "commit", "-q", "-m", "edit")
    assert modificaciones_en_historial(repo) == [f"modificado desde {_primero(repo)}: {EV}"]


@pytest.mark.contract
def test_borrar_y_renombrar_se_detectan(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    _git(repo, "mv", EV, EV.replace("aaaaaaaa", "bbbbbbbb"))
    _git(repo, "commit", "-q", "-m", "ren")
    assert modificaciones_en_historial(repo) == [f"borrado o renombrado: {EV}"]
    _git(repo, "rm", "-q", EV.replace("aaaaaaaa", "bbbbbbbb"))
    _git(repo, "commit", "-q", "-m", "del")
    violaciones = modificaciones_en_historial(repo) or []
    assert len(violaciones) == 2 and all(v.startswith("borrado") for v in violaciones)


@pytest.mark.contract
def test_edicion_escondida_en_un_merge_se_detecta(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    _git(repo, "checkout", "-q", "-b", "feature/y")
    (repo / "o.txt").write_text("o\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "otro")
    _git(repo, "checkout", "-q", "main")
    (repo / "m.txt").write_text("m\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "m")
    subprocess.run(["git", "merge", "--no-commit", "feature/y"], cwd=repo, capture_output=True)
    (repo / EV).write_text("id: EDITADO\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "merge con edicion")
    violaciones = modificaciones_en_historial(repo) or []
    assert violaciones and violaciones[0].startswith("modificado desde")


@pytest.mark.contract
def test_adicion_escondida_en_un_merge_queda_protegida(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    _git(repo, "checkout", "-q", "-b", "feature/z")
    (repo / "o.txt").write_text("o\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "otro")
    _git(repo, "checkout", "-q", "main")
    (repo / "m.txt").write_text("m\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "m")
    subprocess.run(["git", "merge", "--no-commit", "feature/z"], cwd=repo, capture_output=True)
    nuevo = EV.replace("aaaaaaaa", "cccccccc")
    (repo / nuevo).write_text("id: nuevo\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "merge con adicion")
    assert modificaciones_en_historial(repo) == []
    (repo / nuevo).write_text("id: editado\n", encoding="utf-8")
    _git(repo, "commit", "-q", "-am", "edita lo anadido en el merge")
    assert modificaciones_en_historial(repo) == [
        f"modificado desde {_primero(repo, nuevo)}: {nuevo}"
    ]
    _git(repo, "rm", "-q", nuevo)
    _git(repo, "commit", "-q", "-m", "borra lo anadido en el merge")
    assert modificaciones_en_historial(repo) == [f"borrado o renombrado: {nuevo}"]


@pytest.mark.contract
def test_rutas_con_acento_y_espacio_se_vigilan(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    raro = "knowledge/evidence/v\u00eddeo 1/ev-x.yaml"
    (repo / raro).parent.mkdir()
    (repo / raro).write_text("id: a\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "a\u00f1ade \u00cdNDICE raro")
    (repo / raro).write_text("id: b\n", encoding="utf-8")
    _git(repo, "commit", "-q", "-am", "edita")
    assert modificaciones_en_historial(repo) == [f"modificado desde {_primero(repo, raro)}: {raro}"]


@pytest.mark.contract
def test_repositorio_real_sin_modificaciones(repo: Path) -> None:
    violaciones = modificaciones_en_historial(repo)
    if violaciones is None:
        assert not hay_git(repo), "hay git pero la guardia no se pudo evaluar"
        pytest.skip("sin git")
    assert violaciones == [], "\n".join(violaciones)


def _primero(repo: Path, ruta: str = EV) -> str:
    salida = subprocess.run(
        ["git", "log", "-m", "--format=%H", "--diff-filter=A", "--", ruta],
        cwd=repo,
        capture_output=True,
        encoding="utf-8",
        check=True,
    ).stdout.split()
    return salida[-1][:7]
