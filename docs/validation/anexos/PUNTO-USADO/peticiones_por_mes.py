"""Suma por mes la tabla «### Peticiones al servidor» de una o varias salidas del arnes (total,
colocar, modificar, cancelar, cerrar, rechazadas) y el dia con mas peticiones. Solo lee."""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path


def _sin_etiquetas(linea: str) -> str:
    texto = linea
    while texto.startswith("["):
        texto = texto.split("] ", 1)[-1]
    return texto


def resumen(ruta: Path) -> None:
    dentro = False
    por_mes: dict[str, list[int]] = defaultdict(lambda: [0] * 6)
    peor = ("", 0)
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        texto = _sin_etiquetas(linea)
        if texto.startswith("### Peticiones al servidor"):
            dentro = True
            continue
        if dentro and texto.startswith("### "):
            break
        if dentro and texto[:4].isdigit() and texto.count(" | ") == 6:
            dia, *nums = [c.strip() for c in texto.split(" | ")]
            vals = [int(n) for n in nums]
            acum = por_mes[dia[:7]]
            for k, v in enumerate(vals):
                acum[k] += v
            if vals[0] > peor[1]:
                peor = (dia, vals[0])
    print(ruta.name[:40])
    print("  mes | total | colocar | modificar | cancelar | cerrar | rechazadas")
    tot = [0] * 6
    for mes in sorted(por_mes):
        print(f"  {mes} | " + " | ".join(str(v) for v in por_mes[mes]))
        tot = [a + b for a, b in zip(tot, por_mes[mes], strict=True)]
    print("  total | " + " | ".join(str(v) for v in tot))
    print(f"  dia con mas peticiones: {peor[1]}")


for arg in sys.argv[1:]:
    resumen(Path(arg))
