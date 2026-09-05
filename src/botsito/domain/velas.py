"""Vela OHLC del dominio (F15, ADR-0005): enteros en puntos, instante sin `datetime`.

El dominio no importa `datetime` ni usa `float`/`Decimal` fuera de `valores.py`, asi que:
- el inicio de una vela es un `MinutoUtc`: minutos enteros desde 1970-01-01T00:00Z (la capa de
  datos convierte hacia y desde `datetime`; MQL5 usa segundos: `* 60`);
- los precios son `Puntos` (enteros) con la `escala` de la serie (EURUSD: 100000 puntos por
  unidad), el tipo nativo del terminal, sin redondeo fraccion -> puntos (H.2);
- el volumen es un entero con `escala_volumen` de la serie (el proveedor lo da en float).

`escala` y `escala_volumen` no viajan en cada vela: van en `SerieVelas` y en el manifiesto del
dataset. Combinar series con escalas distintas es un error.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import NewType

from botsito.domain.valores import Puntos

MinutoUtc = NewType("MinutoUtc", int)
MINUTOS_POR_DIA = 1440


class VelaInvalidaError(ValueError):
    """Una vela o una serie viola sus invariantes."""


def _entero(valor: object, nombre: str) -> None:
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise VelaInvalidaError(f"{nombre} debe ser un entero, no {type(valor).__name__}")


@dataclass(frozen=True, slots=True)
class Vela:
    """Vela: `inicio` es el minuto UTC de apertura; `duracion_min` la distancia al limite
    siguiente; `n_m1` cuantas M1 la forman; `completa` si su limite de cierre ya paso."""

    inicio: MinutoUtc
    abierta: Puntos
    maxima: Puntos
    minima: Puntos
    cierre: Puntos
    volumen: int
    duracion_min: int = 1
    n_m1: int = 1
    completa: bool = True

    def __post_init__(self) -> None:
        for nombre in ("inicio", "abierta", "maxima", "minima", "cierre", "volumen"):
            _entero(getattr(self, nombre), nombre)
        for nombre in ("duracion_min", "n_m1"):
            _entero(getattr(self, nombre), nombre)
            if getattr(self, nombre) <= 0:
                raise VelaInvalidaError(f"{nombre} debe ser positivo")
        if not isinstance(self.completa, bool):
            raise VelaInvalidaError("completa debe ser booleano")
        if self.volumen < 0:
            raise VelaInvalidaError("volumen negativo")
        if self.inicio < 0:
            raise VelaInvalidaError("inicio anterior a 1970")
        if self.n_m1 > self.duracion_min:
            raise VelaInvalidaError("n_m1 no puede superar la duracion")
        if not (
            self.minima <= self.abierta <= self.maxima and self.minima <= self.cierre <= self.maxima
        ):
            raise VelaInvalidaError(
                f"precios fuera de rango: o={self.abierta} h={self.maxima} "
                f"l={self.minima} c={self.cierre}"
            )

    @property
    def fin(self) -> MinutoUtc:
        """Primer minuto que ya no pertenece a la vela."""
        return MinutoUtc(self.inicio + self.duracion_min)


@dataclass(frozen=True, slots=True)
class SerieVelas:
    """Velas del mismo simbolo, periodo y escalas, en orden ascendente sin solapes."""

    simbolo: str
    periodo_min: int
    escala: int
    escala_volumen: int
    velas: tuple[Vela, ...]
    origen: str | None = None  # dataset_id del que salen (F14 lo cita; F23 lo registra)

    def __post_init__(self) -> None:
        for nombre in ("periodo_min", "escala", "escala_volumen"):
            _entero(getattr(self, nombre), nombre)
            if getattr(self, nombre) <= 0:
                raise VelaInvalidaError(f"{nombre} debe ser positivo")
        if not self.simbolo:
            raise VelaInvalidaError("simbolo vacio")
        for a, b in zip(self.velas, self.velas[1:], strict=False):
            if b.inicio < a.fin:
                raise VelaInvalidaError(f"velas desordenadas o solapadas en {b.inicio}")


def combinar(
    velas: list[Vela], inicio: MinutoUtc, duracion_min: int, completa: bool = True
) -> Vela:
    """Vela de periodo mayor a partir de sus constituyentes, ya en orden ascendente.

    Puro: no decide que velas entran (eso es la agregacion con anclaje); solo las funde.
    """
    if not velas:
        raise VelaInvalidaError("no se puede combinar una lista vacia")
    for a, b in zip(velas, velas[1:], strict=False):
        if b.inicio < a.fin:
            raise VelaInvalidaError(f"velas desordenadas o solapadas en {b.inicio}")
    if velas[0].inicio < inicio or velas[-1].fin > inicio + duracion_min:
        raise VelaInvalidaError("una vela constituyente cae fuera del periodo")
    return Vela(
        inicio=inicio,
        abierta=velas[0].abierta,
        maxima=Puntos(max(v.maxima for v in velas)),
        minima=Puntos(min(v.minima for v in velas)),
        cierre=velas[-1].cierre,
        volumen=sum(v.volumen for v in velas),
        duracion_min=duracion_min,
        n_m1=sum(v.n_m1 for v in velas),
        completa=completa,
    )
