"""Filas de patrones-cuenta-por-mes.txt por (dia, sesion) y patron, para las sesiones nombradas.

Uso: uv run python filas_por_sesion.py <patrones-cuenta-por-mes.txt> <dia:sesion> ...
"""

from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

FILA = re.compile(
    r"^(T0|P\d) ([^:\[]*?)(?: \[([^\]]*)\])?(?: \[posible M[^\]]*\])?: (trader|bot) \| "
    r"(\d{4}-\d{2}-\d{2}) \| (\S+) \| (\S+) \| (\S+) "
)


def main(ruta: Path, pedidas: list[str]) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    por: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    for ln in ruta.read_text(encoding="utf-8").splitlines():
        m = FILA.match(ln)
        if m:
            clave = f"{m.group(1)}{'/' + m.group(3) if m.group(3) else ''} ({m.group(4)})"
            por[(m.group(5), m.group(6))][clave] += 1
    for p in pedidas:
        dia, ses = p.split(":")
        c = por.get((dia, ses), Counter())
        trader = sum(v for k, v in c.items() if "(trader)" in k)
        bot = sum(v for k, v in c.items() if "(bot)" in k)
        print(f"{dia} {ses}: {sum(c.values())} filas (trader {trader}, bot {bot}): {dict(sorted(c.items()))}")
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]), sys.argv[2:]))
