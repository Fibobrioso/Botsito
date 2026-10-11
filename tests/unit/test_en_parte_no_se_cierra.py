"""Una respuesta «en parte» de una sesion no cierra su ambiguedad (encargo de
`trabajo/activar-sesion-04`): lo que la tabla final de cada SESION-0N-EXTRACCION.md da SOLO como
«en parte» (o «resuelve en parte»), sin ninguna fila que lo de como «resuelve», no puede estar
RESUELTA en ambiguedades.yaml. Una DECIDIDA no entra aqui: la cierra un ADR, no una sesion. La
funcion nombra la condicion y se rompe a proposito con un YAML sintetico."""

from __future__ import annotations

import re
from pathlib import Path

from botsito.cases.ambiguedades import cargar_ambiguedades

RAIZ = Path(__file__).resolve().parents[2]
EXTRACCIONES = sorted((RAIZ / "docs" / "validation").glob("SESION-0*-EXTRACCION.md"))
VEREDICTO = re.compile(r"^(no resuelve|resuelve en parte|resuelve|en parte)", re.IGNORECASE)


def veredictos(extraccion: str) -> dict[str, set[str]]:
    """Por ambiguedad, los veredictos de la tabla FINAL: «resuelve», «en parte» o «no resuelve».
    La tabla final es la del ultimo `## ` que nombra una «Tabla»; sin ella, nada."""
    secciones = [s for s in re.split(r"(?m)^(?=## )", extraccion) if s.startswith("## ")]
    tablas = [s for s in secciones if "Tabla" in s.split("\n", 1)[0]]
    salida: dict[str, set[str]] = {}
    if not tablas:
        return salida
    for fila in tablas[-1].splitlines():
        if not fila.startswith("|") or set(fila) <= set("|-: "):
            continue
        celdas = [c.strip() for c in fila.strip().strip("|").split("|")]
        for k, celda in enumerate(celdas[1:], start=1):
            m = VEREDICTO.match(celda.replace("*", "").strip())
            if not m:
                continue
            veredicto = m.group(1).lower()
            if veredicto == "resuelve en parte":
                veredicto = "en parte"
            for aid in re.findall(r"\bA-\d+\b", " ".join(celdas[:k])):
                salida.setdefault(aid, set()).add(veredicto)
            break
    return salida


def solo_en_parte(extracciones: list[str]) -> set[str]:
    """Las ambiguedades cuya ULTIMA sesion (las extracciones vienen en orden) las da solo como
    «en parte»: una sesion posterior manda sobre la anterior (A-44 fue «resuelve con lectura
    nueva» en la 3, PARO en la activacion, y es «en parte» en la 4)."""
    ultimo: dict[str, set[str]] = {}
    for texto in extracciones:
        for aid, v in veredictos(texto).items():
            ultimo[aid] = set(v)
    return {aid for aid, v in ultimo.items() if "en parte" in v and "resuelve" not in v}


def en_parte_cerradas(extracciones: list[str], estados: dict[str, str]) -> list[str]:
    return sorted(
        f"{aid} ({estados[aid]})"
        for aid in solo_en_parte(extracciones)
        if estados.get(aid) == "RESUELTA"
    )


def _estados() -> dict[str, str]:
    ambs = cargar_ambiguedades(RAIZ / "knowledge" / "spec" / "ambiguedades.yaml")
    return {a.id: a.estado for a in ambs}


def test_ninguna_en_parte_esta_resuelta() -> None:
    textos = [p.read_text(encoding="utf-8") for p in EXTRACCIONES]
    assert en_parte_cerradas(textos, _estados()) == []


def test_la_sesion_4_deja_en_parte_lo_que_dice_su_tabla() -> None:
    """Sin esto el test anterior podria pasar leyendo nada."""
    textos = [p.read_text(encoding="utf-8") for p in EXTRACCIONES]
    assert {"A-13", "A-32", "A-35", "A-43", "A-44", "A-50", "A-53"} <= solo_en_parte(textos)
    # A-49 es mezclada (S-4 resuelve; S-1 y S-2 en parte): no es «solo en parte»
    assert "A-49" not in solo_en_parte(textos)


TABLA = """# SESION-09-EXTRACCION

## 5. Tabla final

| Código | Ambigüedad | Tramo | Propuesta |
|---|---|---|---|
| S-1 | A-13 | 0:00–0:01 | en parte |
| S-2 | A-18 | 0:01–0:02 | **resuelve**: lo que sea |
| S-3 | A-49 | 0:02–0:03 | resuelve en parte |
| S-4 | A-49 | 0:03–0:04 | resuelve |
| S-5 | A-50 | 0:04–0:05 | no resuelve |
"""


ANTERIOR = """# SESION-08-EXTRACCION

## 5. Tabla final

| Código | Ambigüedad | Tramo | Propuesta |
|---|---|---|---|
| S-1 | A-13 | 0:00–0:01 | resuelve con lectura NUEVA |
| S-2 | A-50 | 0:01–0:02 | en parte |
"""


def test_se_rompe_a_proposito_si_una_en_parte_figura_resuelta() -> None:
    assert solo_en_parte([TABLA]) == {"A-13"}
    # la sesion posterior manda: A-13 pasa a «en parte» y A-50 a «no resuelve»
    assert solo_en_parte([ANTERIOR, TABLA]) == {"A-13"}
    assert solo_en_parte([ANTERIOR]) == {"A-50"}
    assert en_parte_cerradas([TABLA], {"A-13": "ABIERTA", "A-18": "RESUELTA"}) == []
    assert en_parte_cerradas([TABLA], {"A-13": "RESUELTA", "A-18": "RESUELTA"}) == [
        "A-13 (RESUELTA)"
    ]
