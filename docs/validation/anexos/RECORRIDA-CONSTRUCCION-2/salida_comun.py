"""Lo que comparten `caja_stop.py` y `visor_sesiones.py` (fase 3 de trabajo/recorrida-construccion-2),
sin importar ningun otro guion de la carpeta: asi la cadena de carga desde `test_humo.py` cabe en
los tres niveles que admite la guardia de Claude Code (GUION-MISMO-COMANDO.md §0.c; la negativa a
`test_humo.py` con `caja_stop` importando `para_clasificar`, medida el 2026-11-08). Solo lee texto.

La direccion de una orden se lee como en `para_clasificar.leer_salida`: la de su posicion si se
lleno; si no, la de su caja (el 1 de la caja por encima del precio, venta; por debajo, compra). Un
test de `test_humo.py` comprueba que las dos lecturas dan lo mismo.
"""

# ruff: noqa: E501  (textos y tablas literales: el docstring explica las columnas)

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from fractions import Fraction

ESCALA = 100_000
ROTULO = "[DIAGNOSTICO"
DOS_TERCIOS = Fraction(2, 3)


@dataclass(frozen=True)
class OrdenBot:
    dia: str
    sesion: str
    id: str
    direccion: str | None
    colocada: str  # ISO UTC
    precio: Decimal
    stop: Decimal | None  # None sin direccion
    resultado: str
    motivo: str
    instante: str  # ISO UTC del resultado


def cuerpo(ln: str) -> str:
    return ln.split("] ", 1)[1] if ln.startswith(ROTULO) and "] " in ln else ln


def seccion(lineas: list[str], empieza: str, acaba: str) -> list[str]:
    for i, ln in enumerate(lineas):
        if ln.startswith(empieza):
            salida = []
            for fila in lineas[i + 1 :]:
                if fila.startswith(acaba):
                    break
                salida.append(fila)
            return [f for f in salida if f and f not in ("ninguna", "ninguno")]
    return []


def lado_de_caja(precio: Decimal, caja: str) -> str | None:
    if caja == "-":
        return None
    c = Decimal(caja)
    return "venta" if c > precio else "compra" if c < precio else None


def stop_de(precio: Decimal, distancia_puntos: int, direccion: str | None) -> Decimal | None:
    """El stop de una orden desde su precio y su distancia en puntos: por debajo en una compra, por
    encima en una venta."""
    if direccion is None:
        return None
    d = Decimal(distancia_puntos) / ESCALA
    return precio - d if direccion == "compra" else precio + d


def hacia_el_stop(direccion: str, bot: Decimal, trader: Decimal) -> int:
    """Puntos con signo: > 0 si `bot` esta mas del lado del stop que `trader` (compra: abajo)."""
    d = (trader - bot) if direccion == "compra" else (bot - trader)
    return int(d * ESCALA)


def cociente(entrada_b: Decimal, stop_b: Decimal, entrada_t: Decimal, stop_t: Decimal) -> Fraction:
    return Fraction(abs(entrada_b - stop_b)) / Fraction(abs(entrada_t - stop_t))


def clase(signos: list[int]) -> tuple[str, int, int, int]:
    """(SISTEMATICA o DISPERSA, positivos, negativos, ceros) por la regla de los dos tercios."""
    pos = sum(1 for s in signos if s > 0)
    neg = sum(1 for s in signos if s < 0)
    ceros = len(signos) - pos - neg
    if not signos:
        return "sin filas", pos, neg, ceros
    regla = Fraction(max(pos, neg), len(signos)) >= DOS_TERCIOS
    return ("SISTEMATICA" if regla else "DISPERSA"), pos, neg, ceros


def cierre(hhmmss: str) -> str:
    """El cierre de M1 en que se coloca una orden: su hora (que acaba en :59) mas un segundo."""
    return (datetime.strptime(hhmmss, "%H:%M:%S") + timedelta(seconds=1)).strftime("%H:%M:%S")


def posiciones_de(texto: str) -> list[list[str]]:
    lineas = [cuerpo(ln) for ln in texto.splitlines()]
    return [f.split(" | ") for f in seccion(lineas, "### Posiciones (dia", "posiciones: ")]


def ordenes_de(texto: str) -> dict[tuple[str, str], OrdenBot]:
    """Cada fila de «### Ordenes», con su direccion (la de su posicion, o la de su caja) y su stop."""
    lineas = [cuerpo(ln) for ln in texto.splitlines()]
    lado_pos = {(c[0], c[3]): c[4] for c in posiciones_de(texto)}
    ordenes: dict[tuple[str, str], OrdenBot] = {}
    for fila in seccion(lineas, "### Ordenes (dia", "ordenes: "):
        c = fila.split(" | ")
        dia, sesion, oid, colocada, precio = c[0], c[1], c[2], c[3], Decimal(c[4])
        d = lado_pos.get((dia, oid)) or lado_de_caja(precio, c[16])
        ordenes[(dia, oid)] = OrdenBot(
            dia, sesion, oid, d, colocada, precio, stop_de(precio, int(c[9]), d), c[5], c[6], c[7]
        )
    return ordenes
