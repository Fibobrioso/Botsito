"""Decodificador de PNG de biblioteca estandar: solo `zlib` y `struct` (Next Action 4, 2026-09-23).

Es una HERRAMIENTA DE MEDIDA, no parte del paquete: `pyproject.toml` no se toca y nada de
`botsito` lo importa. Mide pixeles de los fotogramas de `data/fotogramas/**`, que estan fuera de
git; por eso su test fabrica sus propios PNG.

Lo que hace, y nada mas: firma, chunks con su CRC, IHDR, todos los IDAT concatenados y
descomprimidos con `zlib`, y deshacer el filtro de cada linea -None, Sub, Up, Average, Paeth-.
Admite profundidad 8 y color gris (0), RGB (2), gris+alfa (4) y RGBA (6), sin entrelazado. Lo que
no admite lo rechaza con error: **un filtro mal implementado no revienta, da una medida
ligeramente falsa con cara de exacta**, asi que aqui nada se adivina.

Uso: `uv run python scripts/decodificar_png.py <fichero.png>` imprime `ANCHOxALTO, N canales`.
"""

from __future__ import annotations

import struct
import sys
import zlib
from dataclasses import dataclass
from pathlib import Path

FIRMA = b"\x89PNG\r\n\x1a\n"
CANALES = {0: 1, 2: 3, 4: 2, 6: 4}


class PngError(ValueError):
    """El fichero no es un PNG que este decodificador sepa leer."""


@dataclass(frozen=True)
class Imagen:
    ancho: int
    alto: int
    canales: int
    pixeles: bytes  # fila a fila, `canales` bytes por pixel, sin byte de filtro

    def pixel(self, x: int, y: int) -> tuple[int, ...]:
        if not (0 <= x < self.ancho and 0 <= y < self.alto):
            raise IndexError(f"({x}, {y}) fuera de {self.ancho}x{self.alto}")
        i = (y * self.ancho + x) * self.canales
        return tuple(self.pixeles[i : i + self.canales])


def _paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    return b if pb <= pc else c


def _desfiltrar(datos: bytes, ancho: int, alto: int, bpp: int) -> bytes:
    stride = ancho * bpp
    if len(datos) != alto * (stride + 1):
        raise PngError(
            f"IDAT descomprimido mide {len(datos)} y deberia medir {alto * (stride + 1)}"
        )
    salida = bytearray()
    previa = bytearray(stride)
    for y in range(alto):
        inicio = y * (stride + 1)
        filtro = datos[inicio]
        fila = bytearray(datos[inicio + 1 : inicio + 1 + stride])
        for i in range(stride):
            a = fila[i - bpp] if i >= bpp else 0
            b = previa[i]
            c = previa[i - bpp] if i >= bpp else 0
            if filtro == 0:
                continue
            if filtro == 1:
                fila[i] = (fila[i] + a) & 0xFF
            elif filtro == 2:
                fila[i] = (fila[i] + b) & 0xFF
            elif filtro == 3:
                fila[i] = (fila[i] + (a + b) // 2) & 0xFF
            elif filtro == 4:
                fila[i] = (fila[i] + _paeth(a, b, c)) & 0xFF
            else:
                raise PngError(f"linea {y}: tipo de filtro {filtro} desconocido")
        salida += fila
        previa = fila
    return bytes(salida)


def decodificar(contenido: bytes) -> Imagen:
    if not contenido.startswith(FIRMA):
        raise PngError("no empieza por la firma PNG")
    pos = len(FIRMA)
    ihdr: tuple[int, int, int, int, int] | None = None
    idat = bytearray()
    while pos < len(contenido):
        if pos + 8 > len(contenido):
            raise PngError("chunk truncado")
        (longitud,) = struct.unpack(">I", contenido[pos : pos + 4])
        tipo = contenido[pos + 4 : pos + 8]
        datos = contenido[pos + 8 : pos + 8 + longitud]
        (crc,) = struct.unpack(">I", contenido[pos + 8 + longitud : pos + 12 + longitud])
        if zlib.crc32(tipo + datos) & 0xFFFFFFFF != crc:
            raise PngError(f"CRC incorrecto en el chunk {tipo!r}")
        if tipo == b"IHDR":
            ancho, alto, prof, color, comp, filt, entre = struct.unpack(">IIBBBBB", datos)
            if prof != 8 or color not in CANALES or comp != 0 or filt != 0 or entre != 0:
                raise PngError(
                    f"IHDR no admitido: profundidad {prof}, color {color}, entrelazado {entre}"
                )
            ihdr = (ancho, alto, prof, color, entre)
        elif tipo == b"IDAT":
            idat += datos
        elif tipo == b"IEND":
            break
        pos += 12 + longitud
    if ihdr is None:
        raise PngError("sin IHDR")
    ancho, alto, _, color, _ = ihdr
    canales = CANALES[color]
    try:
        crudo = zlib.decompress(bytes(idat))
    except zlib.error as exc:
        raise PngError(f"IDAT no descomprime: {exc}") from exc
    return Imagen(ancho, alto, canales, _desfiltrar(crudo, ancho, alto, canales))


def leer(ruta: Path) -> Imagen:
    return decodificar(ruta.read_bytes())


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("uso: decodificar_png.py <fichero.png>", file=sys.stderr)
        return 2
    imagen = leer(Path(argv[1]))
    print(f"{imagen.ancho}x{imagen.alto}, {imagen.canales} canales")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
