"""G2: todo commit que toque `tramos_no_citables.yaml` lleva `Fuente:` (trabajo/guardias-citas).

Es la guardia de trazabilidad de spec y casos (`commits_sin_fuente`) sobre una ruta mas, con su
propia ancla. La garantia es este test en la CI contra la historia de git, como las guardias de
inmutabilidad (PROJECT_STATE, Decisions and Rationale, 2026-09-04). No hay un bucle propio: la
lectura del trailer es la de `commits_sin_fuente` (decision 3 del consultor del 2026-10-05).

EL ANCLA ES UN SHA, NUNCA UNA FECHA NI UN TAG: `c489685`, el ultimo commit que toco el fichero sin
`Fuente:` (docs/validation/GUARDIAS-CITAS.md §0.c). Los tres que deja fuera -`cfec50b` y `c489685`
sin trailer, `f443eee` con una ruta en vez de un id- no se tocan. Si el ancla no existe en la
historia (un clon superficial, una historia reescrita), el test FALLA, no se salta.

Los tests de mas abajo rompen la guardia a proposito en repos temporales, nunca en el real.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from botsito.comun.historial import commits_sin_fuente, hay_git, resolver

RUTA_TRAMOS = "knowledge/corpus/tramos_no_citables.yaml"
ANCLA_TRAMOS = "c489685f9ef5d1e126f2e3e81872c1f1c5a644fd"
QUE = "tramos_no_citables.yaml"


def problemas_tramos(repo: Path, ancla: str, ids_validos: set[str] | None = None) -> list[str]:
    """Lo que falla de G2 en `repo` desde `ancla`: un ancla que no existe o que no se puede evaluar
    es un fallo, no un «sin problemas»."""
    if resolver(repo, ancla) is None:
        return [f"el ancla de G2 {ancla[:7]} no existe en la historia de este clon"]
    problemas = commits_sin_fuente(
        repo, ancla, rutas=(RUTA_TRAMOS,), ids_validos=ids_validos, que=QUE
    )
    if problemas is None:
        return [f"la guardia de G2 no se pudo evaluar desde {ancla[:7]} (clon superficial?)"]
    return problemas


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=repo, check=True, capture_output=True, encoding="utf-8"
    ).stdout.strip()


def _repo(tmp_path: Path) -> tuple[Path, str]:
    """Repo temporal con el fichero de tramos y un primer commit, que hace de ancla."""
    _git(tmp_path, "init", "-q", "-b", "main")
    _git(tmp_path, "config", "user.email", "t@t")
    _git(tmp_path, "config", "user.name", "t")
    _git(tmp_path, "config", "core.autocrlf", "false")
    (tmp_path / RUTA_TRAMOS).parent.mkdir(parents=True)
    (tmp_path / RUTA_TRAMOS).write_text("tramos: []\n", encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "viejo, sin trailer")
    return tmp_path, _git(tmp_path, "rev-parse", "HEAD")


def _tocar(repo: Path, mensaje: str) -> str:
    ruta = repo / RUTA_TRAMOS
    ruta.write_text(ruta.read_text(encoding="utf-8") + "# otra linea\n", encoding="utf-8")
    _git(repo, "add", RUTA_TRAMOS)
    _git(repo, "commit", "-q", "-m", mensaje)
    return _git(repo, "rev-parse", "HEAD")


@pytest.mark.contract
def test_repositorio_real(repo: Path) -> None:
    if not hay_git(repo):
        pytest.skip("sin git")
    from botsito.evidence.modelo import cargar_evidencia
    from botsito.feedback.modelo import cargar_feedback
    from botsito.validation.knowledge import ids_de_fuente

    ids = ids_de_fuente(
        repo,
        cargar_evidencia(repo / "knowledge" / "evidence"),
        cargar_feedback(repo / "knowledge" / "feedback"),
    )
    problemas = problemas_tramos(repo, ANCLA_TRAMOS, ids)
    assert problemas == [], "\n".join(problemas)


@pytest.mark.contract
def test_el_ancla_es_un_sha_completo() -> None:
    assert len(ANCLA_TRAMOS) == 40
    assert all(c in "0123456789abcdef" for c in ANCLA_TRAMOS)


@pytest.mark.contract
def test_un_commit_tras_el_ancla_sin_fuente_falla(tmp_path: Path) -> None:
    repo, ancla = _repo(tmp_path)
    sha = _tocar(repo, "tramos: uno nuevo\n\nsin trailer")
    assert problemas_tramos(repo, ancla) == [
        f"{sha[:7]}: toca tramos_no_citables.yaml sin trailer 'Fuente:'"
    ]


@pytest.mark.contract
def test_un_commit_tras_el_ancla_con_fuente_pasa(tmp_path: Path) -> None:
    repo, ancla = _repo(tmp_path)
    _tocar(repo, "tramos: uno nuevo\n\nFuente: ADR-0038")
    assert problemas_tramos(repo, ancla, {"ADR-0038"}) == []


@pytest.mark.contract
def test_una_fuente_que_no_existe_falla(tmp_path: Path) -> None:
    repo, ancla = _repo(tmp_path)
    sha = _tocar(repo, "tramos: uno nuevo\n\nFuente: ADR-9999")
    assert problemas_tramos(repo, ancla, {"ADR-0038"}) == [
        f"{sha[:7]}: fuente inexistente ADR-9999"
    ]


@pytest.mark.contract
def test_el_commit_del_ancla_y_los_anteriores_no_se_miran(tmp_path: Path) -> None:
    repo, ancla = _repo(tmp_path)
    assert problemas_tramos(repo, ancla) == []
    _tocar(repo, "tramos: con trailer\n\nFuente: ADR-0038")
    assert problemas_tramos(repo, ancla) == []


@pytest.mark.contract
def test_un_ancla_inexistente_falla(tmp_path: Path) -> None:
    repo, _ = _repo(tmp_path)
    assert problemas_tramos(repo, "0" * 40) == [
        "el ancla de G2 0000000 no existe en la historia de este clon"
    ]


@pytest.mark.contract
def test_un_commit_que_no_toca_los_tramos_no_se_mira(tmp_path: Path) -> None:
    repo, ancla = _repo(tmp_path)
    (repo / "otro.txt").write_text("x\n", encoding="utf-8")
    _git(repo, "add", "otro.txt")
    _git(repo, "commit", "-q", "-m", "otra cosa, sin trailer")
    assert problemas_tramos(repo, ancla) == []


@pytest.mark.contract
def test_el_mensaje_por_defecto_es_el_de_siempre(tmp_path: Path) -> None:
    """Decision 3: con el valor por defecto de `que`, el mensaje es byte a byte el de antes de
    `trabajo/guardias-citas`."""
    repo, ancla = _repo(tmp_path)
    sha = _tocar(repo, "sin trailer")
    assert commits_sin_fuente(repo, ancla, rutas=(RUTA_TRAMOS,)) == [
        f"{sha[:7]}: toca spec/cases sin trailer 'Fuente:'"
    ]
