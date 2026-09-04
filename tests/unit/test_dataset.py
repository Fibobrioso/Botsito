"""Datasets congelados: descarga simulada, manifiesto inmutable, comprobacion y ventana."""

import lzma
import struct
from datetime import date
from pathlib import Path
from typing import Any

import pytest
import yaml

from botsito.data.dataset import (
    DatasetError,
    buscar_manifiesto,
    cargar_manifiesto,
    cargar_serie,
    comprobar,
    congelar,
    dias_entre,
    id_desde_hashes,
    manifiestos,
    validar_manifiesto,
)
from botsito.data.velas import formato_ts

REG = struct.Struct(">iiiiif")
HOY = date(2026, 9, 4)


def bi5_dia(precio: int, minutos: int = 1440, planas_desde: int | None = None) -> bytes:
    regs = []
    for m in range(minutos):
        if planas_desde is not None and m >= planas_desde:
            regs.append(REG.pack(m * 60, precio, precio, precio, precio, 0.0))
        else:
            # (t, abierta, cierre, minima, maxima, volumen)
            regs.append(REG.pack(m * 60, precio, precio + 1, precio - 1, precio + 2, 1.5))
    return lzma.compress(b"".join(regs))


def descarga_falsa(url: str) -> bytes | None:
    """Enero 2026: dias 1-3 presentes; dia 4 (domingo) 404; dia 5 vacio; dia 6 con tarde plana."""
    dia = int(url.split("/")[-2])
    if dia == 4:
        return None
    if dia == 5:
        return b""
    if dia == 6:
        return bi5_dia(100000, planas_desde=600)
    return bi5_dia(100000 + dia)


def _congelar(tmp_path: Path, **extra: Any) -> Any:
    kw: dict[str, Any] = {
        "repo": tmp_path,
        "carpeta_datos": tmp_path / "data",
        "nombre": "prueba",
        "simbolo": "XXXYYY",
        "escala": 100000,
        "desde": date(2026, 1, 1),
        "hasta": date(2026, 1, 6),
        "descarga": descarga_falsa,
        "hoy": HOY,
    }
    kw.update(extra)
    return congelar(**kw)


def test_congelar_escribe_csv_y_manifiesto(tmp_path: Path) -> None:
    c = _congelar(tmp_path)
    m = c.manifiesto
    assert m["dataset_id"].startswith("prueba-") and c.ruta_manifiesto.stem == m["dataset_id"]
    assert [f.name for f in c.ficheros] == ["XXXYYY_M1_2026-01.csv"]
    assert m["dias"] == {
        "presentes": 5,
        "ausentes": ["2026-01-04"],
        "sin_datos": ["2026-01-05"],
        "registros": 5760,
        "descartadas_planas_sin_volumen": 840,
        "descartadas_en_laborable": 840,
        "volumen_cero_no_planas": 0,
        "velas": 4920,
    }
    assert m["huecos"]["menores_de_60_min"] == 0
    assert [h["minutos"] for h in m["huecos"]["mayores"]] == [2880]  # dias 4 y 5 sin velas
    assert m["huso_datos"] == "UTC" and m["escala_volumen"] == 1000 and m["periodo_min"] == 1
    # El manifiesto se recarga y valida; el fichero coincide con el disco.
    doc = cargar_manifiesto(c.ruta_manifiesto)
    assert comprobar(doc, tmp_path / "data", hashes=True) == []
    assert manifiestos(tmp_path) == [c.ruta_manifiesto]
    assert buscar_manifiesto(tmp_path, "prueba") == c.ruta_manifiesto
    assert buscar_manifiesto(tmp_path, m["dataset_id"]) == c.ruta_manifiesto
    with pytest.raises(DatasetError, match="no hay manifiesto"):
        buscar_manifiesto(tmp_path, "otro")


def test_congelar_es_determinista_e_inmutable(tmp_path: Path) -> None:
    c1 = _congelar(tmp_path)
    with pytest.raises(DatasetError, match="ya existe"):
        _congelar(tmp_path)
    otro = tmp_path / "otro"
    otro.mkdir()
    c2 = _congelar(otro)
    assert c1.manifiesto["dataset_id"] == c2.manifiesto["dataset_id"]
    assert c1.ficheros[0].read_bytes() == c2.ficheros[0].read_bytes()
    # Datos distintos = id distinto; reemplaza_a enlaza con el anterior.
    c3 = _congelar(tmp_path, hasta=date(2026, 1, 3), reemplaza_a=c1.manifiesto["dataset_id"])
    assert c3.manifiesto["dataset_id"] != c1.manifiesto["dataset_id"]
    assert c3.manifiesto["reemplaza_a"] == c1.manifiesto["dataset_id"]
    with pytest.raises(DatasetError, match="reemplaza_a"):
        _congelar(tmp_path / "x", reemplaza_a="prueba-00000000")


@pytest.mark.parametrize(
    ("extra", "mensaje"),
    [
        ({"nombre": "Prueba"}, "nombre"),
        ({"simbolo": "eurusd"}, "simbolo"),
        ({"escala": 0}, "escala"),
        ({"escala": True}, "escala"),
        ({"hasta": HOY}, "anterior a hoy"),
        ({"desde": date(2026, 1, 7), "hasta": date(2026, 1, 6)}, "rango invalido"),
        ({"desde": date(2026, 1, 4), "hasta": date(2026, 1, 5)}, "ninguna vela"),
    ],
)
def test_congelar_rechazos(tmp_path: Path, extra: dict[str, Any], mensaje: str) -> None:
    with pytest.raises(DatasetError, match=mensaje):
        _congelar(tmp_path, **extra)
    assert not (tmp_path / "data").exists()


def test_comprobar_detecta_cambios(tmp_path: Path) -> None:
    c = _congelar(tmp_path)
    fichero = c.ficheros[0]
    original = fichero.read_bytes()
    fichero.write_bytes(original.replace(b"100001", b"100009", 1))
    assert comprobar(c.manifiesto, tmp_path / "data", hashes=False) == []  # mismo tamano
    assert comprobar(c.manifiesto, tmp_path / "data", hashes=True) == [
        f"hash distinto: {c.manifiesto['ficheros'][0]['ruta']}"
    ]
    with pytest.raises(DatasetError, match="alterado"):
        cargar_serie(c.manifiesto, tmp_path / "data")
    fichero.write_bytes(original + b"x")
    assert comprobar(c.manifiesto, tmp_path / "data", hashes=False)[0].startswith("tamano")
    fichero.unlink()
    assert comprobar(c.manifiesto, tmp_path / "data", hashes=False)[0].startswith("falta")


def test_cargar_serie_y_ventana(tmp_path: Path) -> None:
    c = _congelar(tmp_path)
    serie = cargar_serie(c.manifiesto, tmp_path / "data")
    assert serie.simbolo == "XXXYYY" and serie.escala == 100000 and len(serie.velas) == 4920
    ventana = cargar_serie(c.manifiesto, tmp_path / "data", date(2026, 1, 2), date(2026, 1, 2))
    assert len(ventana.velas) == 1440
    assert formato_ts(ventana.velas[0].inicio) == "2026-01-02T00:00Z"
    assert formato_ts(ventana.velas[-1].inicio) == "2026-01-02T23:59Z"
    fuera = cargar_serie(c.manifiesto, tmp_path / "data", date(2026, 3, 1), date(2026, 3, 2))
    assert fuera.velas == ()


def test_manifiesto_editado_o_corrupto(tmp_path: Path) -> None:
    c = _congelar(tmp_path)
    doc = yaml.safe_load(c.ruta_manifiesto.read_text(encoding="utf-8"))
    casos: list[tuple[dict[str, Any], str]] = [
        ({"huso_datos": "Europe/Madrid"}, "huso_datos"),
        ({"schema_version": 2}, "schema_version"),
        ({"escala": "100000"}, "escala"),
        ({"hasta": "2025-12-31"}, "hasta anterior"),
        ({"descargado_el": "ayer"}, "fecha"),
        ({"extra": 1}, "desconocidos"),
        ({"reemplaza_a": "x"}, "reemplaza_a"),
        ({"ficheros": []}, "lista no vacia"),
        ({"ficheros": [dict(doc["ficheros"][0], sha256="0" * 64)]}, "sufijo"),
        ({"ficheros": [dict(doc["ficheros"][0], ruta="../x.csv")]}, "ruta"),
        ({"ficheros": [dict(doc["ficheros"][0], bytes=True)]}, "bytes"),
        ({"dias": []}, "mapas"),
    ]
    for cambio, mensaje in casos:
        with pytest.raises(DatasetError, match=mensaje):
            validar_manifiesto(dict(doc, **cambio), "manifiesto")
    for campo in ("dataset_id", "ficheros", "huecos"):
        roto = dict(doc)
        del roto[campo]
        with pytest.raises(DatasetError, match="faltan"):
            validar_manifiesto(roto, "manifiesto")
    with pytest.raises(DatasetError, match="debe llamarse"):
        validar_manifiesto(doc, "otro-nombre-deadbeef.yaml")
    (tmp_path / "data" / "manifests" / "roto.yml").write_text("{", encoding="utf-8")
    with pytest.raises(DatasetError, match="inesperado"):
        manifiestos(tmp_path)


def test_utilidades() -> None:
    assert len(dias_entre(date(2026, 1, 1), date(2026, 1, 31))) == 31
    with pytest.raises(DatasetError):
        dias_entre(date(2026, 1, 2), date(2026, 1, 1))
    assert id_desde_hashes("a", ["x"]) == id_desde_hashes("a", ["x"])
    assert id_desde_hashes("a", ["x"]) != id_desde_hashes("a", ["y"])
