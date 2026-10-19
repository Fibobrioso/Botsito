"""Las sesiones cuyas ordenes («### Ordenes») cambian entre dos salidas del arnes: por sesion,
cuantas ordenes de cada resultado hay en cada una, solo las que difieren. Solo lee."""

from __future__ import annotations

import sys
from collections import Counter, defaultdict
from pathlib import Path


def _sin_etiquetas(linea: str) -> str:
    texto = linea
    while texto.startswith("["):
        texto = texto.split("] ", 1)[-1]
    return texto


def por_sesion(ruta: Path) -> dict[tuple[str, str], Counter[str]]:
    dentro = False
    salida: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        texto = _sin_etiquetas(linea)
        if texto.startswith("### Ordenes (dia"):
            dentro = True
            continue
        if dentro and texto.startswith("### "):
            break
        if dentro and texto.count(" | ") >= 14:
            f = [c.strip() for c in texto.split(" | ")]
            salida[(f[0], f[1])][f[5]] += 1
    return salida


a, b = por_sesion(Path(sys.argv[1])), por_sesion(Path(sys.argv[2]))
n = 0
for clave in sorted(set(a) | set(b)):
    if a.get(clave) != b.get(clave):
        n += 1
        antes, despues = dict(a.get(clave, {})), dict(b.get(clave, {}))
        print(f"{clave[0]} {clave[1]} | antes {antes} | despues {despues}")
print(f"sesiones que cambian: {n}")
