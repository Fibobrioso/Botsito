"""Los cierres de mercado y la ventana que FTMO prohibe antes de uno largo (ADR-0068).

R15 de `docs/validation/FTMO-REGLAS.md` prohibe «perform gap trading [...] by opening simulated
trades: [...] two hours or less before a relevant financial market is closed for at least two
hours». Aqui vive el PREDICADO UNICO que lo decide, `ventana_prohibida_por_cierre`: el broker le
pregunta antes de colocar o de mover una pendiente, asi que ninguna regla de la estrategia puede
saltarselo (el mismo sitio que el freno de peticiones, ADR-0067).

Todo va en instantes absolutos (milisegundos UTC): la ventana es una DURACION antes del instante en
que empieza el cierre, y nunca depende de un reloj de pared. El reloj solo entra al convertir la
hora declarada de un cierre en un instante, y eso lo hace quien construye el calendario
(`engine/calendario_cierres.py`), con el huso que declara cada entrada. Sin IO ni reloj propio, y
sin cifras: el margen y el minimo los da el perfil de la firma (ADR-0002).
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass

MOTIVO_CIERRE = "cierre_mercado"
MOTIVO_SIN_CALENDARIO = "cierre_sin_calendario"
MOTIVOS_DE_CIERRE = (MOTIVO_CIERRE, MOTIVO_SIN_CALENDARIO)


class CierresError(ValueError):
    """Un calendario o unas sesiones que no tienen sentido: no se adivina."""


@dataclass(frozen=True)
class Cierre:
    """Un tramo con el mercado cerrado, [inicio, fin), y de donde sale."""

    inicio_ms: int
    fin_ms: int
    fuente: str

    def __post_init__(self) -> None:
        if self.fin_ms <= self.inicio_ms:
            raise CierresError(f"un cierre acaba despues de empezar ({self.fuente})")

    @property
    def duracion_ms(self) -> int:
        return self.fin_ms - self.inicio_ms


@dataclass(frozen=True)
class CalendarioCierres:
    """Los cierres conocidos, ya unidos, y el tramo [desde, hasta) que el calendario cubre."""

    cierres: tuple[Cierre, ...]
    cubre_desde_ms: int
    cubre_hasta_ms: int

    def __post_init__(self) -> None:
        if self.cubre_hasta_ms <= self.cubre_desde_ms:
            raise CierresError("el calendario no cubre nada")
        if list(self.cierres) != sorted(self.cierres, key=lambda c: c.inicio_ms):
            raise CierresError("los cierres van en orden")
        for a, b in zip(self.cierres, self.cierres[1:], strict=False):
            if b.inicio_ms <= a.fin_ms:
                raise CierresError("los cierres van unidos: dos se tocan o se pisan")


@dataclass(frozen=True)
class ReglasCierres:
    """Lo que el broker necesita para el predicado: el calendario, el margen y el minimo de la
    firma (R15) y que hacer con una pendiente al empezar la ventana (PROVISIONAL bajo A-55)."""

    calendario: CalendarioCierres
    margen_ms: int
    minimo_ms: int
    cancelar_pendientes: bool


@dataclass(frozen=True)
class Prohibicion:
    """Por que no se abre ni se coloca en un instante: el motivo, y el cierre y el inicio de su
    ventana cuando es un cierre."""

    motivo: str
    cierre: Cierre | None = None
    ventana_desde_ms: int | None = None


def ventana_prohibida_por_cierre(
    instante_ms: int, calendario: CalendarioCierres, margen_ms: int, minimo_ms: int
) -> Prohibicion | None:
    """None si en `instante_ms` se puede abrir o colocar; si no, la prohibicion.

    Prohibido: desde `margen_ms` antes de un cierre de `minimo_ms` o mas hasta que acaba (los dos
    bordes de R15 dentro: «two hours or less», «at least two hours»; con el mercado cerrado tampoco
    se coloca), y fuera del tramo que cubre el calendario, donde no se sabe (abstenerse)."""
    if margen_ms <= 0 or minimo_ms <= 0:
        raise CierresError("el margen y el minimo son duraciones positivas")
    if not calendario.cubre_desde_ms <= instante_ms < calendario.cubre_hasta_ms:
        return Prohibicion(MOTIVO_SIN_CALENDARIO)
    for c in calendario.cierres:
        if c.inicio_ms - margen_ms > instante_ms:
            break
        if c.duracion_ms >= minimo_ms and instante_ms < c.fin_ms:
            return Prohibicion(MOTIVO_CIERRE, c, c.inicio_ms - margen_ms)
    return None


def proxima_prohibicion(
    desde_ms: int, hasta_ms: int, calendario: CalendarioCierres, margen_ms: int, minimo_ms: int
) -> int | None:
    """El primer instante de (desde, hasta] en que empieza una prohibicion que en `desde` no
    habia: el inicio de una ventana o el fin de lo que cubre el calendario. None si no hay."""
    candidatos = [
        c.inicio_ms - margen_ms
        for c in calendario.cierres
        if c.duracion_ms >= minimo_ms and desde_ms < c.inicio_ms - margen_ms <= hasta_ms
    ]
    if desde_ms < calendario.cubre_hasta_ms <= hasta_ms:
        candidatos.append(calendario.cubre_hasta_ms)
    return min(candidatos, default=None)


def cierres_desde_sesiones(sesiones: Iterable[tuple[int, int]], fuente: str) -> tuple[Cierre, ...]:
    """Los huecos entre sesiones de negociacion [inicio, fin) ya en instantes: lo que da la
    plataforma en vivo (las sesiones del simbolo en MT5, o las de la API de la firma)."""
    ordenadas = sorted(sesiones)
    for inicio, fin in ordenadas:
        if fin <= inicio:
            raise CierresError(f"una sesion de {fuente} acaba antes de empezar")
    return tuple(
        Cierre(a_fin, b_inicio, fuente)
        for (_, a_fin), (b_inicio, _) in zip(ordenadas, ordenadas[1:], strict=False)
        if b_inicio > a_fin
    )


def juntar_cierres(cierres: Iterable[Cierre]) -> tuple[Cierre, ...]:
    """Los cierres en orden, con los que se tocan o se pisan hechos uno (las fuentes, juntas)."""
    salida: list[Cierre] = []
    for c in sorted(cierres, key=lambda x: (x.inicio_ms, x.fin_ms)):
        if salida and c.inicio_ms <= salida[-1].fin_ms:
            u = salida[-1]
            fuentes = u.fuente.split(" + ")
            fuente = u.fuente if c.fuente in fuentes else f"{u.fuente} + {c.fuente}"
            salida[-1] = Cierre(u.inicio_ms, max(u.fin_ms, c.fin_ms), fuente)
        else:
            salida.append(c)
    return tuple(salida)


@dataclass(frozen=True)
class FuenteCierres:
    """Los cierres que da una fuente y el tramo [desde, hasta) del que sabe algo."""

    nombre: str
    cierres: tuple[Cierre, ...]
    desde_ms: int
    hasta_ms: int


@dataclass(frozen=True)
class Discrepancia:
    """Un cierre largo de una fuente que empieza con el mercado ABIERTO en otra que si sabe de ese
    instante."""

    cierre: Cierre
    de: str
    falta_en: str


def unir_cierres(
    fuentes: Sequence[FuenteCierres], minimo_ms: int
) -> tuple[tuple[Cierre, ...], tuple[Discrepancia, ...]]:
    """Gana la MAS RESTRICTIVA: la union de los cierres de todas las fuentes. Y, como
    discrepancia, cada cierre largo de una fuente que empieza dentro del tramo de otra sin que esa
    otra tenga el mercado cerrado en ese instante."""
    juntas = [(f, juntar_cierres(f.cierres)) for f in fuentes]
    discrepancias = [
        Discrepancia(c, f.nombre, g.nombre)
        for f, cs in juntas
        for c in cs
        if c.duracion_ms >= minimo_ms
        for g, ds in juntas
        if g.nombre != f.nombre
        and g.desde_ms <= c.inicio_ms < g.hasta_ms
        and not any(d.inicio_ms <= c.inicio_ms < d.fin_ms for d in ds)
    ]
    return juntar_cierres(c for _, cs in juntas for c in cs), tuple(discrepancias)


__all__ = [
    "MOTIVOS_DE_CIERRE",
    "MOTIVO_CIERRE",
    "MOTIVO_SIN_CALENDARIO",
    "CalendarioCierres",
    "Cierre",
    "CierresError",
    "Discrepancia",
    "FuenteCierres",
    "Prohibicion",
    "ReglasCierres",
    "cierres_desde_sesiones",
    "juntar_cierres",
    "proxima_prohibicion",
    "unir_cierres",
    "ventana_prohibida_por_cierre",
]
