"""Recuentos por mes de casos_reservados y casos_ocultos, y los dias dev y operaciones del trader de
la construccion por la compuerta del arnes. Ninguna clave ni fecha impresa. Raiz por argumento."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

from botsito.cases.criterio_fidelidad import cargar_criterio
from botsito.cases.holdout import casos_ocultos, casos_reservados
from botsito.engine import arnes

MES = re.compile(r"(\d{4}-\d{2})-\d{2}$", re.ASCII)


def por_mes(claves: dict[str, str]) -> Counter[str]:
    return Counter(m.group(1) if (m := MES.search(c)) else "?" for c in claves)


def main() -> None:
    repo = Path(sys.argv[1]).resolve()
    criterio = cargar_criterio(repo)
    reservados = por_mes(casos_reservados(repo))
    ocultos = por_mes(casos_ocultos(repo))
    print(f"casos_reservados: {sum(reservados.values())} ({dict(sorted(reservados.items()))})")
    print(f"casos_ocultos: {sum(ocultos.values())} ({dict(sorted(ocultos.items()))})")
    for mes in criterio.construccion:
        print(f"  {mes}: reservados {reservados.get(mes, 0)}, ocultos {ocultos.get(mes, 0)}")
    dias = arnes.dias_de_construccion(repo, criterio, criterio.construccion)
    por = Counter(d.dia[:7] for d in dias)
    ops = Counter(d.dia[:7] for d in dias for _ in d.operaciones)
    for mes in criterio.construccion:
        print(f"  {mes}: dias dev {por[mes]}, operaciones del trader {ops[mes]}")
    print(f"total: dias dev {len(dias)}, operaciones del trader {sum(ops.values())}")


if __name__ == "__main__":
    main()
