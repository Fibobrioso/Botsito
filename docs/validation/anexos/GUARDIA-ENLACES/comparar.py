"""Compara caso a caso la medida de antes (guardia de main) y la de despues (la de la rama)."""

import sys
from collections import Counter


def leer(fichero: str) -> dict[tuple[str, ...], str]:
    salida = {}
    for linea in open(fichero, encoding="utf-8"):
        partes = [p.strip() for p in linea.rstrip("\n").lstrip(".F").split(" | ")]
        if len(partes) == 5 and partes[0] in {"memoria", "stdin"}:
            salida[tuple(partes[:4])] = partes[4]
    return salida


antes, despues = leer(sys.argv[1]), leer(sys.argv[2])
cuenta: Counter[str] = Counter()
for clave in sorted(set(antes) | set(despues)):
    a, d = antes.get(clave, "(falta)"), despues.get(clave, "(falta)")
    an, dn = a.startswith("negada"), d.startswith("negada")
    if an and not dn:
        cuenta["negada -> PERMITIDA"] += 1
        print("ABRE:", " | ".join(clave), "|", a, "->", d)
    elif not an and dn:
        cuenta["PERMITIDA -> negada"] += 1
    elif a != d:
        cuenta["negada, otra regla"] += 1
        print("REGLA:", " | ".join(clave), "|", a, "->", d)
    else:
        cuenta["igual"] += 1
print(dict(cuenta), "casos:", len(set(antes) | set(despues)))
