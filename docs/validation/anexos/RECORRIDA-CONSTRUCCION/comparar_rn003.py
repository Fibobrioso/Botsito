"""El rn003 (el sesgo de RN-003 al abrir) de cada sesion con operaciones del trader de abril y
agosto en la linea base de 2026-09-26 (CABLEADO-SIMULADOR-LINEA-BASE.txt) frente a la corrida 1
de esta rama: el «RN-003 al abrir» de la salida es un agregado de todas las sesiones y no se parte
por mes en el diff. SOLO LEE las dos salidas.

uso: uv run python comparar_rn003.py <linea base> <cuenta-arrastrada.txt>
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

POR_SESION = re.compile(
    r"^(\d{4}-\d{2}-\d{2}) (\S+) \| trader (\d+) \| bot (\d+) \| rn003 (\S+) \|"
)
sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]


def sesgos(ruta: Path) -> dict[tuple[str, str], str]:
    salida = {}
    for ln in ruta.read_text(encoding="utf-8").splitlines():
        if ln.startswith("[DIAGNOSTICO") and "] " in ln:
            ln = ln.split("] ", 1)[1]
        m = POR_SESION.match(ln)
        if m:
            salida[(m.group(1), m.group(2))] = m.group(5)
    return salida


base, nueva = (sesgos(Path(p)) for p in sys.argv[1:3])
comunes = sorted(set(base) & set(nueva))
print(f"sesiones: linea base {len(base)}; corrida 1 {len(nueva)}; comunes {len(comunes)}")
print(f"solo en la base: {sorted(set(base) - set(nueva))}")
cambian = [(d, s, base[(d, s)], nueva[(d, s)]) for d, s in comunes if base[(d, s)] != nueva[(d, s)]]
print(f"sesiones comunes cuyo rn003 cambia: {len(cambian)}")
for d, s, a, b in cambian:
    print(f"  {d} {s}: {a} -> {b}")
for nombre, mapa in (("base", base), ("corrida 1", nueva)):
    por_mes: dict[str, Counter[str]] = {}
    for (d, _s), v in mapa.items():
        por_mes.setdefault(d[:7], Counter())[v] += 1
    for mes in sorted(por_mes):
        if mes in ("2026-04", "2026-08"):
            print(
                f"  {nombre} {mes}: "
                + ", ".join(f"{k} {n}" for k, n in sorted(por_mes[mes].items()))
            )
