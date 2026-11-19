"""Cuantas filas de HOLDOUT-EXPOSICIONES.md nombran cada particion reservada, y en que fecha se
declararon. trabajo/preregistro, fase 0, punto 0.3.

Solo imprime el nombre de la particion, el numero de filas y la PRIMERA columna de cada fila (la
fecha de la declaracion, que no es un dia de mercado). No imprime nada del contenido de la fila.
Una fila cuenta para una particion si su texto nombra la particion entre acentos graves o tal
cual (`holdout-1` o holdout-1). Ademas: filas que nombran «holdout» sin numero, y las que nombran
un mes reservado entero de meses_reservados.yaml (por el nombre del mes en castellano).
Uso: uv run python <este guion> <raiz del repo>
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

FICHERO = "docs/validation/HOLDOUT-EXPOSICIONES.md"
PARTICIONES = ("holdout-1", "holdout-2", "holdout-3", "fidelidad-1", "fidelidad-2", "fidelidad-3")
FILA = re.compile(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|")


def main(repo: Path) -> None:
    filas = []
    for linea in (repo / FICHERO).read_text(encoding="utf-8").splitlines():
        m = FILA.match(linea)
        if m:
            filas.append((m.group(1), linea))
    print(f"filas de la tabla: {len(filas)}")
    for p in PARTICIONES:
        fechas = [f for f, texto in filas if re.search(rf"(?<![\w-]){re.escape(p)}(?![\w-])", texto)]
        print(f"{p} | {len(fechas)} filas | declaradas: {sorted(set(fechas))}")
    sin_numero = [
        f
        for f, texto in filas
        if re.search(r"holdout(?!-\d)", texto, re.IGNORECASE)
        and not any(p in texto for p in PARTICIONES)
    ]
    print(f"nombran holdout sin particion | {len(sin_numero)} filas | {sorted(set(sin_numero))}")
    for mes in ("marzo", "mayo", "junio", "septiembre", "octubre", "noviembre", "febrero"):
        fechas = [f for f, texto in filas if re.search(rf"\b{mes}\b", texto, re.IGNORECASE)]
        print(f"nombran {mes} | {len(fechas)} filas")


if __name__ == "__main__":
    main(Path(sys.argv[1]).resolve())
