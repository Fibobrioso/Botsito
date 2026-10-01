"""Las rutas de codigo y documentacion citadas en PROJECT_STATE existen.

Nacio de la auditoria global del 2026-09-05: `src/botsito/evidence/historial.py` llevaba desde
ADR-0006 en `comun/` y la seccion Important Files seguia citando la ruta vieja sin que ningun test
lo viera. Desde la dieta (`trabajo/dieta-y-skills`, 2026-10-01) esa seccion vive en
docs/state/HISTORIA.md, que es archivo y puede citar rutas de entonces; la guardia pasa a mirar
PROJECT_STATE ENTERO, que es lo que una sesion lee como presente. `data/` queda fuera: no esta en
git y la CI no la tiene.
"""

from __future__ import annotations

import re
from pathlib import Path

_RUTA = re.compile(r"(?<![\w/])((?:src|docs|knowledge|tests|scripts|config)/[\w./-]+)")


def test_las_rutas_de_project_state_existen(repo: Path) -> None:
    texto = (repo / "PROJECT_STATE.md").read_text(encoding="utf-8")
    citadas = sorted({m.group(1).rstrip(".") for m in _RUTA.finditer(texto)})
    assert citadas, "PROJECT_STATE no cita ninguna ruta"
    faltan = [r for r in citadas if not (repo / r).exists() and not r.endswith("/")]
    assert faltan == [], f"rutas citadas en PROJECT_STATE que no existen: {faltan}"
