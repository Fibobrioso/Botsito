"""Las tres fechas de «día anterior» que escribían dos anexos de 3e1995df, contadas por la compuerta.

Respuesta del consultor a la PARADA final de trabajo/preparacion-sesion-7 (2026-11-11), punto 3: se
cuentan con casos_reservados(repo) y casos_ocultos(repo), solo el número, sin imprimir ninguna.

Uso (desde la raíz del repo): uv run python tres_fechas.py

Las tres son el día de mercado anterior (el laborable anterior, el mismo cálculo que `anterior` de
dias_d3.py) al 1 de abril, al 1 de julio y al 3 de agosto de 2026. Antes de contar se comprueba que
son las que lleva 3e1995df: cada una aparece en dias-d3.txt o en sustitutas.txt de ese commit, y
ninguna de las dos salidas de ahora la lleva. No se imprime ninguna fecha ni ningún id.
"""

from __future__ import annotations

import re
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

from botsito.cases import visto
from botsito.cases.criterio_fidelidad import cargar_criterio
from botsito.cases.holdout import casos_ocultos, casos_reservados

REPO = Path(".")
COMMIT = "3e1995df"
ANEXOS = "docs/validation/anexos/PREPARACION-SESION-7"
SALIDAS = ("dias-d3.txt", "sustitutas.txt")
PRIMEROS = ("2026-04-01", "2026-07-01", "2026-08-03")


def anterior(d: str) -> str:
    x = date.fromisoformat(d) - timedelta(days=1)
    while x.weekday() >= 5:
        x -= timedelta(days=1)
    return x.isoformat()


def dias_de(casos: object) -> set[str]:
    return {m.group(1) for c in casos if (m := re.search(r"(\d{4}-\d{2}-\d{2})", str(c)))}


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    fechas = [anterior(d) for d in PRIMEROS]
    viejas = subprocess.run(
        ["git", "show", "3e1995df:docs/validation/anexos/PREPARACION-SESION-7/dias-d3.txt"],
        capture_output=True, text=True, encoding="utf-8", check=True,
    ).stdout + subprocess.run(
        ["git", "show", "3e1995df:docs/validation/anexos/PREPARACION-SESION-7/sustitutas.txt"],
        capture_output=True, text=True, encoding="utf-8", check=True,
    ).stdout  # fmt: skip
    nuevas = "".join((REPO / ANEXOS / s).read_text(encoding="utf-8") for s in SALIDAS)
    en_3e1995df = sum(f in viejas for f in fechas)
    en_las_de_ahora = sum(f in nuevas for f in fechas)
    print(f"fechas: {len(fechas)}; las lleva {COMMIT}: {en_3e1995df}; las salidas de ahora: {en_las_de_ahora}")

    reservados = dias_de(casos_reservados(REPO))
    ocultos = dias_de(casos_ocultos(REPO))
    criterio = cargar_criterio(REPO)
    dev: set[str] = set()
    for mes in criterio.construccion:
        for caso, part in visto.asignacion(REPO, mes).items():
            if part == "dev":
                m = re.search(r"(\d{4}-\d{2}-\d{2})$", caso)
                assert m
                dev.add(m.group(1))
    print(f"en casos_reservados: {sum(f in reservados for f in fechas)}")
    print(f"en casos_ocultos: {sum(f in ocultos for f in fechas)}")
    print(f"en los dias dev de construccion: {sum(f in dev for f in fechas)}")
    print(f"en ninguno de los tres: {sum(f not in reservados | ocultos | dev for f in fechas)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
