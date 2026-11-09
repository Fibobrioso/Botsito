"""Recuento de julio de 2026 por dia: casos_reservados y casos_ocultos, sin imprimir ids.
Y meses_libres (si 7 esta). Solo recuentos."""
from pathlib import Path

from botsito.cases.holdout import casos_ocultos, casos_reservados, meses_libres

repo = Path(".").resolve()
res = casos_reservados(repo)
ocu = casos_ocultos(repo)


def dias_de(d: dict[str, str]) -> list[str]:
    salida = []
    for k in d:
        for parte in str(k).replace("caso-eurusd-", "").split():
            if parte.startswith("2026-07"):
                salida.append(parte[:10])
    return salida


r7 = dias_de(res)
o7 = dias_de(ocu)
print(f"casos_reservados: {len(res)} en total; de 2026-07: {len(r7)}")
print(f"casos_ocultos: {len(ocu)} en total; de 2026-07: {len(o7)}")
for dia in range(1, 32):
    d = f"2026-07-{dia:02d}"
    n_r = r7.count(d)
    n_o = o7.count(d)
    if n_r or n_o:
        print(f"  dia {dia}: reservados {n_r}, ocultos {n_o}")
print("dias de julio 1-31 sin ninguno: ", sum(1 for dia in range(1, 32) if f"2026-07-{dia:02d}" not in r7 + o7))
ml = meses_libres(repo)
print(f"meses_libres: {sorted(ml) if ml is not None else None}; 7 dentro: {ml is not None and 7 in ml}")
