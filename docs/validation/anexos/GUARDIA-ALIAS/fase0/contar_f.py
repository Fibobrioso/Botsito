"""Fase 0.f: de las filas protegidas que PASAN guardia.py, cuantas pasan tambien solo_lectura.py
(solo decide sobre Bash; las demas herramientas son n/a). Uso: python contar_f.py tabla.md."""

import sys
from collections import Counter
from pathlib import Path

filas = []
for linea in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()[2:]:
    celdas = [c.strip() for c in linea.strip().strip("|").split(" | ")]
    if len(celdas) == 5:
        filas.append(celdas)
    else:
        filas.append([celdas[0], celdas[1], " | ".join(celdas[2:-2]), celdas[-2], celdas[-1]])

fugas = [
    f
    for f in filas
    if f[3] == "pasa"
    and (
        (f[0].startswith("a/d") and f[1] not in ("espacio final",))
        or (f[0] in ("b contenedor",) and f[2] != "Glob")
        or (f[0].startswith("c variables") and ("//?/" in f[1] or "8.3" in f[1] or "$env:" in f[1]))
    )
]
print(f"fugas reales (guardia.py pasa): {len(fugas)}")
print(Counter(f[0].split(' ')[0] for f in fugas))
por_bash = [f for f in fugas if f[4] != "n/a"]
print(f"de ellas, decididas tambien por solo_lectura.py (Bash): {len(por_bash)}")
print(f"  pasan alli: {sum(f[4] == 'pasa' for f in por_bash)}; niega: {sum(f[4] == 'niega' for f in por_bash)}")
print("  por herramienta:", dict(Counter(f[2] for f in por_bash)))
print(f"las otras {len(fugas) - len(por_bash)} no pasan por solo_lectura.py (Read, Grep, PowerShell, Monitor):",
      dict(Counter(f[2] for f in fugas if f[4] == "n/a")))
