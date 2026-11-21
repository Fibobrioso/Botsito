"""Resume la salida de test_medida_enlaces_tmp.py: una fila por (parte, forma, clase) con lo que
decide cada herramienta, agrupado: NEGADA (todas), PERMITIDA (todas) o la lista mixta."""

import sys
from collections import OrderedDict

filas: "OrderedDict[tuple[str, str, str], list[tuple[str, str]]]" = OrderedDict()
for linea in open(sys.argv[1], encoding="utf-8"):
    partes = [p.strip() for p in linea.rstrip("\n").lstrip(".F").split(" | ")]
    if len(partes) != 5 or partes[0] not in {"memoria", "stdin"}:
        continue
    parte, forma, clase, herramienta, decision = partes
    filas.setdefault((parte, forma, clase), []).append((herramienta, decision))

print("| parte | forma | clase | decision |")
print("|---|---|---|---|")
for (parte, forma, clase), ds in filas.items():
    negadas = [h for h, d in ds if d.startswith("negada")]
    if len(negadas) == len(ds):
        reglas = sorted({d.split(" ", 1)[1] for _, d in ds})
        txt = "NEGADA en todas (" + "; ".join(reglas) + ")"
    elif not negadas:
        txt = "PERMITIDA en todas (" + ", ".join(h for h, _ in ds) + ")"
    else:
        txt = "mixta: " + "; ".join(f"{h}: {'negada' if d.startswith('negada') else 'PERMITIDA'}" for h, d in ds)
    print(f"| {parte} | {forma} | {clase} | {txt} |")
