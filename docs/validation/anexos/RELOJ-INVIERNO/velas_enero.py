"""M3 de RELOJ-INVIERNO.md, la primera mirada: velas M1 de Dukascopy (BID) de un tramo de enero, para
comparar a ojo con el eje de un fotograma de v4 (la medida es eje_contra_dukascopy.py).

    uv run python docs/validation/anexos/RELOJ-INVIERNO/velas_enero.py AAAA-MM-DD HH:MM HH:MM   (horas UTC)
"""

from __future__ import annotations

import os
import sys
from datetime import UTC, datetime
from pathlib import Path

RAIZ = Path(os.environ.get("BOTSITO_RAIZ") or Path(__file__).resolve().parents[4])
sys.path.insert(0, str(RAIZ / "src"))

from botsito.cases.fidelidad import cargar_config  # noqa: E402
from botsito.config.ajustes import carpeta_datos  # noqa: E402
from botsito.data.dataset import buscar_manifiesto, cargar_manifiesto, cargar_serie  # noqa: E402


def main(dia: str, desde: str, hasta: str) -> int:
    if not dia.startswith("2026-01-"):
        raise SystemExit("solo enero")
    prefijo = cargar_config(RAIZ).dataset_prefijo
    ruta = buscar_manifiesto(RAIZ, f"{prefijo}2026-01")
    s = cargar_serie(cargar_manifiesto(ruta), carpeta_datos(RAIZ))
    a = datetime.fromisoformat(f"{dia}T{desde}:00+00:00")
    b = datetime.fromisoformat(f"{dia}T{hasta}:00+00:00")
    print(f"{ruta.stem} · {dia} {desde}-{hasta} UTC · O H L C (puntos de 1e-5)")
    for v in s.velas:
        t = datetime.fromtimestamp(int(v.inicio) * 60, tz=UTC)
        if a <= t <= b:
            print(f"{t:%H:%M} {int(v.abierta)} {int(v.maxima)} {int(v.minima)} {int(v.cierre)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(*sys.argv[1:4]))
