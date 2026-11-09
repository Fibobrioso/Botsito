"""Los recuentos de §8 (respuesta del consultor a la PARADA 2, puntos 1 y 4): cuantas filas de cada
patron hay por mes y en cada una de las nueve sesiones del visor, y cuantas de P4 son de agosto desde
el 2026-08-19. Solo LEE `patrones-cuenta-por-mes.txt` (las filas de `patrones.py --filas`).

Uso (desde la raiz):
    uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/recuento_clases.py \\
        docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/patrones-cuenta-por-mes.txt
"""

# ruff: noqa: E501  (textos y tablas literales: el docstring explica las columnas)

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

VISOR = {
    ("2026-07-06", "07-11"), ("2026-07-07", "07-11"), ("2026-07-07", "11-15"),
    ("2026-07-15", "11-15"), ("2026-01-22", "11-15"), ("2026-07-02", "11-15"),
    ("2026-04-13", "07-11"), ("2026-01-13", "07-11"), ("2026-04-15", "11-15"),
    ("2026-07-14", "11-15"),
}  # fmt: skip


def main(ruta: Path) -> int:
    sys.stdout.reconfigure(encoding="utf-8", newline="\n")  # type: ignore[union-attr]
    filas = []
    dentro = False
    for ln in ruta.read_text(encoding="utf-8").splitlines():
        if ln == "-- filas":
            dentro = True
            continue
        if dentro and ": " in ln:
            cabeza, fila = ln.split(": ", 1)
            patron = cabeza.split(" [")[0]
            c = fila.split(" | ")
            filas.append((patron, c[1], c[2]))
    por_mes: Counter[tuple[str, str]] = Counter((p, d[:7]) for p, d, _ in filas)
    en_visor: Counter[tuple[str, str, str]] = Counter(
        (p, d, s) for p, d, s in filas if (d, s) in VISOR
    )
    print(f"# Recuentos de §8 sobre {ruta.name}: {len(filas)} filas")
    print("patron | mes | filas")
    for (p, m), n in sorted(por_mes.items()):
        print(f"{p} | {m} | {n}")
    print("\npatron | sesion del visor | filas")
    for (p, d, s), n in sorted(en_visor.items()):
        print(f"{p} | {d} {s} | {n}")
    p4_ago = sum(1 for p, d, _ in filas if p == "P4 sin orden" and d >= "2026-08-19")
    print(f"\nP4 de agosto desde el 2026-08-19: {p4_ago}")
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1])))
