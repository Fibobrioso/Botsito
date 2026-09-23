"""El decodificador de PNG de `scripts/` (Next Action 4, 2026-09-23).

El test FABRICA SUS PROPIOS PNG: `data/fotogramas/**` esta fuera de git. Y el codificador de aqui
aplica los cinco filtros con una implementacion PROPIA, escrita por separado, porque un filtro mal
implementado no revienta: da una medida ligeramente falsa con cara de exacta. Si el decodificador y
el test compartieran la funcion, un error comun se cancelaria y el test pasaria igual.
"""

from __future__ import annotations

import importlib.util
import struct
import sys
import zlib
from pathlib import Path
from types import ModuleType

import pytest

RUTA = Path(__file__).resolve().parents[2] / "scripts" / "decodificar_png.py"


def _modulo() -> ModuleType:
    """Cargado por ruta, como `scripts/mover_sesion.py` en `test_kit.py`. Se REGISTRA en
    `sys.modules` antes de ejecutarlo: `dataclass` busca ahi su modulo, y sin registrar falla."""
    if "decodificar_png" in sys.modules:
        return sys.modules["decodificar_png"]
    spec = importlib.util.spec_from_file_location("decodificar_png", RUTA)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules["decodificar_png"] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def _chunk(tipo: bytes, datos: bytes) -> bytes:
    crc = zlib.crc32(tipo + datos) & 0xFFFFFFFF
    return struct.pack(">I", len(datos)) + tipo + datos + struct.pack(">I", crc)


def _predictor_paeth(a: int, b: int, c: int) -> int:
    # Escrito aqui a proposito, con la formula del estandar tal cual, sin mirar el decodificador.
    estimado = a + b - c
    distancias = [abs(estimado - a), abs(estimado - b), abs(estimado - c)]
    if distancias[0] <= distancias[1] and distancias[0] <= distancias[2]:
        return a
    if distancias[1] <= distancias[2]:
        return b
    return c


def _filtrar(fila: bytes, previa: bytes, bpp: int, tipo: int) -> bytes:
    salida = bytearray()
    for i, x in enumerate(fila):
        izq = fila[i - bpp] if i >= bpp else 0
        arr = previa[i]
        diag = previa[i - bpp] if i >= bpp else 0
        pred = {
            0: 0,
            1: izq,
            2: arr,
            3: (izq + arr) // 2,
            4: _predictor_paeth(izq, arr, diag),
        }[tipo]
        salida.append((x - pred) % 256)
    return bytes([tipo]) + bytes(salida)


def _png(
    pixeles: list[list[tuple[int, ...]]], color: int, filtros: list[int], trozos: int = 1
) -> bytes:
    alto, ancho = len(pixeles), len(pixeles[0])
    bpp = len(pixeles[0][0])
    crudo = bytearray()
    previa = bytes(ancho * bpp)
    for y, fila in enumerate(pixeles):
        bytes_fila = bytes(v for p in fila for v in p)
        crudo += _filtrar(bytes_fila, previa, bpp, filtros[y % len(filtros)])
        previa = bytes_fila
    comprimido = zlib.compress(bytes(crudo))
    paso = max(1, len(comprimido) // trozos + 1)
    idats = b"".join(
        _chunk(b"IDAT", comprimido[i : i + paso]) for i in range(0, len(comprimido), paso)
    )
    ihdr = struct.pack(">IIBBBBB", ancho, alto, 8, color, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", ihdr) + idats + _chunk(b"IEND", b"")


def _imagen(ancho: int, alto: int, canales: int) -> list[list[tuple[int, ...]]]:
    """Pixeles deterministas y variados: gradientes, saltos bruscos y valores cerca de 0 y 255,
    que es donde un filtro mal hecho desborda."""
    return [
        [
            tuple(
                (x * 37 + y * 91 + c * 53 + (x * y) % 17 + (250 if (x + y + c) % 7 == 0 else 0))
                % 256
                for c in range(canales)
            )
            for x in range(ancho)
        ]
        for y in range(alto)
    ]


@pytest.mark.parametrize("filtro", [0, 1, 2, 3, 4], ids=["None", "Sub", "Up", "Average", "Paeth"])
@pytest.mark.parametrize(("color", "canales"), [(2, 3), (6, 4), (0, 1)])
def test_cada_filtro_devuelve_los_pixeles_exactos(filtro: int, color: int, canales: int) -> None:
    png = _modulo()
    esperado = _imagen(13, 9, canales)
    imagen = png.decodificar(_png(esperado, color, [filtro]))
    assert (imagen.ancho, imagen.alto, imagen.canales) == (13, 9, canales)
    for y in range(9):
        for x in range(13):
            assert imagen.pixel(x, y) == esperado[y][x], (filtro, x, y)


def test_filtros_mezclados_linea_a_linea_y_varios_idat() -> None:
    """Cada linea con un filtro distinto -el caso real de un PNG de ffmpeg- y el IDAT partido."""
    png = _modulo()
    esperado = _imagen(20, 15, 3)
    imagen = png.decodificar(_png(esperado, 2, [0, 1, 2, 3, 4, 4, 3, 2, 1], trozos=4))
    assert [[imagen.pixel(x, y) for x in range(20)] for y in range(15)] == esperado


def test_un_crc_roto_se_rechaza() -> None:
    png = _modulo()
    datos = bytearray(_png(_imagen(4, 4, 3), 2, [4]))
    datos[-20] ^= 0xFF  # dentro del ultimo IDAT, antes del IEND
    with pytest.raises(png.PngError, match="CRC"):
        png.decodificar(bytes(datos))


def test_lo_que_no_admite_se_rechaza_y_no_se_adivina() -> None:
    png = _modulo()
    entrelazado = struct.pack(">IIBBBBB", 2, 2, 8, 2, 0, 0, 1)
    fichero = b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", entrelazado) + _chunk(b"IEND", b"")
    with pytest.raises(png.PngError, match="IHDR no admitido"):
        png.decodificar(fichero)
    with pytest.raises(png.PngError, match="firma"):
        png.decodificar(b"no soy un png")


def test_el_pixel_fuera_de_la_imagen_es_error() -> None:
    png = _modulo()
    imagen = png.decodificar(_png(_imagen(3, 3, 3), 2, [0]))
    with pytest.raises(IndexError):
        imagen.pixel(3, 0)


def test_solo_usa_zlib_y_struct() -> None:
    """Condicion (c) del punto 4: cero dependencias nuevas."""
    import ast

    arbol = ast.parse(RUTA.read_text(encoding="utf-8"))
    importados = {
        n.names[0].name.split(".")[0]
        if isinstance(n, ast.Import)
        else (n.module or "").split(".")[0]
        for n in ast.walk(arbol)
        if isinstance(n, ast.Import | ast.ImportFrom)
    }
    assert importados <= {"__future__", "struct", "sys", "zlib", "dataclasses", "pathlib"}
