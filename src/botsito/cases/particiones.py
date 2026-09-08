"""Seed y asignacion de casos a particiones (F10, ADR-0011; MASTER_PLAN H "Tres particiones").

Orden determinista e independiente de la version de Python: clave `sha256(f"{seed}:{caso}")`
sobre la lista ordenada de ids; nada de `random.shuffle` (sin garantia entre versiones).
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping, Sequence

PARTICIONES = ("dev", "holdout-1", "holdout-2", "holdout-3")


class ParticionError(ValueError):
    """La asignacion no se puede hacer con lo pedido."""


def clave_orden(seed: int, caso: str) -> str:
    return hashlib.sha256(f"{seed}:{caso}".encode()).hexdigest()


def asignar(casos: Sequence[str], seed: int, cupos: Mapping[str, int]) -> dict[str, str]:
    """`caso -> particion`. Los cupos se llenan en el orden de PARTICIONES sobre los casos
    ordenados por su clave; los casos sobrantes no se asignan (quedan fuera del paquete)."""
    if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
        raise ParticionError("el seed debe ser un entero >= 0")
    if len(set(casos)) != len(casos):
        raise ParticionError("ids de caso repetidos")
    desconocidas = sorted(set(cupos) - set(PARTICIONES))
    if desconocidas:
        raise ParticionError(f"particiones desconocidas {desconocidas} (validas: {PARTICIONES})")
    if any(isinstance(v, bool) or not isinstance(v, int) or v < 0 for v in cupos.values()):
        raise ParticionError("cada cupo es un entero >= 0")
    total = sum(cupos.values())
    if total > len(casos):
        raise ParticionError(f"se piden {total} casos y el universo tiene {len(casos)}")
    ordenados = sorted(casos, key=lambda c: (clave_orden(seed, c), c))
    salida: dict[str, str] = {}
    i = 0
    for particion in PARTICIONES:
        for _ in range(cupos.get(particion, 0)):
            salida[ordenados[i]] = particion
            i += 1
    return salida
