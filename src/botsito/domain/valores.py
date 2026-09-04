"""Tipos de valor del dominio: fracciones y porcentajes que no se mezclan.

Un 0,5 % de riesgo escrito como 0,5 en vez de 0,005 es un error de factor 100. Aqui un
`Porcentaje` y una `Fraccion` son tipos distintos: no se suman, no se comparan y solo se
convierten de forma explicita. Los valores son `Decimal`; un `float` se rechaza en la entrada.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Self

CIEN = Decimal(100)


def _a_decimal(valor: Decimal | int | str) -> Decimal:
    if isinstance(valor, bool | float):
        raise TypeError("float y bool no son valores admitidos; usa Decimal, int o str")
    try:
        resultado = valor if isinstance(valor, Decimal) else Decimal(valor)
    except InvalidOperation as exc:
        raise ValueError(f"valor decimal invalido: {valor!r}") from exc
    if not resultado.is_finite():
        raise ValueError(f"valor no finito: {valor!r}")
    return resultado


@dataclass(frozen=True, slots=True)
class Fraccion:
    """Proporcion sobre 1: 0,75 significa tres cuartos."""

    valor: Decimal

    def __init__(self, valor: Decimal | int | str) -> None:
        object.__setattr__(self, "valor", _a_decimal(valor))

    def __add__(self, otro: Self) -> Fraccion:
        _misma_clase(self, otro)
        return Fraccion(self.valor + otro.valor)

    def __sub__(self, otro: Self) -> Fraccion:
        _misma_clase(self, otro)
        return Fraccion(self.valor - otro.valor)

    def __lt__(self, otro: Self) -> bool:
        _misma_clase(self, otro)
        return self.valor < otro.valor

    def __le__(self, otro: Self) -> bool:
        _misma_clase(self, otro)
        return self.valor <= otro.valor

    def como_porcentaje(self) -> Porcentaje:
        return Porcentaje(self.valor * CIEN)

    def __str__(self) -> str:
        return f"{self.valor} (fraccion)"


@dataclass(frozen=True, slots=True)
class Porcentaje:
    """Proporcion sobre 100: 0,5 significa medio punto porcentual."""

    valor: Decimal

    def __init__(self, valor: Decimal | int | str) -> None:
        object.__setattr__(self, "valor", _a_decimal(valor))

    def __add__(self, otro: Self) -> Porcentaje:
        _misma_clase(self, otro)
        return Porcentaje(self.valor + otro.valor)

    def __sub__(self, otro: Self) -> Porcentaje:
        _misma_clase(self, otro)
        return Porcentaje(self.valor - otro.valor)

    def __lt__(self, otro: Self) -> bool:
        _misma_clase(self, otro)
        return self.valor < otro.valor

    def __le__(self, otro: Self) -> bool:
        _misma_clase(self, otro)
        return self.valor <= otro.valor

    def como_fraccion(self) -> Fraccion:
        return Fraccion(self.valor / CIEN)

    def __str__(self) -> str:
        return f"{self.valor} %"


def _misma_clase(a: object, b: object) -> None:
    if type(a) is not type(b):
        raise TypeError(
            f"no se puede operar {type(a).__name__} con {type(b).__name__}: "
            "convierte explicitamente con como_fraccion() o como_porcentaje()"
        )


@dataclass(frozen=True, slots=True)
class HoraLocal:
    """Hora de reloj `HH:MM` en un huso IANA concreto (ADR-0004).

    Una hora sin huso no significa nada en un sistema con tres relojes (trader en Madrid, servidor
    del broker, datos en UTC). El dominio no resuelve el huso (no importa `datetime`): lo hace la
    capa de datos o el motor con `zoneinfo`; aqui solo viaja junto a la hora.
    """

    hora: str
    huso: str

    @property
    def minutos_del_dia(self) -> int:
        hh, mm = self.hora.split(":")
        return int(hh) * 60 + int(mm)

    def __str__(self) -> str:
        return f"{self.hora} {self.huso}"
