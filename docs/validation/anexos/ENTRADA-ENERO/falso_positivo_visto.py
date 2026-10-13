"""Fase 0.b de trabajo/entrada-enero: el falso positivo de `cases/visto.py:requisitos`.

La condicion 2 de ADR-0042 §2 (la lectura COMPLETA del libro declarada en HOLDOUT-EXPOSICIONES) se
comprueba buscando el NOMBRE del fichero en el documento. El de enero ya aparece en la fila del
2026-10-06, que declara solo dos columnas. Se mide EN MEMORIA, sin escribir nada: se da a
`requisitos` una configuracion del kit con el tramo de enero que la fase 2 escribira (2 al 30, el
sha del manifiesto) y se mira que condiciones fallan, con el documento tal como esta hoy.

  uv run python falso_positivo_visto.py <raiz del repo>
"""

from __future__ import annotations

import dataclasses
import sys
from pathlib import Path

RAIZ = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(RAIZ / "src"))

from botsito.cases import visto  # noqa: E402

MES = "2026-01"
SHA = "ee4ade46094c73c1f1de0043acc5345cf7fa42c729b71a4b57d781002554ab86"

print(f"hoy, sin tramo: {visto.requisitos(RAIZ, MES)}")

original = visto.cargar_config


def con_enero(ruta: Path):  # type: ignore[no-untyped-def]
    c = original(ruta)
    return dataclasses.replace(
        c,
        cobertura={**c.cobertura, MES: (("2026-01-02", "2026-01-30"),)},
        materiales={**c.materiales, SHA: MES},
    )


visto.cargar_config = con_enero  # type: ignore[assignment]
problemas = visto.requisitos(RAIZ, MES)
print(f"con el tramo de la fase 2 en memoria y SIN fila nueva: {problemas or 'NINGUNO: pasa'}")
