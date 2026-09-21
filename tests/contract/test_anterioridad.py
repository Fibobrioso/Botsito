"""La anterioridad se prueba por CASO, no por sesion (ADR-0036).

La guardia del kit empareja los `LABEL_CASE` por el campo `sesion` del registro y nunca por el caso
que etiquetan. Es deuda anotada cuatro veces, y aqui se ve fallar de verdad: una etiqueta sobre un
caso repartido, llevando en `sesion` el nombre de OTRO paquete, pasaba entera. En el camino de
fidelidad no hay `sesion` siquiera, asi que emparejar por ella no es insuficiente: es imposible.

Todo en repositorios sinteticos, porque en el real no hay ni un `LABEL_CASE`: adoptar la guardia
hoy cuesta cero, y dentro de un mes costaria renunciar a ella.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from botsito.cases.anterioridad import problemas_de_anterioridad
from botsito.feedback.modelo import FeedbackRecord, cargar_feedback, escribir_registro

CASO = "caso-xxxyyy-2026-05-06"
SESION = "2026-09-15-sesion-01"
KIT = f"knowledge/cases/kit/{SESION}"
FIDELIDAD = "knowledge/cases/fidelidad/xxxyyy-2026-05"


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def _repo(tmp_path: Path) -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    _git(tmp_path, "init", "-q", "-b", "main")
    _git(tmp_path, "config", "user.email", "t@t")
    _git(tmp_path, "config", "user.name", "t")
    _git(tmp_path, "config", "core.autocrlf", "false")
    (tmp_path / "README.md").write_text("x", encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "inicio")
    return tmp_path


def _reparto(repo: Path, directorio: str, caso: str, clave: str, nombre: str) -> None:
    """Un `particiones.yaml` minimo, del camino que sea: los dos se leen igual."""
    (repo / directorio).mkdir(parents=True, exist_ok=True)
    (repo / directorio / "particiones.yaml").write_text(
        f"{clave}: {nombre}\nseed: 1\nasignacion:\n  {caso}: dev\n", encoding="utf-8"
    )
    (repo / directorio / "ventanas.yaml").write_text(
        f"{clave}: {nombre}\ncasos:\n  - id: {caso}\n", encoding="utf-8"
    )


def _etiqueta(repo: Path, caso: str, sesion: str = SESION) -> None:
    escribir_registro(
        repo / "knowledge" / "feedback",
        {
            "sesion": sesion,
            "fecha": sesion[:10],
            "recibido_el": sesion[:10],
            "procedencia": "trader_hoja",
            "medio": "escrito",
            "objetivo": {"tipo": "caso", "id": caso},
            "accion": "LABEL_CASE",
            "respuesta_literal": "venta en la primera sesion",
            "valor_resultante": "07-11: venta; 11-15: no_trade",
            "registrado_por": "aleks",
        },
    )


def _registros(repo: Path) -> list[FeedbackRecord]:
    return cargar_feedback(repo / "knowledge" / "feedback")


@pytest.mark.contract
def test_el_reparto_anterior_a_la_etiqueta_pasa(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    _reparto(repo, KIT, CASO, "sesion", SESION)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "reparto\n\nFuente: ADR-0011")
    _etiqueta(repo, CASO)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "etiqueta")
    assert problemas_de_anterioridad(repo, _registros(repo)) == []


@pytest.mark.contract
def test_mutante_la_etiqueta_antes_que_su_reparto_falla(tmp_path: Path) -> None:
    """El mutante que manda: si el reparto no es anterior, la guardia lo dice."""
    repo = _repo(tmp_path)
    _etiqueta(repo, CASO)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "etiqueta primero")
    _reparto(repo, KIT, CASO, "sesion", SESION)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "reparto despues\n\nFuente: ADR-0011")
    problemas = problemas_de_anterioridad(repo, _registros(repo))
    assert len(problemas) == 1 and "no es anterior" in problemas[0]

    # En el MISMO commit tampoco vale: no habria forma de ordenarlos.
    otro = _repo(tmp_path / "juntos")
    _reparto(otro, KIT, CASO, "sesion", SESION)
    _etiqueta(otro, CASO)
    _git(otro, "add", "-A")
    _git(otro, "commit", "-q", "-m", "todo junto\n\nFuente: ADR-0011")
    problemas2 = problemas_de_anterioridad(otro, _registros(otro))
    assert len(problemas2) == 1 and "no es anterior" in problemas2[0]


@pytest.mark.contract
def test_una_etiqueta_sobre_un_caso_sin_reparto_no_pasa(tmp_path: Path) -> None:
    """El agujero entero, en una linea: hoy nadie comprueba que el caso este repartido."""
    repo = _repo(tmp_path)
    _reparto(repo, KIT, CASO, "sesion", SESION)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "reparto\n\nFuente: ADR-0011")
    _etiqueta(repo, "caso-xxxyyy-2026-09-01")  # un caso que no esta en ningun reparto
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "etiqueta de un caso ajeno")
    problemas = problemas_de_anterioridad(repo, _registros(repo))
    assert len(problemas) == 1 and "ningun reparto commiteado contiene" in problemas[0]


@pytest.mark.contract
def test_empareja_por_caso_aunque_la_sesion_sea_de_otro_paquete(tmp_path: Path) -> None:
    """Lo que la guardia por `sesion` no veia: la etiqueta llega con el nombre de otra sesion.

    El caso etiquetado esta en un reparto que se commiteo DESPUES. Con el emparejamiento por
    `sesion` el bucle ni visita ese reparto -la sesion del registro no es la suya- y todo pasa.
    """
    repo = _repo(tmp_path)
    _reparto(repo, KIT, CASO, "sesion", SESION)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "reparto viejo\n\nFuente: ADR-0011")
    _etiqueta(repo, "caso-xxxyyy-2026-05-07", sesion=SESION)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "etiqueta con sesion del paquete viejo")
    _reparto(repo, FIDELIDAD, "caso-xxxyyy-2026-05-07", "artefacto", "xxxyyy-2026-05")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "reparto nuevo despues\n\nFuente: ADR-0036")
    problemas = problemas_de_anterioridad(repo, _registros(repo))
    assert len(problemas) == 1 and "no es anterior" in problemas[0]
    assert "xxxyyy-2026-05" in problemas[0], "empareja por el caso, no por la sesion del registro"


@pytest.mark.contract
def test_un_caso_repartido_dos_veces_es_problema(tmp_path: Path) -> None:
    """Dos repartos del mismo dia harian ambigua la prueba: cual tiene que ser anterior."""
    repo = _repo(tmp_path)
    _reparto(repo, KIT, CASO, "sesion", SESION)
    _reparto(repo, FIDELIDAD, CASO, "artefacto", "xxxyyy-2026-05")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "dos repartos\n\nFuente: ADR-0036")
    problemas = problemas_de_anterioridad(repo, [])  # sin una sola etiqueta ya se ve
    assert len(problemas) == 1 and "repartido dos veces" in problemas[0]
