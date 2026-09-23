"""El criterio de lectura de v5 (`scripts/v5_criterio.py`), sobre fotogramas SINTETICOS.

Ninguno de los cuatro fotogramas ya abiertos cumple a la vez a) -niveles 0 y 1 con linea propia- y
b) -herramienta valida-: por eso la medida quedo NO CONCLUYENTE. Asi que el unico positivo de la
cadena completa -valido, y SEPARA- es sintetico: una caja y una herramienta pintadas con los
colores calibrados, con el stop en 0,8 o en 1,0. Sin este test, nada demostraria que el criterio
sabe decir «separa» antes de mirar los 36 fotogramas.
"""

from __future__ import annotations

import importlib.util
import struct
import sys
import zlib
from pathlib import Path
from types import ModuleType

import pytest

RAIZ = Path(__file__).resolve().parents[2]
ANCHO, ALTO = 1280, 720
FONDO = (19, 19, 19)
GRIS, AZUL, VERDE = (136, 136, 136), (58, 102, 220), (100, 177, 103)
ROJO_ZONA, TEAL_ZONA = (59, 22, 26), (12, 41, 38)


def _cargar(nombre: str) -> ModuleType:
    if nombre in sys.modules:
        return sys.modules[nombre]
    spec = importlib.util.spec_from_file_location(nombre, RAIZ / "scripts" / f"{nombre}.py")
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def _png(filas: list[bytearray]) -> bytes:
    def chunk(tipo: bytes, datos: bytes) -> bytes:
        crc = zlib.crc32(tipo + datos) & 0xFFFFFFFF
        return struct.pack(">I", len(datos)) + tipo + datos + struct.pack(">I", crc)

    crudo = b"".join(b"\x00" + bytes(f) for f in filas)
    ihdr = struct.pack(">IIBBBBB", ANCHO, ALTO, 8, 2, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", zlib.compress(crudo))
        + chunk(b"IEND", b"")
    )


def _fotograma(stop_frac: float, tp_mult: float, desplaza_entrada: int = 0) -> object:
    """Caja de 100 px (nivel 1 en y=150, nivel 0 en y=250) en x 600..900, y una VENTA: stop por
    encima de la entrada, TP por debajo, en x 950..1100. El stop cae en `stop_frac` de la caja y el
    TP a `tp_mult` cajas por debajo de la entrada."""
    filas = [bytearray(bytes(FONDO) * ANCHO) for _ in range(ALTO)]

    def linea(y: int, x0: int, x1: int, color: tuple[int, int, int]) -> None:
        filas[y][x0 * 3 : (x1 + 1) * 3] = bytes(color) * (x1 - x0 + 1)

    y1, y0, caja = 150, 250, 100
    linea(y1, 600, 900, GRIS)
    linea(y0, 600, 900, GRIS)
    linea(round(y0 - 0.8 * caja), 600, 900, AZUL)
    linea(round(y0 - 0.5 * caja), 600, 900, VERDE)
    entrada = y0 + desplaza_entrada
    stop = round(y0 - stop_frac * caja)
    tp = round(y0 + tp_mult * caja)
    for y in range(stop, entrada - 1):
        linea(y, 950, 1100, ROJO_ZONA)
    for y in range(entrada + 2, tp + 1):
        linea(y, 950, 1100, TEAL_ZONA)
    return _cargar("decodificar_png").decodificar(_png(filas))


@pytest.fixture(scope="module")
def criterio() -> ModuleType:
    return _cargar("v5_criterio")


def test_stop_en_0_8_y_tp_a_2_4_cajas_separa_hacia_riesgo_real(criterio: ModuleType) -> None:
    lectura = criterio.evaluar("sintetico", _fotograma(0.8, 2.4))
    assert (lectura.a, lectura.b, lectura.valido) == (True, True, True)
    assert lectura.veredicto == "separa: riesgo_real", lectura


def test_stop_en_1_0_y_tp_a_3_cajas_separa_hacia_caja_completa(criterio: ModuleType) -> None:
    lectura = criterio.evaluar("sintetico", _fotograma(1.0, 3.0))
    assert lectura.valido and lectura.veredicto == "separa: caja_completa", lectura


def test_sin_ancla_comun_el_fotograma_no_es_valido(criterio: ModuleType) -> None:
    """Arista de entrada a 10 px del nivel 0: no comparten ancla (LA-CAJA-DEL-29-DE-ABRIL:180)."""
    lectura = criterio.evaluar("sintetico", _fotograma(0.8, 2.4, desplaza_entrada=10))
    assert not lectura.valido and lectura.motivo.startswith("ancla")


def test_la_agregacion_por_instante_y_global(criterio: ModuleType) -> None:
    lec = criterio.Lectura
    rr = lec("f", True, True, True, "valido", 0.5, 30.0, "separa: riesgo_real")
    cc = lec("f", True, True, True, "valido", 30.0, 0.5, "separa: caja_completa")
    nv = lec("f", False, False, False, "no cumple a) y b)")
    assert criterio.resultado_instante([nv, nv]) == "sin fotograma valido"
    assert criterio.resultado_instante([nv, rr]) == "separa: riesgo_real"
    assert criterio.resultado_instante([rr, cc]) == "contradictorio"
    g = criterio.resultado_global
    assert g({"1": "sin fotograma valido"}) == "la medida NO ESTA en v5"
    assert g({"1": "separa: riesgo_real", "2": "no separa"}) == "separacion hacia riesgo_real"
    assert g({"1": "separa: riesgo_real", "2": "separa: caja_completa"}).startswith(
        "contradictorio"
    )
    assert g({"1": "no separa", "2": "sin fotograma valido"}) == "no separa"


def test_la_lista_cerrada_son_36_de_la_ventana_y_ninguno_ya_abierto(criterio: ModuleType) -> None:
    assert len(criterio.MEDIR) == 36 == len(set(criterio.MEDIR))
    assert not set(criterio.MEDIR) & set(criterio.ABIERTOS)


def test_un_nombre_fuera_de_la_lista_falla_sin_decodificar_nada(
    criterio: ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    def prohibido(*_: object) -> None:
        raise AssertionError("no se puede leer ni decodificar nada antes de la lista cerrada")

    monkeypatch.setattr(criterio, "_png", prohibido)
    monkeypatch.setattr(criterio, "sha_esperados", prohibido)
    with pytest.raises(criterio.IntegridadError, match="fuera de la lista cerrada"):
        criterio.leer_para_medir("000216000")  # un abierto: no es de los 36
    with pytest.raises(criterio.IntegridadError, match="fuera de la lista cerrada"):
        criterio.verificar(("000999000",))


def test_un_fotograma_que_no_es_el_de_f05_se_rechaza(
    criterio: ModuleType, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Extraccion F05 falsa: manifiesto -> sha del indice -> sha de cada PNG. Un byte cambiado en el
    PNG, o un indice que no es el del manifiesto, se rechazan antes de decodificar."""
    import hashlib
    import json

    nombre = criterio.MEDIR[0]
    png = tmp_path / f"{nombre}.png"
    png.write_bytes(b"los bytes que F05 extrajo")
    indice = tmp_path / "index.jsonl"
    fila = {"fichero": f"{nombre}.png", "sha256": hashlib.sha256(png.read_bytes()).hexdigest()}
    indice.write_text(json.dumps(fila) + "\n", encoding="utf-8")
    manifiesto = tmp_path / "fr.yaml"
    sha_indice = hashlib.sha256(indice.read_bytes()).hexdigest()
    manifiesto.write_text(f"sha256_index: {sha_indice}\n", encoding="utf-8")
    monkeypatch.setattr(criterio, "FOTOGRAMAS", tmp_path)
    monkeypatch.setattr(criterio, "MANIFIESTO_F05", manifiesto)

    criterio.verificar((nombre,))  # integro: pasa
    png.write_bytes(b"otros bytes")
    with pytest.raises(criterio.IntegridadError, match="no es el fotograma que extrajo F05"):
        criterio.verificar((nombre,))
    manifiesto.write_text("sha256_index: " + "0" * 64 + "\n", encoding="utf-8")
    with pytest.raises(criterio.IntegridadError, match="index.jsonl no es el que fija"):
        criterio.verificar((nombre,))
