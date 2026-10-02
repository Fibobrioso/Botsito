"""Cuanta evidencia oculta `kb` por defecto en el repositorio real, por video, motivo y via.

Anexo de `docs/validation/CUARENTENA-POR-DEFECTO.md` (cuarta orden, 1b; quinta orden). Via «cita»:
su intervalo pisa un segmento oculto; via «copia»: su texto copia uno (`cuarentena.copia`). Imprime
SOLO cuentas: ni ids de casos, ni texto, ni fechas.

    uv run python docs/validation/anexos/CUARENTENA-POR-DEFECTO/kb_ocultos.py
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

from botsito.cli import _carpeta_datos
from botsito.corpus.cuarentena import items_ocultos
from botsito.retrieval.indice import construir_indice

RAIZ = Path(__file__).resolve().parents[4]


def main() -> int:
    ind = construir_indice(RAIZ, _carpeta_datos(RAIZ))
    por_cita: set[str] = set()
    for video, filtro in ind.filtros.items():
        de_video = [(it.id, it.t0_ms, it.t1_ms) for it in ind.items if it.video_id == video]
        por_cita.update(items_ocultos(filtro, de_video))
    cuenta = Counter(
        (o.video_id, o.motivo, "cita" if iid in por_cita else "copia")
        for iid, o in ind.evidencia_oculta.items()
    )
    print(f"items de evidencia: {len(ind.items)}; ocultos por defecto: {len(ind.evidencia_oculta)}")
    print("| Video | Motivo | Via | Items |")
    print("|---|---|---|---|")
    for (video, motivo, via), n in sorted(cuenta.items()):
        print(f"| {video} | ({motivo}) | {via} | {n} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
