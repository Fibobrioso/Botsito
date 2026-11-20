"""Operaciones del trader por dia `dev` de construccion, de una salida YA COMMITEADA del arnes.

trabajo/preregistro, fase 0, punto 0.4. Lee solo
`docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt` (enero, abril, julio y agosto
de 2026: construccion, ningun dia reservado): la seccion «## Por sesion» (una linea por sesion con
`trader N`) y la tabla «Resumen por mes», que da los dias corridos de cada mes. Un dia corrido sin
ninguna linea en «Por sesion», o con trader 0 en todas, cuenta como cero operaciones.

Uso: uv run python <este guion> <raiz del repo>
"""

from __future__ import annotations

import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path

ANEXO = "docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt"
SESION = re.compile(r"^(\d{4}-\d{2})-(\d{2}) \S+ \| trader (\d+) \|")
RESUMEN = re.compile(r"^(\d{4}-\d{2}) \| (\d+) \| (\d+) \|")


def main(repo: Path) -> None:
    lineas = (repo / ANEXO).read_text(encoding="utf-8").splitlines()
    i = lineas.index("## Por sesion")
    por_dia: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for linea in lineas[i + 1 :]:
        if linea.startswith("## "):
            break
        m = SESION.match(linea)
        if m:
            por_dia[m.group(1)][m.group(2)] += int(m.group(3))
    j = lineas.index("### Resumen por mes (en el orden de construccion)")
    dias_mes: dict[str, tuple[int, int]] = {}
    for linea in lineas[j + 2 :]:
        m = RESUMEN.match(linea)
        if not m:
            break
        dias_mes[m.group(1)] = (int(m.group(2)), int(m.group(3)))
    print("mes | dias dev | operaciones | dias con alguna | media | mediana | min | max")
    todos: list[int] = []
    for mes in sorted(dias_mes):
        n_dias, n_ops = dias_mes[mes]
        con = list(por_dia[mes].values())
        valores = con + [0] * (n_dias - len(con))
        assert sum(valores) == n_ops, (mes, sum(valores), n_ops)
        todos += valores
        print(
            f"{mes} | {n_dias} | {n_ops} | {sum(1 for v in valores if v)} | "
            f"{statistics.mean(valores):.2f} | {statistics.median(valores)} | "
            f"{min(valores)} | {max(valores)}"
        )
    print(
        f"total | {len(todos)} | {sum(todos)} | {sum(1 for v in todos if v)} | "
        f"{statistics.mean(todos):.2f} | {statistics.median(todos)} | {min(todos)} | {max(todos)}"
    )


if __name__ == "__main__":
    main(Path(sys.argv[1]).resolve())
