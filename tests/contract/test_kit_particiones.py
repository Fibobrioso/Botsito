"""F10 (MASTER_PLAN H "Tres particiones reservadas"): la asignacion de casos se commitea ANTES de la
sesion de etiquetado. La guardia es de ancestro en git (el commit que anadio particiones.yaml
precede al que anadio el primer LABEL_CASE de la sesion), no de fecha.

Y desde el 2026-09-21, el ANCLA del paquete (ADR-0035, enmienda): lo que un paquete congela dentro
de si mismo -el universo en `datasets:`, los cupos en el bloque `config:`- se ata por el sha de su
BLOB desde `anclas.yaml`, que vive fuera. Sin eso, congelar no seria falsable: editar a mano
`anclajes_candidatos`, `sesiones` o `etiquetas` del bloque congelado no cambia `particiones.yaml`,
y una sesion celebrada exime `ventanas.yaml`. Medido antes de escribir nada: exit 0."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from botsito import cli
from botsito.cases.paquete import anclas_del_arbol, escribir_anclas, validar_paquetes
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
        f"sesion: {SESION}\ndatasets:\n  - prueba-1\n"
        f"casos:\n  - id: {caso}\n    dataset_id: prueba-1\n",
        encoding="utf-8",
    )
    (repo / KIT / "particiones.yaml").write_text(
        f"sesion: {SESION}\nseed: 1\nasignacion:\n  {caso}: dev\n", encoding="utf-8"
    )
    (repo / KIT / "hoja_trader.md").write_text("# hoja\n", encoding="utf-8")


def _anclar(repo: Path) -> None:
    """El ancla del paquete (ADR-0035, enmienda del 2026-09-21). Va en el mismo commit que el
    paquete: sin ella, `validar_paquetes` dice que lo congelado no esta atado contra
    manipulacion. NO depende de que existan etiquetas, a proposito."""
    escribir_anclas(repo, {SESION: anclas_del_arbol(repo, SESION)})


def _etiqueta(repo: Path, caso: str) -> None:
    escribir_registro(
        repo / "knowledge" / "feedback",
        {
            "sesion": SESION,
            "fecha": SESION[:10],
            "recibido_el": SESION[:10],
            "procedencia": "trader_hoja",
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
    _anclar(repo)
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
    _anclar(repo)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "kit despues\n\nFuente: ADR-0011")
    registros = cargar_feedback(repo / "knowledge" / "feedback")
    problemas, _ = validar_paquetes(repo, registros, {"ev-v1-000010-aaaaaaaa"}, {"prueba-1"})
    assert len(problemas) == 1 and "no es anterior" in problemas[0]
    # en el MISMO commit tampoco vale
    (tmp_path / "dos").mkdir()
    repo2 = _repo(tmp_path / "dos")
    _paquete(repo2, caso)
    _anclar(repo2)
    _etiqueta(repo2, caso)
    _git(repo2, "add", "-A")
    _git(repo2, "commit", "-q", "-m", "todo junto\n\nFuente: ADR-0011")
    registros2 = cargar_feedback(repo2 / "knowledge" / "feedback")
    problemas2, _ = validar_paquetes(repo2, registros2, {"ev-v1-000010-aaaaaaaa"}, {"prueba-1"})
    assert len(problemas2) == 1 and "no es anterior" in problemas2[0]
    assert es_ancestro(repo2, "HEAD", "0000000000000000000000000000000000000000") is None


@pytest.mark.contract
def test_particiones_inmutables_tras_el_etiquetado(tmp_path: Path) -> None:
    """B-1 de la auditoria: reasignar despues del etiquetado, commiteado o solo en el arbol de
    trabajo, es error.

    Hasta el 2026-09-21 este test afirmaba ademas que ANTES del etiquetado el paquete se podia
    regenerar libremente: `validar_paquetes` se desentendia con `if not etiquetas: continue`. Eso
    dejaba de pie el agujero que la enmienda de ADR-0035 cierra: hoy no existe ni un `LABEL_CASE`
    en el repositorio -118 registros de feedback, ninguno- y el periodo "antes de la primera
    etiqueta" es justo aquel en el que hay que poder confiar en lo congelado. El ANCLA no hereda
    ese `continue`: ata el fichero entero por el sha de su blob, con etiquetas o sin ellas.
    """
    repo = _repo(tmp_path)
    caso = "caso-xxxyyy-2026-05-06"
    _paquete(repo, caso)
    _anclar(repo)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "kit\n\nFuente: ADR-0011")
    ruta = repo / KIT / "particiones.yaml"
    ruta.write_text(ruta.read_text(encoding="utf-8").replace("dev", "holdout-1"), encoding="utf-8")
    problemas, _ = validar_paquetes(repo, [], {"ev-v1-000010-aaaaaaaa"}, {"prueba-1"})
    assert any("no coincide con su ancla" in p for p in problemas), (
        "sin una sola etiqueta, tocar la asignacion tiene que verse igual"
    )
    ruta.write_text(ruta.read_text(encoding="utf-8").replace("holdout-1", "dev"), encoding="utf-8")
    assert validar_paquetes(repo, [], {"ev-v1-000010-aaaaaaaa"}, {"prueba-1"}) == ([], [])
    _etiqueta(repo, caso)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "feedback")
    registros = cargar_feedback(repo / "knowledge" / "feedback")
    assert validar_paquetes(repo, registros, {"ev-v1-000010-aaaaaaaa"}, {"prueba-1"}) == ([], [])
    ruta.write_text(ruta.read_text(encoding="utf-8").replace("dev", "holdout-1"), encoding="utf-8")
    problemas, _ = validar_paquetes(repo, registros, {"ev-v1-000010-aaaaaaaa"}, {"prueba-1"})
    assert any("particiones.yaml cambio" in p for p in problemas)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "reasignacion\n\nFuente: ADR-0011")
    problemas, _ = validar_paquetes(repo, registros, {"ev-v1-000010-aaaaaaaa"}, {"prueba-1"})
    assert any("particiones.yaml cambio" in p for p in problemas)
    # Y commitear la reasignacion no la lava: el ancla vive FUERA del fichero que ata, asi que
    # sigue diciendo el blob viejo. Re-anclar es un acto explicito, no un efecto colateral.
    assert any("el paquete cambio despues de anclarse" in p for p in problemas)


@pytest.mark.contract
def test_el_ancla_ata_ventanas_aunque_no_cambie_la_asignacion(tmp_path: Path) -> None:
    """El agujero que motivo esta guardia, en su forma minima.

    La falsabilidad de lo congelado no es uniforme: editar `particiones` dentro del bloque
    `config:` cambia la asignacion y `particiones.yaml` -que no se exime nunca- deja de
    reproducirse, asi que se ve. Pero `anclajes_candidatos`, `sesiones` y `etiquetas` solo
    alimentan `ventanas.yaml` y `hoja_trader.md`, que una sesion celebrada SI exime. Medido en el
    repositorio real el 2026-09-21 antes de tocar nada: renombrar la etiqueta del anclaje dentro
    del bloque congelado daba `exit 0` y "sin diferencias que no explique la sesion celebrada".

    Aqui se prueba la propiedad que lo cierra: CUALQUIER byte de `ventanas.yaml` que no coincida
    con su ancla se ve, sin etiquetas, sin `data/` y sin depender de que la asignacion cambie.
    """
    repo = _repo(tmp_path)
    caso = "caso-xxxyyy-2026-05-06"
    _paquete(repo, caso)
    _anclar(repo)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "kit\n\nFuente: ADR-0011")
    assert validar_paquetes(repo, [], {"ev-v1-000010-aaaaaaaa"}, {"prueba-1"}) == ([], [])

    ventanas = repo / KIT / "ventanas.yaml"
    antes = (repo / KIT / "particiones.yaml").read_text(encoding="utf-8")
    ventanas.write_text(
        ventanas.read_text(encoding="utf-8") + "anclajes_candidatos: [servidor-ny-99]\n",
        encoding="utf-8",
    )
    problemas, _ = validar_paquetes(repo, [], {"ev-v1-000010-aaaaaaaa"}, {"prueba-1"})
    assert any("ventanas.yaml" in p and "no coincide con su ancla" in p for p in problemas)
    assert (repo / KIT / "particiones.yaml").read_text(encoding="utf-8") == antes, (
        "la prueba solo vale si la asignacion NO cambio: es el caso que se escapaba"
    )


@pytest.mark.contract
def test_un_paquete_sin_ancla_no_pasa_y_reanclar_es_explicito(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Sin ancla no se valida -congelar sin atar no es congelar- y re-anclar se pide a proposito."""
    repo = _repo(tmp_path)
    caso = "caso-xxxyyy-2026-05-06"
    _paquete(repo, caso)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "kit sin ancla\n\nFuente: ADR-0011")
    problemas, _ = validar_paquetes(repo, [], {"ev-v1-000010-aaaaaaaa"}, {"prueba-1"})
    assert len(problemas) == 2 and all("sin ancla" in p for p in problemas)

    assert cli.main(["--repo", str(repo), "kit", "anclar", "--sesion", SESION]) == 0
    assert validar_paquetes(repo, [], {"ev-v1-000010-aaaaaaaa"}, {"prueba-1"}) == ([], [])
    # Anclar dos veces lo mismo es idempotente y no toca el fichero.
    assert cli.main(["--repo", str(repo), "kit", "anclar", "--sesion", SESION]) == 0
    assert "ya esta anclada" in capsys.readouterr().out

    ruta = repo / KIT / "particiones.yaml"
    ruta.write_text(ruta.read_text(encoding="utf-8").replace("dev", "holdout-1"), encoding="utf-8")
    assert cli.main(["--repo", str(repo), "kit", "anclar", "--sesion", SESION]) == 1
    assert "Re-anclar es un acto explicito" in capsys.readouterr().err
    assert cli.main(["--repo", str(repo), "kit", "anclar", "--sesion", SESION, "--reanclar"]) == 0
    assert "re-anclada" in capsys.readouterr().out
