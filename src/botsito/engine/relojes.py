"""Con que reloj se cuentan la ventana operativa y sus sesiones (ADR-0063, ADR-0069).

La puerta del reloj de las sesiones vive en `botsito.cases.relojes` desde `trabajo/cases-rejilla`
(CASES-REJILLA.md §0.b): `cases/` cuenta la ventana de cada caso por ella, y el contrato de capas
de import-linter no le deja importar de `engine/`. Este modulo la REEXPORTA con los mismos nombres
para que el motor la siga importando de aqui; no define ninguna funcion ni clase propia
(`tests/unit/test_cases_rejilla.py`), o habria dos puertas.
"""

from __future__ import annotations

from botsito.cases.relojes import (
    DE_PARED,
    HUSO_DEL_RELOJ,
    MINUTOS_H4,
    MINUTOS_POR_DIA,
    PARAMETRO_RELOJ_SESIONES,
    PARAMETROS_DE_LA_REJILLA,
    REJILLA_H4,
    RelojError,
    RelojSesiones,
    huso_de_las_sesiones,
    huso_del_reloj,
    reloj_de_las_sesiones,
)

__all__ = [
    "DE_PARED",
    "HUSO_DEL_RELOJ",
    "MINUTOS_H4",
    "MINUTOS_POR_DIA",
    "PARAMETROS_DE_LA_REJILLA",
    "PARAMETRO_RELOJ_SESIONES",
    "REJILLA_H4",
    "RelojError",
    "RelojSesiones",
    "huso_de_las_sesiones",
    "huso_del_reloj",
    "reloj_de_las_sesiones",
]
