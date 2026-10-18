"""VISOR-CONSTRUCCION (R3.2), respuesta del consultor a la PARADA, puntos 4 y 5: ANTES de generar la
pagina del visor de un dia, si lo que la pagina pinta de fuera del dia dev toca un dia reservado.

Prepara el dia como `motor visor --simular --caso` (comun_visor.py) y mira, sin imprimir ninguna
fecha, hora ni precio:
- las H4 de contexto de la pagina (`DiaVisor.h4`, las que pinta `_h4_svg`): cuantas hay, cuantas
  empiezan antes de las 00:00Z de la fecha del caso, cuantas son del mes anterior, y cuantas caen en
  un dia OCULTO (reservado o retirado: `casos_ocultos`, por pertenencia de
  `caso-eurusd-<fecha UTC>`)
  o en un mes reservado entero (`meses_reservados.yaml`);
- el grafico M1 de la ventana (`DiaVisor.m1`): si empieza antes de las 00:00Z, y si ese tramo cae en
  un dia oculto o en un mes reservado entero.
Sale con codigo 2 si algo toca un dia oculto o un mes reservado entero: es PARADA.

    uv run python docs/validation/anexos/VISOR-CONSTRUCCION/contexto_h4.py <caso> [<caso> ...]
"""

from __future__ import annotations

import sys
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comun_visor as cv  # noqa: E402

from botsito.cases.holdout import cargar_meses_reservados, casos_ocultos  # noqa: E402
from botsito.domain.ticks import MS_POR_MINUTO  # noqa: E402

PREFIJO_CASO = "caso-eurusd-"


def _fecha(minuto: int) -> str:
    return datetime.fromtimestamp(minuto * MS_POR_MINUTO / 1000, UTC).date().isoformat()


def main(casos: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    ocultos = set(casos_ocultos(cv.RAIZ))
    meses_enteros = set(cargar_meses_reservados(cv.RAIZ))
    peor = 0
    for caso in casos:
        d = cv.construir(caso)
        mes = d.clave[:7]

        def toca(fecha: str) -> bool:
            return f"{PREFIJO_CASO}{fecha}" in ocultos or fecha[:7] in meses_enteros

        h4 = d.pagina.h4
        antes = [v for v in h4 if d.antes_del_dia(int(v.inicio))]
        mes_anterior = [v for v in antes if _fecha(int(v.inicio))[:7] != mes]
        h4_ocultas = [v for v in antes if toca(_fecha(int(v.inicio)))]
        m1 = d.pagina.m1
        m1_antes = [v for v in m1 if d.antes_del_dia(int(v.inicio))]
        m1_ocultas = [v for v in m1_antes if toca(_fecha(int(v.inicio)))]
        veredicto = "PARADA" if (h4_ocultas or m1_ocultas) else "ok"
        if veredicto == "PARADA":
            peor = 2
        print(
            f"{caso}: H4 de contexto {len(h4)}; antes del dia {len(antes)}; del mes anterior "
            f"{len(mes_anterior)}; en un dia oculto o mes reservado {len(h4_ocultas)} | M1 de la "
            f"ventana antes de las 00:00Z {len(m1_antes)}; en un dia oculto o mes reservado "
            f"{len(m1_ocultas)} | {veredicto}"
        )
    return peor


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
