"""Escribe (o comprueba) la lista de propuestas con segmentos ocultos que lee la guardia.

La lista se CALCULA con `botsito.corpus.cuarentena.propuestas_con_ocultos` (orden del consultor del
2026-10-01, rama `trabajo/cuarentena-por-defecto`): no se escribe a mano. Imprime solo nombres de
fichero y cuentas por regla, nunca contenido.

Uso:
    uv run python scripts/propuestas_con_ocultos.py            (comprueba; sale con 1 si no cuadra)
    uv run python scripts/propuestas_con_ocultos.py --escribir (la reescribe)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from botsito.corpus.cuarentena import (
    FICHERO_PROPUESTAS_OCULTAS,
    propuestas_con_ocultos,
    texto_de_la_lista,
)

RAIZ = Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--escribir", action="store_true")
    args = ap.parse_args(argv)
    calculadas = propuestas_con_ocultos(RAIZ)
    for nombre, cuenta in sorted(calculadas.items()):
        print(f"{nombre}: " + ", ".join(f"({m}) {cuenta[m]}" for m in sorted(cuenta)))
    texto = texto_de_la_lista(calculadas)
    destino = RAIZ / FICHERO_PROPUESTAS_OCULTAS
    if args.escribir:
        destino.write_text(texto, encoding="utf-8", newline="\n")
        print(f"OK: {len(calculadas)} propuestas en {FICHERO_PROPUESTAS_OCULTAS}")
        return 0
    actual = destino.read_text(encoding="utf-8") if destino.is_file() else ""
    if actual != texto:
        print(f"ERROR: {FICHERO_PROPUESTAS_OCULTAS} no coincide con lo calculado: --escribir")
        return 1
    print(f"OK: {FICHERO_PROPUESTAS_OCULTAS} coincide ({len(calculadas)} propuestas)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
