# ruff: noqa: E501  (textos de salida)
"""Los huecos de dias de mercado entre dias corridos de la construccion (sesgo 2, punto c).

Lee los 76 dias dev por la compuerta del arnes (solo sus fechas, ninguna operacion) y, de los
manifiestos M1 de los CUATRO meses de construccion (data/manifests, en git), las fechas sin datos
(fines de semana y festivos). Un dia de mercado es un dia de lunes a viernes con M1 en su manifiesto.
Un dia de un mes sin manifiesto de construccion (febrero, marzo, mayo, junio) no se lee: se cuenta
como «mes fuera de la construccion» sin mirar su manifiesto. Raiz por argumento.
"""

from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path

from botsito.cases.criterio_fidelidad import cargar_criterio
from botsito.comun.yaml_estricto import leer_yaml
from botsito.engine import arnes

MANIFIESTOS = {
    "2026-01": "data/manifests/eurusd-m1-2026-01-e37291d4.yaml",
    "2026-04": "data/manifests/eurusd-m1-2026-04-990211bd.yaml",
    "2026-07": "data/manifests/eurusd-m1-2026-07-aa162170.yaml",
    "2026-08": "data/manifests/eurusd-m1-2026-08-0d42230e.yaml",
}


def main() -> None:
    repo = Path(sys.argv[1]).resolve()
    criterio = cargar_criterio(repo)
    sin_datos: set[str] = set()
    for ruta in MANIFIESTOS.values():
        doc = leer_yaml(repo / ruta)
        sin_datos |= {str(d) for d in doc["dias"]["sin_datos"]}
        sin_datos |= {str(d) for d in doc["dias"]["ausentes"]}
    dias = sorted(
        date.fromisoformat(d.dia)
        for d in arnes.dias_de_construccion(repo, criterio, criterio.construccion)
    )
    print(f"dias corridos: {len(dias)}; orden de la corrida: {dias[0]} .. {dias[-1]} (por fecha)")
    huecos = 0
    for a, b in zip(dias, dias[1:], strict=False):
        mercado, fuera = 0, set()
        d = a + timedelta(days=1)
        while d < b:
            mes = d.isoformat()[:7]
            if mes not in MANIFIESTOS:
                fuera.add(mes)
            elif d.weekday() < 5 and d.isoformat() not in sin_datos:
                mercado += 1
            d += timedelta(days=1)
        if mercado or fuera:
            huecos += 1
            print(
                f"hueco entre {a} y {b}: {mercado} dias de mercado sin correr en meses de construccion"
                + (
                    f"; meses fuera de la construccion por medio: {', '.join(sorted(fuera))}"
                    if fuera
                    else ""
                )
            )
    print(f"huecos: {huecos}; tramos de dias seguidos: {huecos + 1}")


if __name__ == "__main__":
    main()
