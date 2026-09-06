"""Las rutas de codigo y documentacion citadas en PROJECT_STATE (Important Files) existen.

Nacio de la auditoria global del 2026-09-05: `src/botsito/evidence/historial.py` llevaba desde
ADR-0006 en `comun/` y la seccion seguia citando la ruta vieja sin que ningun test lo viera.
"""

from __future__ import annotations

import re
from pathlib import Path

from botsito.cli import _read_section

_RUTA = re.compile(r"(?<![\w/])((?:src|docs|knowledge|data|tests|scripts|config)/[\w./-]+)")


def test_important_files_existen(repo: Path) -> None:
    texto = (repo / "PROJECT_STATE.md").read_text(encoding="utf-8")
    seccion = _read_section(texto, "Important Files")
    citadas = sorted({m.group(1).rstrip(".") for m in _RUTA.finditer(seccion)})
    assert citadas, "la seccion Important Files no cita ninguna ruta"
    faltan = [r for r in citadas if not (repo / r).exists() and not r.endswith("/")]
    assert faltan == [], f"rutas citadas en Important Files que no existen: {faltan}"
