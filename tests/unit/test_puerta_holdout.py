"""La puerta del holdout se niega, y se ve negar (ADR-0021 §3, ADR-0033).

Todo lo que abre de verdad se prueba en repositorios temporales. El `PREREGISTRO.md` del proyecto
sigue vacio a proposito, y este fichero comprueba que, tal como esta, la puerta no deja pasar nada.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from botsito.cases.holdout import (
    FICHERO_PREREGISTRO,
    MARCA_SIN_RELLENAR,
    PARTICIONES_RESERVADAS,
    HoldoutCerradoError,
    abrir,
    casos_reservados,
    leer_fichero,
    motivos_de_cierre,
)

REPO = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("particion", PARTICIONES_RESERVADAS)
def test_con_el_preregistro_de_hoy_la_puerta_se_niega_y_nombra_adr_0021(particion: str) -> None:
    assert MARCA_SIN_RELLENAR in (REPO / FICHERO_PREREGISTRO).read_text(encoding="utf-8")
    with pytest.raises(HoldoutCerradoError, match="ADR-0021 §3") as exc:
        abrir(REPO, particion, "prueba")
    assert "sigue vacio" in str(exc.value)
    assert f"AUTORIZACION-{particion}.md" in str(exc.value)


def test_leer_material_del_holdout_real_pasa_por_la_puerta_y_se_niega() -> None:
    # la ruta no existe, y da igual: la puerta decide antes de abrir nada
    with pytest.raises(HoldoutCerradoError, match="holdout-2"):
        leer_fichero(REPO, "knowledge/cases/holdout/2/caso-xxxyyy-2026-05-07.yaml")
    # el README es libre
    assert leer_fichero(REPO, "knowledge/cases/holdout/1/README.md")
    with pytest.raises(ValueError, match="no esta en"):
        leer_fichero(REPO, "knowledge/cases/kit/config.yaml")


def test_los_casos_reservados_salen_de_la_asignacion_sin_abrir_nada() -> None:
    """Leer `particiones.yaml` no es abrir: es lo que dice que no se puede leer."""
    reservados = casos_reservados(REPO)
    assert set(reservados.values()) == set(PARTICIONES_RESERVADAS)
    por_particion = {
        p: sum(1 for v in reservados.values() if v == p) for p in PARTICIONES_RESERVADAS
    }
    # los cupos del paquete de la sesion 1 (config.yaml): 8 por particion reservada
    assert por_particion == dict.fromkeys(PARTICIONES_RESERVADAS, 8)
    assert "caso-eurusd-2026-05-14" in reservados  # el dia quemado sigue asignado a holdout-2


def _git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t", *args],
        check=True,
        capture_output=True,
    )


def _repo(tmp_path: Path, preregistro: str, autorizacion: str | None) -> Path:
    (tmp_path / "docs" / "validation").mkdir(parents=True)
    (tmp_path / "docs" / "adr").mkdir(parents=True)
    (tmp_path / "docs" / "adr" / "0099-apertura.md").write_text("# 99\n", encoding="utf-8")
    (tmp_path / FICHERO_PREREGISTRO).write_text(preregistro, encoding="utf-8")
    if autorizacion is not None:
        (tmp_path / "docs" / "validation" / "AUTORIZACION-holdout-2.md").write_text(
            autorizacion, encoding="utf-8"
        )
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "x")
    return tmp_path


BUENA = "particion: holdout-2\nautorizado_por: el usuario\nfecha: 2026-10-01\nadr: ADR-0099\n"
RELLENO = "# PREREGISTRO\n\numbral: 0.8\n"


def test_con_todo_en_orden_se_abre(tmp_path: Path) -> None:
    repo = _repo(tmp_path, RELLENO, BUENA)
    assert motivos_de_cierre(repo, "holdout-2") == []
    abrir(repo, "holdout-2", "prueba")  # no lanza
    # y la autorizacion es POR PARTICION: la de holdout-2 no abre holdout-1
    assert any("AUTORIZACION-holdout-1.md" in m for m in motivos_de_cierre(repo, "holdout-1"))


@pytest.mark.parametrize(
    ("preregistro", "autorizacion", "aguja"),
    [
        (f"# PREREGISTRO\n{MARCA_SIN_RELLENAR}\n", BUENA, "sigue vacio"),
        (RELLENO, None, "no hay autorizacion"),
        (RELLENO, BUENA.replace("holdout-2", "holdout-1"), "autoriza 'holdout-1'"),
        (RELLENO, BUENA.replace("ADR-0099", "ADR-0777"), "no es un ADR que exista"),
        (RELLENO, BUENA.replace("2026-10-01", "ayer"), "no es AAAA-MM-DD"),
        (RELLENO, "particion: holdout-2\n", "faltan"),
        (RELLENO, "particion: holdout-1\n" + BUENA, "claves repetidas"),
        (RELLENO, BUENA + "particion: holdout-1\n", "claves repetidas"),
    ],
)
def test_cada_motivo_de_cierre_salta_por_su_cuenta(
    tmp_path: Path, preregistro: str, autorizacion: str | None, aguja: str
) -> None:
    repo = _repo(tmp_path, preregistro, autorizacion)
    motivos = motivos_de_cierre(repo, "holdout-2")
    assert any(aguja in m for m in motivos), motivos
    with pytest.raises(HoldoutCerradoError):
        abrir(repo, "holdout-2", "prueba")


def test_una_autorizacion_sin_commitear_no_autoriza(tmp_path: Path) -> None:
    """Dificil de activar sin querer y trivial de auditar: lo que no esta en git no cuenta, y
    tampoco un fichero commiteado y cambiado despues en el arbol."""
    repo = _repo(tmp_path, RELLENO, None)
    auto = repo / "docs" / "validation" / "AUTORIZACION-holdout-2.md"
    auto.write_text(BUENA, encoding="utf-8")
    assert any("no hay autorizacion" in m for m in motivos_de_cierre(repo, "holdout-2"))
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "autoriza")
    assert motivos_de_cierre(repo, "holdout-2") == []
    (repo / FICHERO_PREREGISTRO).write_text(RELLENO + "umbral: 0.5\n", encoding="utf-8")
    assert any("no esta commiteado" in m for m in motivos_de_cierre(repo, "holdout-2"))


def test_un_bom_no_rompe_una_autorizacion_buena(tmp_path: Path) -> None:
    repo = _repo(tmp_path, RELLENO, "\ufeff" + BUENA)
    assert motivos_de_cierre(repo, "holdout-2") == []


def test_sin_el_ejecutable_de_git_se_cierra_con_un_motivo(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import botsito.cases.holdout as puerta

    repo = _repo(tmp_path, RELLENO, BUENA)

    def sin_git(_repo: Path, _ruta: str) -> str | None:
        raise FileNotFoundError("git")

    monkeypatch.setattr(puerta, "contenido_en_head", sin_git)
    motivos = motivos_de_cierre(repo, "holdout-2")
    assert any("no esta commiteado" in m for m in motivos), motivos


def test_sin_git_no_se_abre_nada(tmp_path: Path) -> None:
    (tmp_path / "docs" / "validation").mkdir(parents=True)
    (tmp_path / FICHERO_PREREGISTRO).write_text(RELLENO, encoding="utf-8")
    assert motivos_de_cierre(tmp_path, "holdout-1")
    assert motivos_de_cierre(tmp_path, "dev") == [
        f"'dev' no es una particion reservada {PARTICIONES_RESERVADAS}"
    ]
