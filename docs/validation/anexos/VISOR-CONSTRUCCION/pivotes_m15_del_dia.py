"""VISOR-CONSTRUCCION (R3.2), lo que el revisor no pudo comprobar: si algun pivote de M15 que
imprime `traza_por_cierre.py` (la liquidez de RN-004) tiene su NIVEL en una vela anterior a las 00:00Z de
la fecha del caso. Un pivote formado de madrugada lo forma una M15 contraria tras una racha de
M15 del otro color, y su nivel es el extremo de esa racha (`domain/pivotes_m15.py`): si la racha
empieza el dia UTC anterior, el precio impreso podria ser de ese dia.

Corre el mismo motor que la traza (comun_visor.construir con el `Lector` de traza_por_cierre.py),
reune los pivotes distintos que la traza imprime (los formados desde las 00:00Z; los de antes los
tapa la traza) y, para cada uno, busca su vela contraria en las M15 del dia y su racha. Imprime
SOLO recuentos: ninguna hora, ninguna vela, ningun precio. No escribe nada.

    uv run python docs/validation/anexos/VISOR-CONSTRUCCION/pivotes_m15_del_dia.py <caso>...
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comun_visor as cv  # noqa: E402
import traza_por_cierre as tpc  # noqa: E402

from botsito.domain import pivotes_m15 as pm  # noqa: E402
from botsito.engine.interprete import Interprete  # noqa: E402


def main(caso: str) -> int:
    lector = tpc.Lector()
    datos: list[Any] = []

    def instalar(motor: Any) -> None:
        lector.instalar(motor)
        evaluar_lector = Interprete.evaluar

        def evaluar(self: Any, nodo: Any, momento: Any, estado: Any, faltan: Any) -> Any:
            if not datos and getattr(momento, "datos", None) is not None:
                datos.append(momento.datos)
            return evaluar_lector(self, nodo, momento, estado, faltan)

        Interprete.evaluar = evaluar  # type: ignore[method-assign]

    d = cv.construir(caso, antes_de_correr=instalar)
    pivotes = {
        (p.lado, int(p.nivel), int(p.contraria_inicio), int(p.formado_en))
        for p in lector.pivote.values()
        if p is not None and not d.antes_del_dia(int(p.formado_en))
    }
    if not datos:
        print(f"{caso}: sin datos de mercado capturados")
        return 2
    m15 = list(datos[0]._m15)
    nivel_antes = racha_antes = sin_vela = 0
    for lado, nivel, contraria_inicio, _ in sorted(pivotes):
        i = next((k for k, v in enumerate(m15) if int(v.inicio) == contraria_inicio), None)
        if i is None:
            sin_vela += 1
            continue
        racha = pm._racha_anterior(m15, i, -pm.color(m15[i]))

        def extremo(v: Any, lado: str = lado) -> int:
            return int(v.maxima) if lado == pm.ALTO else int(v.minima)

        if any(d.antes_del_dia(int(v.inicio)) for v in racha):
            racha_antes += 1
        if any(extremo(v) == nivel and d.antes_del_dia(int(v.inicio)) for v in racha):
            nivel_antes += 1
    print(
        f"{caso}: pivotes de M15 que imprime la traza {len(pivotes)}; con la racha empezando antes "
        f"de las 00:00Z {racha_antes}; con su NIVEL en una vela anterior a las 00:00Z "
        f"{nivel_antes}; sin su vela contraria en las M15 del dia {sin_vela}"
    )
    return 3 if nivel_antes else 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    peor = 0
    for c in sys.argv[1:]:
        peor = max(peor, main(c))
    raise SystemExit(peor)
