"""Que filas de «Diferencias por operacion» caen en una hora de ticks perdida (decision 2 de la
PARADA de la fase 0: el cruce se hace con un guion que queda escrito, no a ojo).

Uso: uv run python docs/validation/anexos/CORRIDA-CONSTRUCCION/horas_perdidas.py <salida del arnes>

Las horas son las 18 de los cuatro manifiestos de ticks (CORRIDA-CONSTRUCCION.md §1.e), escritas
aqui tal cual para que el guion no lea ningun manifiesto. Una fila cae en una hora perdida si el
instante del trader, el del bot emparejado o el del mas cercano esta dentro de esa hora UTC. Las
filas se leen de la salida del arnes, que lleva cada linea con su prefijo de diagnostico.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

HORAS_PERDIDAS = (
    "2026-01-05T10Z", "2026-01-14T07Z", "2026-01-20T11Z", "2026-01-23T11Z", "2026-01-29T11Z",
    "2026-04-03T09Z", "2026-04-06T10Z", "2026-04-07T10Z", "2026-04-22T07Z", "2026-04-22T10Z",
    "2026-04-22T13Z", "2026-04-23T05Z",
    "2026-07-10T05Z", "2026-07-14T12Z", "2026-07-16T11Z",
    "2026-08-14T07Z", "2026-08-17T11Z", "2026-08-20T07Z",
)  # fmt: skip
FUERA_DE_SESION = ("2026-04-22T13Z",)  # la ventana de verano acaba a las 13:00Z (§1.e)
INSTANTE = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?\+00:00")


def hora_de(instante: str) -> str:
    return instante[:13] + "Z"


def main(ruta: Path) -> int:
    sys.stdout.reconfigure(encoding="utf-8")  # las filas llevan «Δ»; la consola de Windows, cp1252
    filas = [
        ln.split("] ", 1)[-1]
        for ln in ruta.read_text(encoding="utf-8").splitlines()
        if ln.split("] ", 1)[-1].startswith(("trader | ", "bot | "))
    ]
    print(f"{ruta.name}: {len(filas)} filas por operacion")
    tocadas = 0
    for fila in filas:
        horas = sorted({hora_de(i) for i in INSTANTE.findall(fila)} & set(HORAS_PERDIDAS))
        if horas:
            tocadas += 1
            marca = " (fuera de sesion)" if all(h in FUERA_DE_SESION for h in horas) else ""
            print(f"- {', '.join(horas)}{marca}: {fila}")
    print(f"filas con algun instante en una hora perdida: {tocadas} de {len(filas)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1])))
