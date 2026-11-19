"""Por particion reservada: dias, retirados, medibles y, de los medibles, cuantos caen dentro de
un tramo de `cobertura_material`. SOLO RECUENTOS: ninguna clave, ninguna fecha, ningun tramo.

trabajo/preregistro, segundo tiempo, T3 (decision 2 de la respuesta del consultor del
2026-11-19, que autoriza este recuento). Lee solo la ASIGNACION (`casos_reservados`,
`casos_retirados`, `casos_medidos`) y la `cobertura_material` de cada camino por su cargador
(`paquete.cargar_config` para el kit, `fidelidad.cargar_config` para el camino de fidelidad). El
criterio es el TRAMO, no el mes (respuesta, punto 2): un dia cuenta si cae entre el `desde` y el
`hasta` de algun tramo de su mes en la cobertura de SU camino; un mes declarado con cero tramos, o
no declarado, no aporta ninguno. La fecha de cada caso se toma del final de su id y no se imprime.

Uso: uv run python <este guion> <raiz del repo>
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

from botsito.cases import fidelidad, paquete
from botsito.cases.holdout import (
    PARTICIONES_RESERVADAS,
    PARTICIONES_RESERVADAS_FIDELIDAD,
    RESERVADAS,
    casos_medidos,
    casos_reservados,
    casos_retirados,
)

_DIA = re.compile(r"(\d{4}-\d{2}-\d{2})$")


def main(repo: Path) -> None:
    kit = paquete.cargar_config(repo / paquete.DIRECTORIO_KIT / paquete.FICHERO_CONFIG).cobertura
    fid = fidelidad.cargar_config(repo).cobertura
    cobertura = {p: kit for p in PARTICIONES_RESERVADAS}
    cobertura.update({p: fid for p in PARTICIONES_RESERVADAS_FIDELIDAD})

    reservados = casos_reservados(repo)
    retirados = casos_retirados(repo)
    medidos = casos_medidos(repo)

    en_tramo: Counter[str] = Counter()
    mes_sin_tramos: Counter[str] = Counter()
    mes_no_declarado: Counter[str] = Counter()
    fuera_de_tramo: Counter[str] = Counter()
    for caso, particion in medidos.items():
        m = _DIA.search(caso)
        if m is None:
            raise SystemExit("un caso sin fecha al final de su id: no se puede contar")
        dia = m.group(1)
        tramos = cobertura[particion].get(dia[:7])
        if tramos is None:
            mes_no_declarado[particion] += 1
        elif not tramos:
            mes_sin_tramos[particion] += 1
        elif any(desde <= dia <= hasta for desde, hasta in tramos):
            en_tramo[particion] += 1
        else:
            fuera_de_tramo[particion] += 1

    tot = Counter(reservados.values())
    ret = Counter(retirados.values())
    med = Counter(medidos.values())
    print(
        "particion | dias | retirados | medibles | medibles en un tramo | en un mes con cero "
        "tramos | en un mes sin declarar | fuera de los tramos de su mes"
    )
    for p in RESERVADAS:
        print(
            f"{p} | {tot[p]} | {ret[p]} | {med[p]} | {en_tramo[p]} | {mes_sin_tramos[p]} | "
            f"{mes_no_declarado[p]} | {fuera_de_tramo[p]}"
        )
    print(
        f"TOTAL | {sum(tot.values())} | {sum(ret.values())} | {sum(med.values())} | "
        f"{sum(en_tramo.values())} | {sum(mes_sin_tramos.values())} | "
        f"{sum(mes_no_declarado.values())} | {sum(fuera_de_tramo.values())}"
    )


if __name__ == "__main__":
    main(Path(sys.argv[1]).resolve())
