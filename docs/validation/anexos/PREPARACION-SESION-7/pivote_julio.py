"""0.7 de trabajo/preparacion-sesion-7: T0 y P5 + P6 en sesion de 2026-07, contados sobre
anexos/RECORRIDA-CONSTRUCCION-2/patrones-cuenta-por-mes.txt. Sale con 1 si no son 14 y 39.

Uso: uv run python pivote_julio.py <ruta de patrones-cuenta-por-mes.txt>
Ademas cuenta, para la cuenta de D5: P2, P3 y P7 de julio (operaciones del trader con una del bot
del mismo lado en su sesion, junto con T0) y las P5 de julio por lado.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

FILA = re.compile(r"^(T0|P\d) [^:]*?(?:\[([^\]]*)\])?(?: \[posible M[^\]]*\])?: (trader|bot) \| (\d{4}-\d{2})-\d{2} \| ")


def main(ruta: Path) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    cuenta: Counter[tuple[str, str]] = Counter()
    p5_lado: Counter[str] = Counter()
    for ln in ruta.read_text(encoding="utf-8").splitlines():
        m = FILA.match(ln)
        if not m or m.group(4) != "2026-07":
            continue
        patron, sub = m.group(1), m.group(2) or ""
        cuenta[(patron, sub)] += 1
        if patron == "P5":
            p5_lado[sub] += 1
    t0 = sum(v for (p, _), v in cuenta.items() if p == "T0")
    p5 = sum(v for (p, _), v in cuenta.items() if p == "P5")
    p6_sesion = cuenta[("P6", "en sesion")]
    p6_dia = cuenta[("P6", "en dia")]
    p2 = sum(v for (p, _), v in cuenta.items() if p == "P2")
    p3 = sum(v for (p, _), v in cuenta.items() if p == "P3")
    p7 = sum(v for (p, _), v in cuenta.items() if p == "P7")
    p1 = sum(v for (p, _), v in cuenta.items() if p == "P1")
    p4 = sum(v for (p, _), v in cuenta.items() if p == "P4")
    print(f"{ruta.name}, mes 2026-07")
    print(f"T0 (parejas): {t0}")
    print(f"P5: {p5} ({dict(p5_lado)}); P6 en sesion: {p6_sesion}; P6 en dia: {p6_dia}")
    print(f"operaciones de mas (P5 + P6 en sesion): {p5 + p6_sesion}")
    print(f"P1 {p1}, P2 {p2}, P3 {p3}, P4 {p4}, P7 {p7}")
    print(f"T0 + P2 + P3 + P7 = {t0} + {p2} + {p3} + {p7} = {t0 + p2 + p3 + p7}")
    print(f"tasa de pareja: {t0} / {t0 + p2 + p3 + p7} = {t0 / (t0 + p2 + p3 + p7):.3f}")
    ok = t0 == 14 and p5 + p6_sesion == 39
    print("OK: 14 y 39" if ok else "NO CUADRA: no son 14 y 39")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1])))
