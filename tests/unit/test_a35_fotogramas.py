"""Los fotogramas de A-35 (`scripts/a35_fotogramas.py`): la lista cerrada son las ventanas de los
segmentos, nada se lee fuera de ella, un PNG que no es el de F05 se rechaza antes de decodificar y
el recuento de pixeles distintos. Sin abrir ningun fotograma real."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType

import pytest

RAIZ = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def m() -> ModuleType:
    nombre = "a35_fotogramas"
    if nombre in sys.modules:
        return sys.modules[nombre]
    spec = importlib.util.spec_from_file_location(nombre, RAIZ / "scripts" / f"{nombre}.py")
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def test_la_lista_cerrada_son_las_ventanas_de_los_segmentos(m: ModuleType) -> None:
    assert set(m.MEDIR) == {"P4", "P5", "P6", "P8", "P9"}
    for pasaje, (video, _, t0, t1, citado) in m.VENTANAS.items():
        nombres = m.MEDIR[pasaje]
        assert video in ("v3", "v4")  # solo los videos del brief
        assert len(nombres) == t1 - t0 + 1 == len(set(nombres))
        assert nombres[0] == f"{t0 * 1000:09d}" and nombres[-1] == f"{t1 * 1000:09d}"
        assert f"{citado * 1000:09d}" in nombres  # el fotograma citado cae dentro


def test_fuera_de_la_lista_falla_sin_leer_nada(
    m: ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    def prohibido(*_: object) -> None:
        raise AssertionError("no se puede leer nada antes de la lista cerrada")

    monkeypatch.setattr(m, "_png", prohibido)
    monkeypatch.setattr(m, "sha_esperados", prohibido)
    with pytest.raises(m.IntegridadError, match="fuera de la lista cerrada de P9"):
        m.verificar("P9", ("003426000",))  # el vecino ya medido: no esta en la ventana
    with pytest.raises(m.IntegridadError, match="pasaje fuera de la lista cerrada"):
        m.verificar("P1", ("000000000",))


def test_un_fotograma_que_no_es_el_de_f05_se_rechaza(
    m: ModuleType, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    nombre = m.MEDIR["P8"][0]
    carpeta = tmp_path / "v4" / "png-1fps"
    carpeta.mkdir(parents=True)
    png = carpeta / f"{nombre}.png"
    png.write_bytes(b"los bytes que F05 extrajo")
    indice = carpeta / "index.jsonl"
    fila = {"fichero": f"{nombre}.png", "sha256": hashlib.sha256(png.read_bytes()).hexdigest()}
    indice.write_text(json.dumps(fila) + "\n", encoding="utf-8")
    manifiestos = tmp_path / "manifiestos"
    manifiestos.mkdir()
    sha_indice = hashlib.sha256(indice.read_bytes()).hexdigest()
    manifiesto = manifiestos / "fr-v4-9ad0ebb8.yaml"
    manifiesto.write_text(f"sha256_index: {sha_indice}\n", encoding="utf-8")
    monkeypatch.setattr(m, "DATOS", tmp_path)
    monkeypatch.setattr(m, "MANIFIESTOS", manifiestos)

    assert m.verificar("P8", (nombre,))[0].endswith("= indice F05: OK")
    png.write_bytes(b"otros bytes")
    with pytest.raises(m.IntegridadError, match="no es el fotograma que extrajo F05"):
        m.verificar("P8", (nombre,))
    manifiesto.write_text("sha256_index: " + "0" * 64 + "\n", encoding="utf-8")
    with pytest.raises(m.IntegridadError, match="index.jsonl no es el que fija"):
        m.verificar("P8", (nombre,))


def test_distintos_cuenta_pixeles_no_bytes(m: ModuleType) -> None:
    a = bytes([1, 2, 3, 4, 5, 6])
    assert m.distintos(a, a, 3) == 0
    assert m.distintos(a, bytes([1, 2, 9, 4, 5, 6]), 3) == 1
    assert m.distintos(a, bytes([9, 9, 9, 9, 9, 9]), 3) == 2
    with pytest.raises(ValueError):
        m.distintos(a, a[:3], 3)
