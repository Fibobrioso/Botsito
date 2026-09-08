"""F10 (MASTER_PLAN H "Tres particiones reservadas"): la asignacion de casos se commitea ANTES de la
sesion de etiquetado. La guardia es de ancestro en git (el commit que anadio particiones.yaml
precede al que anadio el primer LABEL_CASE de la sesion), no de fecha."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from botsito.cases.paquete import validar_paquetes
from botsito.comun.historial import commit_que_anadio, es_ancestro
from botsito.feedback.modelo import cargar_feedback, escribir_registro

SESION = "2026-09-15-sesion-01"
KIT = f"knowledge/cases/kit/{SESION}"


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def _repo(tmp_path: Path) -> Path:
    _git(tmp_path, "init", "-q", "-b", "main")
    _git(tmp_path, "config", "user.email", "t@t")
    _git(tmp_path, "config", "user.name", "t")
    _git(tmp_path, "config", "core.autocrlf", "false")
    (tmp_path / "README.md").write_text("x", encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "inicio")
    return tmp_path


def _paquete(repo: Path, caso: str) -> None:
    (repo / KIT).mkdir(parents=True)
    (repo / KIT / "cuestionario.yaml").write_text(
        f"sesion: {SESION}\npreguntas:\n  - id: P-01\n    casos:\n"
        "      - evidencia: ev-v1-000010-aaaaaaaa\n",
        encoding="utf-8",
    )
    (repo / KIT / "ventanas.yaml").write_text(
        f"sesion: {SESION}\ncasos:\n  - id: {caso}\n    dataset_id: prueba-1\n", encoding="utf-8"
    )
    (repo / KIT / "particiones.yaml").write_text(
        f"sesion: {SESION}\nseed: 1\nasignacion:\n  {caso}: dev\n", encoding="utf-8"
    )
    (repo / KIT / "hoja_trader.md").write_text("# hoja\n", encoding="utf-8")


def _etiqueta(repo: Path, caso: str) -> None:
    escribir_registro(
        repo / "knowledge" / "feedback",
        {
            "sesion": SESION,
            "fecha": SESION[:10],
            "medio": "escrito",
            "objetivo": {"tipo": "caso", "id": caso},
            "accion": "LABEL_CASE",
            "respuesta_literal": "venta en la primera sesion",
            "valor_resultante": "07-11: venta; 11-15: no_trade",
            "registrado_por": "aleks",
        },
    )


@pytest.mark.contract
def test_particiones_antes_del_etiquetado(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    caso = "caso-xxxyyy-2026-05-06"
    _paquete(repo, caso)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "kit: particiones\n\nFuente: ADR-0011")
    alta = commit_que_anadio(repo, f"{KIT}/particiones.yaml")
    assert alta is not None and alta[1].endswith("Z")
    _etiqueta(repo, caso)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "feedback: sesion 1")
    registros = cargar_feedback(repo / "knowledge" / "feedback")
    assert (
        es_ancestro(repo, alta[0], "HEAD") is True and es_ancestro(repo, "HEAD", alta[0]) is False
    )
    assert validar_paquetes(repo, registros, {"ev-v1-000010-aaaaaaaa"}, {"prueba-1"}) == ([], [])


@pytest.mark.contract
def test_particiones_despues_del_etiquetado_falla(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    caso = "caso-xxxyyy-2026-05-06"
    _etiqueta(repo, caso)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "feedback primero")
    _paquete(repo, caso)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "kit despues\n\nFuente: ADR-0011")
    registros = cargar_feedback(repo / "knowledge" / "feedback")
    problemas, _ = validar_paquetes(repo, registros, {"ev-v1-000010-aaaaaaaa"}, {"prueba-1"})
    assert len(problemas) == 1 and "no es anterior" in problemas[0]
    # en el MISMO commit tampoco vale
    (tmp_path / "dos").mkdir()
    repo2 = _repo(tmp_path / "dos")
    _paquete(repo2, caso)
    _etiqueta(repo2, caso)
    _git(repo2, "add", "-A")
    _git(repo2, "commit", "-q", "-m", "todo junto\n\nFuente: ADR-0011")
    registros2 = cargar_feedback(repo2 / "knowledge" / "feedback")
    problemas2, _ = validar_paquetes(repo2, registros2, {"ev-v1-000010-aaaaaaaa"}, {"prueba-1"})
    assert len(problemas2) == 1 and "no es anterior" in problemas2[0]
    assert es_ancestro(repo2, "HEAD", "0000000000000000000000000000000000000000") is None
