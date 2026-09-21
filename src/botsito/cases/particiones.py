"""Seed y asignacion de casos a particiones (F10, ADR-0011; MASTER_PLAN H "Tres particiones").

Orden determinista e independiente de la version de Python: clave `sha256(f"{seed}:{caso}")`
sobre la lista ordenada de ids; nada de `random.shuffle` (sin garantia entre versiones).
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping, Sequence

PARTICIONES = ("dev", "holdout-1", "holdout-2", "holdout-3")
# El camino de fidelidad (ADR-0036) lleva NOMBRES PROPIOS, y no por estetica: los nombres del kit
# son GLOBALES -`holdout.casos_reservados` agrega sobre todos los paquetes y devuelve un mapa plano
# que tira el paquete, y hay UN solo `AUTORIZACION-<nombre>.md` por nombre-, asi que meter dias NO
# ciegos en `holdout-N` daria un cubo mezclado con los dias ciegos de mayo y una cifra que no se
# puede interpretar (ADR-0034: llamarlo holdout "seria vender por ciego lo que no lo es").
PARTICIONES_FIDELIDAD = ("fidelidad-dev", "fidelidad-1", "fidelidad-2", "fidelidad-3")


class ParticionError(ValueError):
    """La asignacion no se puede hacer con lo pedido."""


def clave_orden(seed: int, caso: str) -> str:
    return hashlib.sha256(f"{seed}:{caso}".encode()).hexdigest()


def asignar(
    casos: Sequence[str],
    seed: int,
    cupos: Mapping[str, int],
    orden: Sequence[str] = PARTICIONES,
) -> dict[str, str]:
    """`caso -> particion`. Los cupos se llenan en el orden de `orden` sobre los casos ordenados
    por su clave; los casos sobrantes no se asignan (quedan fuera del paquete).

    `orden` es el juego de nombres del camino que llama. Por omision, el del kit. El camino de
    fidelidad (ADR-0036) trae los suyos, porque sus dias NO son ciegos y mezclarlos con los del
    kit daria un cubo cuya cifra no se puede interpretar. El ORDEN importa: es el que decide que
    caso cae en que particion, asi que forma parte de lo que `particiones.yaml` reproduce.
    """
    if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
        raise ParticionError("el seed debe ser un entero >= 0")
    if len(set(casos)) != len(casos):
        raise ParticionError("ids de caso repetidos")
    if len(set(orden)) != len(orden) or not orden:
        raise ParticionError("el orden de particiones va sin repetidos y no vacio")
    desconocidas = sorted(set(cupos) - set(orden))
    if desconocidas:
        raise ParticionError(f"particiones desconocidas {desconocidas} (validas: {tuple(orden)})")
    if any(isinstance(v, bool) or not isinstance(v, int) or v < 0 for v in cupos.values()):
        raise ParticionError("cada cupo es un entero >= 0")
    total = sum(cupos.values())
    if total > len(casos):
        raise ParticionError(f"se piden {total} casos y el universo tiene {len(casos)}")
    ordenados = sorted(casos, key=lambda c: (clave_orden(seed, c), c))
    salida: dict[str, str] = {}
    i = 0
    for particion in orden:
        for _ in range(cupos.get(particion, 0)):
            salida[ordenados[i]] = particion
            i += 1
    return salida
