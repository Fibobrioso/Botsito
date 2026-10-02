"""Cuanta evidencia oculta `kb` por defecto en el repositorio real, por video, motivo y via.

Anexo de `docs/validation/CUARENTENA-POR-DEFECTO.md`. Con el criterio de la sexta orden del
consultor (2026-10-01), el de la evidencia: un tramo no citable (b) -su cita cae en el, o su texto
lo copia- o un dia de `casos_ocultos` (c). Construye el indice como `kb` (`cli._kb_indice`, con
los dias de `casos_ocultos`). Via «cita»: su cita cae en un tramo; «dia»: trae un dia reservado;
«copia»: su texto copia un tramo. Imprime SOLO cuentas: ni ids de casos, ni texto, ni fechas.

Con `--cuarta` reproduce el criterio de la cuarta y la quinta orden (antes del cambio): toda
evidencia cuya cita pisa un segmento oculto, o que copia uno.

    uv run python docs/validation/anexos/CUARENTENA-POR-DEFECTO/kb_ocultos.py
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

from botsito.cli import _kb_indice
from botsito.corpus.cuarentena import items_ocultos

RAIZ = Path(__file__).resolve().parents[4]


def main() -> int:
    ind = _kb_indice(RAIZ)
    cuenta: Counter[tuple[str, str, str]] = Counter()
    for o in ind.evidencia_oculta.values():
        filtro = ind.filtros.get(o.video_id)
        en_tramo = filtro is not None and any(
            t1 > a and t0 < b
            for a, b, _ in filtro.tramos
            for t0, t1 in [(o.t0_ms, o.t1_ms)]
        )
        via = "dia" if o.fecha_vigilada else ("cita" if en_tramo else "copia")
        cuenta[(o.video_id, o.motivo, via)] += 1
    if "--cuarta" in sys.argv:
        cuarta = {
            iid
            for video, filtro in ind.filtros.items()
            for iid in items_ocultos(
                filtro, [(i.id, i.t0_ms, i.t1_ms) for i in ind.items if i.video_id == video]
            )
        }
        print(f"criterio de la cuarta orden (cita que pisa un segmento oculto): {len(cuarta)}")
    print(f"items de evidencia: {len(ind.items)}; ocultos por defecto: {len(ind.evidencia_oculta)}")
    print("| Video | Motivo | Via | Items |")
    print("|---|---|---|---|")
    for (video, motivo, via), n in sorted(cuenta.items()):
        print(f"| {video} | ({motivo}) | {via} | {n} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
