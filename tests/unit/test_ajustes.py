from pathlib import Path

import pytest

from botsito.config.ajustes import AjustesError, cargar_ajustes

OK = """
[entorno]
nombre = "backtest"

[rutas]
corpus = "corpus"
data = "data"
knowledge = "knowledge"
"""


def _w(tmp_path: Path, contenido: str) -> Path:
    p = tmp_path / "settings.toml"
    p.write_text(contenido, encoding="utf-8")
    return p


def test_carga_valida(tmp_path: Path) -> None:
    a = cargar_ajustes(_w(tmp_path, OK))
    assert a.entorno == "backtest" and a.knowledge == Path("knowledge")


def test_ejemplo_del_repo_es_valido(repo: Path) -> None:
    cargar_ajustes(repo / "config" / "settings.example.toml")


def test_seccion_no_permitida(tmp_path: Path) -> None:
    with pytest.raises(AjustesError, match="seccion no permitida"):
        cargar_ajustes(_w(tmp_path, OK + "\n[estrategia]\nstop = 0.75\n"))


def test_clave_que_colisiona_con_el_registro(tmp_path: Path) -> None:
    contenido = OK.replace('nombre = "backtest"', 'nombre = "backtest"\nstop_fraccion = "0.75"')
    with pytest.raises(AjustesError, match="parametro del registro"):
        cargar_ajustes(_w(tmp_path, contenido), frozenset({"stop_fraccion"}))


def test_clave_desconocida(tmp_path: Path) -> None:
    contenido = OK.replace('nombre = "backtest"', 'nombre = "backtest"\notra = 1')
    with pytest.raises(AjustesError, match="clave no permitida"):
        cargar_ajustes(_w(tmp_path, contenido))


def test_entorno_invalido(tmp_path: Path) -> None:
    with pytest.raises(AjustesError, match="entorno"):
        cargar_ajustes(_w(tmp_path, OK.replace("backtest", "produccion")))


def test_falta_ruta(tmp_path: Path) -> None:
    with pytest.raises(AjustesError, match="falta"):
        cargar_ajustes(_w(tmp_path, OK.replace('data = "data"\n', "")))
