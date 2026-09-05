"""Husos horarios por nombre IANA canonico, con un solo criterio para registro y datos.

`ZoneInfo("Europe/madrid")` resuelve en Windows (sistema de ficheros sin mayusculas) y falla en
Linux: un parametro aceptado en una maquina y rechazado en otra es un error de reproducibilidad.
Aqui se exige el nombre exacto de `available_timezones()`.
"""

from __future__ import annotations

from zoneinfo import ZoneInfo, ZoneInfoNotFoundError, available_timezones

_CONOCIDOS: frozenset[str] = frozenset()


class HusoDesconocidoError(ValueError):
    """El nombre no es un huso IANA canonico."""


def huso_canonico(nombre: object) -> ZoneInfo:
    global _CONOCIDOS
    if not _CONOCIDOS:
        _CONOCIDOS = frozenset(available_timezones())
    if not isinstance(nombre, str) or nombre not in _CONOCIDOS:
        raise HusoDesconocidoError(f"huso desconocido {nombre!r} (nombre IANA exacto)")
    try:
        return ZoneInfo(nombre)
    except (ZoneInfoNotFoundError, ValueError) as exc:  # pragma: no cover - tzdata ausente
        raise HusoDesconocidoError(f"huso desconocido {nombre!r}") from exc
