"""Un perfil de cuenta SINTETICO: el de FTMO con `firma_stops_level_puntos` devuelto a UNKNOWN.

Desde ADR-0071 (rama `trabajo/demo-ejecucion-1`) el perfil real fija el stops level en 0, medido en
la demo de FTMO, y el broker ya no se niega a colocar una orden stop. La negativa por defecto de
ADR-0057 §5 -sin stops level, una orden stop no se coloca y lo dice nombrando A-27- sigue en el
codigo para cualquier perfil que no lo tenga, y se prueba con esta copia (orden del consultor del
2026-10-09, punto 3: ningun test de esa negativa se borra; se pasa a un perfil sintetico). Es la
misma forma que `_registro_con_a47_unknown` de `test_selector_orden_stop.py`."""

from __future__ import annotations

import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
PERFIL_REAL = RAIZ / "knowledge" / "cuentas" / "ftmo-2step-swing-100k.yaml"
_BLOQUE = re.compile(
    r"(  - nombre: firma_stops_level_puntos\n(?:    (?!estado:).*\n|      .*\n)*)"
    r"    estado: CONFIRMED\n    valor: 0\n(    consumido_por: \[F24\]\n)"
    r"    fuente: \{tipo: decision, id: ADR-\d{4}\}\n"
)


def perfil_con_stops_level_unknown(carpeta: Path) -> Path:
    """Escribe en `carpeta` una copia del perfil real con el stops level en UNKNOWN y sin valor,
    con el MISMO nombre de fichero (el nombre del perfil es su nombre de fichero, ADR-0050)."""
    texto = PERFIL_REAL.read_text(encoding="utf-8")
    nuevo, n = _BLOQUE.subn(r"\1    estado: UNKNOWN\n\2", texto)
    assert n == 1, "el bloque de firma_stops_level_puntos del perfil real cambio de forma"
    copia = carpeta / PERFIL_REAL.name
    copia.write_text(nuevo, encoding="utf-8")
    return copia
