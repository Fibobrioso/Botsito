"""Los dias retirados del holdout (ADR-0041): fuera de lo que se mide, dentro de lo que se oculta.

Retirar no es desreservar. Un dia retirado deja de contar en su particion, pero sus etiquetas no se
leen nunca: la puerta lo rechaza con o sin autorizacion. Y la retirada vive en su propio fichero,
SOLO ANADIR y por la huella del id, porque el reparto se reproduce byte a byte y no se toca.
"""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

import pytest

from botsito import cli
from botsito.cases.holdout import (
    FICHERO_PREREGISTRO,
    FICHERO_RETIRADOS,
    HoldoutCerradoError,
    RetiradosError,
    abrir,
    abrir_caso,
    cargar_retirados,
    casos_medidos,
    casos_ocultos,
    casos_reservados,
    casos_retirados,
    huella_de_caso,
    problemas_de_retirados,
)

REPO = Path(__file__).resolve().parents[2]
RETIRADO = "caso-xxxyyy-2026-05-04"
MEDIDO = "caso-xxxyyy-2026-05-05"


def _git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t", *args],
        check=True,
        capture_output=True,
    )


def _blob(texto: str) -> str:
    datos = texto.encode("utf-8")
    return hashlib.sha1(b"blob %d\x00" % len(datos) + datos).hexdigest()  # noqa: S324


RELLENO = "# PREREGISTRO\n\n## Preguntas\n\n- pregunta: P1 | estado: ABIERTA | una pregunta\n"
AUTORIZACION = (
    "particion: holdout-2\nautorizado_por: el usuario\nfecha: 2026-10-01\nadr: ADR-0099\n"
    f"pregunta: P1\npreregistro_blob: {_blob(RELLENO)}\n"
)


def _entrada(motivo: str = "expuesto") -> str:
    return (
        f"    motivo: {motivo}\n    exposicion: HOLDOUT-EXPOSICIONES, la entrada del dia\n"
        f"    adr: ADR-0099\n    retirado_el: '2026-10-01'\n"
    )


def _retirados(*huellas: str, motivo: str = "expuesto") -> str:
    return "retirados:\n" + "".join(f'  "{h}":\n{_entrada(motivo)}' for h in huellas)


def _repo(tmp_path: Path, retirados: str | None) -> Path:
    """Un repositorio con dos casos en `holdout-2`, autorizacion valida para abrirlo y, si se
    pide, un `retirados.yaml`."""
    kit = tmp_path / "knowledge" / "cases" / "kit" / "s1"
    kit.mkdir(parents=True)
    (kit / "particiones.yaml").write_text(
        f"asignacion:\n  {RETIRADO}: holdout-2\n  {MEDIDO}: holdout-2\n", encoding="utf-8"
    )
    (tmp_path / "docs" / "adr").mkdir(parents=True)
    (tmp_path / "docs" / "adr" / "0099-retirada.md").write_text("# 99\n", encoding="utf-8")
    (tmp_path / "docs" / "validation").mkdir(parents=True)
    (tmp_path / FICHERO_PREREGISTRO).write_text(RELLENO, encoding="utf-8")
    (tmp_path / "docs" / "validation" / "AUTORIZACION-holdout-2.md").write_text(
        AUTORIZACION, encoding="utf-8"
    )
    if retirados is not None:
        (tmp_path / FICHERO_RETIRADOS).write_text(retirados, encoding="utf-8")
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "x")
    return tmp_path


def test_un_retirado_no_se_mide_se_oculta_y_la_puerta_lo_rechaza_con_autorizacion(
    tmp_path: Path,
) -> None:
    repo = _repo(tmp_path, _retirados(huella_de_caso(RETIRADO)))
    assert RETIRADO not in casos_medidos(repo)
    assert MEDIDO in casos_medidos(repo)
    assert RETIRADO in casos_ocultos(repo) and MEDIDO in casos_ocultos(repo)
    assert casos_retirados(repo) == {RETIRADO: "holdout-2"}
    # La autorizacion es valida: la particion se abre, y el caso medido tambien...
    abrir(repo, "holdout-2", "P1")
    abrir_caso(repo, MEDIDO, "P1")
    # ...y el retirado NO, con esa misma autorizacion. El mensaje no lo nombra.
    with pytest.raises(HoldoutCerradoError, match="no se abre nunca") as exc:
        abrir_caso(repo, RETIRADO, "P1")
    assert RETIRADO not in str(exc.value) and "2026-05-04" not in str(exc.value)


def test_sin_fichero_no_hay_retirados_y_medidos_son_los_reservados(tmp_path: Path) -> None:
    repo = _repo(tmp_path, None)
    assert cargar_retirados(repo) == {}
    assert casos_medidos(repo) == casos_reservados(repo) == casos_ocultos(repo)


def test_retirados_es_solo_anadir_contra_el_historial(tmp_path: Path) -> None:
    """El mismo mecanismo que `libros.yaml`: cada version contiene, identicas, las anteriores."""
    huella = huella_de_caso(RETIRADO)
    repo = _repo(tmp_path, _retirados(huella))
    assert problemas_de_retirados(repo) == []
    # anadir una entrada si vale
    (repo / FICHERO_RETIRADOS).write_text(
        _retirados(huella, huella_de_caso(MEDIDO)), encoding="utf-8"
    )
    assert problemas_de_retirados(repo) == []
    # modificar una entrada commiteada
    (repo / FICHERO_RETIRADOS).write_text(_retirados(huella, motivo="otro"), encoding="utf-8")
    assert any("modifica la retirada" in p for p in problemas_de_retirados(repo))
    # borrarla
    (repo / FICHERO_RETIRADOS).write_text("retirados: {}\n", encoding="utf-8")
    assert any("borra la retirada" in p for p in problemas_de_retirados(repo))
    # y commitear el borrado no lo arregla: el historial lo sigue viendo
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "borra")
    assert any("borra la retirada" in p for p in problemas_de_retirados(repo))


def test_una_huella_que_no_es_de_ningun_reservado_falla(tmp_path: Path) -> None:
    repo = _repo(tmp_path, _retirados(huella_de_caso("caso-xxxyyy-2026-05-06")))
    assert any(
        "no es la huella de ningun caso reservado" in p for p in problemas_de_retirados(repo)
    )


def test_una_entrada_mal_formada_cierra_la_puerta(tmp_path: Path) -> None:
    repo = _repo(tmp_path, f'retirados:\n  "{huella_de_caso(RETIRADO)}":\n    motivo: x\n')
    with pytest.raises(RetiradosError):
        casos_medidos(repo)
    assert problemas_de_retirados(repo)


def test_el_repo_real_retira_uno_y_ninguna_salida_lo_nombra(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """En el repositorio: 34 reservados, 33 medidos, 1 retirado. Y ninguna de las salidas de los
    comandos que recorren casos imprime el id del retirado. El id no se escribe en este test: se
    deriva de la huella."""
    retirados = casos_retirados(REPO)
    assert len(retirados) == 1
    assert len(casos_medidos(REPO)) == len(casos_reservados(REPO)) - 1
    (caso,) = retirados
    kit = sorted(p.parent.name for p in (REPO / "knowledge/cases/kit").glob("*/particiones.yaml"))
    fid = sorted(
        p.parent.name for p in (REPO / "knowledge/cases/fidelidad").glob("*/particiones.yaml")
    )
    comandos = [
        ["knowledge", "validate"],
        ["state", "check"],
        ["casos", "check"],
        ["spec", "status"],
        ["feedback", "pending"],
        *(["kit", "check", "--sesion", s] for s in kit),
        *(["fidelidad", "check", "--artefacto", a] for a in fid),
    ]
    for argv in comandos:
        capsys.readouterr()
        cli.main(["--repo", str(REPO), *argv])
        salida = capsys.readouterr()
        assert caso not in salida.out + salida.err, f"{' '.join(argv)} imprime el id del retirado"
