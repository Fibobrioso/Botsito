"""Quinta respuesta del consultor, punto 4, SIN ABRIR NADA: si el mes al que apunta cada tramo de
precaucion de v10 leido durante trabajo/sesion-04 tiene dias en `casos_ocultos`, en
`casos_reservados` (por particion) o en el universo de un mes reservado entero
(`knowledge/cases/meses_reservados.yaml`, que lleva marzo de 2026).

El mes de cada tramo sale de su motivo y de la fila del 2026-10-04 de HOLDOUT-EXPOSICIONES.md:
0:40:20-0:40:42, enero (por el contexto); 1:56:07-1:56:19, junio (posible exposicion);
1:27:44-1:28:19, un periodo que el audio no identifica. El ano no consta en ninguno: se cuentan
todos los anos.

Solo imprime RECUENTOS por particion: ni fechas ni ids de caso.

Uso: uv run python docs/validation/anexos/FILTRADAS-ESCENARIO-B/meses_de_los_tramos.py
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

from botsito.cases.holdout import cargar_meses_reservados, casos_ocultos, casos_reservados

RAIZ = Path(__file__).resolve().parents[4]
_MES = re.compile(r"-\d{4}-(0[1-9]|1[0-2])-\d{2}$", re.ASCII)  # el de holdout._MES_DE_CASO
TRAMOS = [
    ("0:40:20-0:40:42", 1, "enero"),
    ("1:56:07-1:56:19", 6, "junio"),
    ("1:27:44-1:28:19", None, "no identificado"),
]


def por_particion(casos: dict[str, str], mes: int | None) -> dict[str, int]:
    cuenta: Counter[str] = Counter()
    for caso, particion in casos.items():
        m = _MES.search(caso)
        if m is None:
            cuenta["SIN MES"] += 1
        elif mes is None or int(m.group(1)) == mes:
            cuenta[particion] += 1
    return dict(sorted(cuenta.items()))


def main() -> None:
    ocultos = casos_ocultos(RAIZ)
    reservados = casos_reservados(RAIZ)
    enteros = cargar_meses_reservados(RAIZ)
    for tramo, mes, nombre in TRAMOS:
        print(f"== {tramo} ({nombre})")
        o = por_particion(ocultos, mes)
        r = por_particion(reservados, mes)
        print(f"   casos_ocultos, dias por particion: {o or 'ninguno'}")
        print(f"   casos_reservados, dias por particion: {r or 'ninguno'}")
        if mes is None:
            print(f"   meses reservados enteros (cualquiera): {len(enteros)}")
        else:
            n = sum(1 for m in enteros if int(m[5:7]) == mes)
            print(f"   meses reservados enteros con ese mes (universo de marzo incluido): {n}")
        tiene = (
            bool(o)
            or bool(r)
            or (mes is None and bool(enteros))
            or (mes is not None and any(int(m[5:7]) == mes for m in enteros))
        )
        print(f"   TIENE DIAS RESERVADOS U OCULTOS: {tiene}")


if __name__ == "__main__":
    main()
