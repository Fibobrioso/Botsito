"""Tick del dominio (rama `trabajo/ticks-llenado`, ADR-0051): enteros, sin `datetime`.

Un tick es una cotizacion en un instante: BID y ASK en puntos de la serie (la escala va en la
serie, como en las velas) y los volumenes en milesimas. El instante son MILISEGUNDOS UTC desde
1970-01-01T00:00Z, enteros, porque el proveedor da milisegundos dentro de la hora; el minuto UTC
de las velas es `ms // 60000`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import NewType

from botsito.domain.valores import Puntos
from botsito.domain.velas import MinutoUtc

MilisegundoUtc = NewType("MilisegundoUtc", int)
MS_POR_MINUTO = 60_000


class TickInvalidoError(ValueError):
    """Un tick viola sus invariantes."""


@dataclass(frozen=True, slots=True)
class Tick:
    instante: MilisegundoUtc
    ask: Puntos
    bid: Puntos
    volumen_ask: int  # milesimas
    volumen_bid: int  # milesimas

    def __post_init__(self) -> None:
        for nombre in ("instante", "ask", "bid", "volumen_ask", "volumen_bid"):
            valor = getattr(self, nombre)
            if isinstance(valor, bool) or not isinstance(valor, int):
                raise TickInvalidoError(f"{nombre} debe ser un entero")
        if self.instante < 0:
            raise TickInvalidoError("instante anterior a 1970")
        if self.ask <= 0 or self.bid <= 0:
            raise TickInvalidoError("precio no positivo")
        if self.volumen_ask < 0 or self.volumen_bid < 0:
            raise TickInvalidoError("volumen negativo")

    @property
    def minuto(self) -> MinutoUtc:
        return MinutoUtc(self.instante // MS_POR_MINUTO)

    @property
    def spread(self) -> int:
        """ASK menos BID, en puntos. Puede ser negativo en una cotizacion cruzada: se conserva."""
        return int(self.ask) - int(self.bid)


__all__ = ["MS_POR_MINUTO", "MilisegundoUtc", "Tick", "TickInvalidoError"]
