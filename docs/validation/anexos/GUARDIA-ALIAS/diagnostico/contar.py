"""Cuenta, solo sobre la columna de guardia.py, lo que pasa de la tabla del diagnostico de K."""

import sys
from collections import Counter
from pathlib import Path

filas = []
for linea in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()[2:]:
    celdas = [c.strip() for c in linea.strip().strip("|").split(" | ")]
    if len(celdas) == 5:
        filas.append(celdas)
    else:  # una celda con " | " dentro (la herramienta `gci -Recurse | gc`)
        filas.append([celdas[0], celdas[1], " | ".join(celdas[2:-2]), celdas[-2], celdas[-1]])

prot = [f for f in filas if f[0].startswith("a/d")]
pasan = [f for f in prot if f[3] == "pasa"]
print(f"a/d: {len(prot)} filas protegidas, {len(pasan)} pasan la guardia")
for (forma, herr), n in sorted(Counter((f[1], f[2]) for f in pasan).items()):
    print(f"  pasa: {forma} · {herr} x{n}")
for bloque in ("b contenedor", "b' contenedor real", "c variables"):
    sub = [f for f in filas if f[0].startswith(bloque)]
    print(f"{bloque}: {len(sub)} filas, pasan {sum(f[3] == 'pasa' for f in sub)}")
    for f in sub:
        if f[3] == "pasa":
            print(f"  pasa: {f[0]} · {f[1]} · {f[2]}")
buenas = [f for f in filas if f[0].startswith("e")]
print(f"e (lo bueno): {len(buenas)} filas, negadas {sum(f[3] != 'pasa' for f in buenas)}")
for f in buenas:
    if f[3] != "pasa":
        print(f"  negada: {f[1]} · {f[2]} · {f[3]}")
