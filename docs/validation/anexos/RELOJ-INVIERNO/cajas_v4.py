"""M3b de RELOJ-INVIERNO.md: las posiciones de enero que enseñan los fotogramas de v4 abiertos en M3,
frente a la hora UTC del libro de enero (declarado UTC en M1).

Los fotogramas 1149000, 1200000 y 1248000 de v4 (abiertos en M3 por instante localizado) enseñan
en el eje del grafico tres dias de enero -viernes 30, jueves 29 y martes 27- con una posicion
dibujada (la caja de entrada, stop y objetivo de FX Replay) y la etiqueta de su precio de entrada
en el eje de precios. Este guion imprime, de esos TRES dias y de ningun otro, la hora UTC de cada
entrada del libro y su precio de entrada (las dos columnas declaradas en HOLDOUT-EXPOSICIONES el
2026-10-06), y esa hora escrita en UTC+1 (Europe/Madrid en enero) y en UTC+2 (Etc/GMT-2), para
compararla con la hora a la que el eje del grafico pone la caja. Nada mas: ni stop, ni objetivo,
ni resultado.

    uv run python docs/validation/anexos/RELOJ-INVIERNO/cajas_v4.py
"""

from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

RAIZ = Path(os.environ.get("BOTSITO_RAIZ") or Path(__file__).resolve().parents[4])
sys.path.insert(0, str(RAIZ / "src"))

from botsito.cases.holdout import casos_ocultos, casos_reservados  # noqa: E402
from botsito.config.registro import cargar_registro  # noqa: E402
from botsito.corpus.libro import PESTANA_OPERACIONES, filas_de_los_dias  # noqa: E402
from botsito.corpus.libros import cargar_libros, sha256_de  # noqa: E402

LIBRO = "corpus/Estrategia del trader/Material adicional de su operativa/backtesting-analytics ENERO 2026.xlsx"  # noqa: E501
DIAS = ("2026-01-27", "2026-01-29", "2026-01-30")
MADRID = ZoneInfo("Europe/Madrid")
FIJO = ZoneInfo("Etc/GMT-2")


def main() -> int:
    ocultos = set(casos_ocultos(RAIZ)) | set(casos_reservados(RAIZ))
    if any(d in c for c in ocultos for d in DIAS):
        raise SystemExit("ERROR: un dia pedido esta en una particion: no se lee")
    libro = RAIZ / LIBRO
    decl = cargar_libros(RAIZ).get(sha256_de(libro))
    if decl is None:
        raise SystemExit("ERROR: el libro de enero no esta declarado en libros.yaml (M1)")
    huso_dias = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml").texto(
        "huso_operativa"
    )
    filas = filas_de_los_dias(
        libro, set(DIAS), PESTANA_OPERACIONES, ("dateStart", "entryPrice"), decl,
        huso_de_los_dias=huso_dias,
    )
    print("| Dia | Hora UTC (libro) | En UTC+1 (Madrid, enero) | En UTC+2 (Etc/GMT-2) | Entrada |")
    print("|---|---|---|---|---|")
    for f in sorted(filas, key=lambda f: str(f["_instante_utc"])):
        i = datetime.fromisoformat(str(f["_instante_utc"]))
        print(f"| {i:%a %Y-%m-%d} | {i:%H:%M:%S} | {i.astimezone(MADRID):%H:%M:%S} | "
              f"{i.astimezone(FIJO):%H:%M:%S} | {f['entryPrice']} |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
