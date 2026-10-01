"""La lista vieja de Next Action, punto a punto (revision del consultor de `trabajo/dieta-y-skills`).

Lee el Archivo 1 de docs/state/HISTORIA.md (el PROJECT_STATE.md de `df6aa2c`) y, para cada punto
que el consultor nombra, imprime su arranque LITERAL. La evidencia de que esta hecho la pone la
sesion a mano (EVIDENCIA, abajo), cada una con su commit, tag, ADR o informe; sin evidencia, el
punto se queda en PROJECT_STATE, en «Pendientes heredados (sin verificar)». Escribe en `--salida`
(fuera del repositorio) la tabla del informe y las lineas de la subseccion.

Uso: uv run python docs/validation/anexos/DIETA-Y-SKILLS/pendientes_heredados.py --salida <carpeta>
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
ORDEN = ["A2", "A3", "a", "b", "c", "d", "0", "e", "A4", "A5"] + [
    str(n) for n in (2, 6, 7, 8, 9, 10, 12, 15, 22, 23, 25, 27, 30, 34, 35, 36, 37)
]
MAX = 110
# Solo lo que tiene evidencia de estar HECHO ENTERO va solo a HISTORIA.
EVIDENCIA = {
    "a": "ADR-0060; commit `6698426` (F32), tag `stable/F36-nocturno-01oct`",
    "c": (
        "redondeo hacia fuera: ADR-0061, `2cca34d`; RN-004 en M1: ADR-0062, `2763ceb` (los dos en "
        "`stable/F36-nocturno-01oct`); break even al tocar: ADR-0065, `stable/F36h-be-al-tick`"
    ),
    "0": "ADR-0063; commit `fad0305` (F36), tag `stable/F36-nocturno-01oct`",
}
PARCIAL = {
    "A3": "encabezado: de sus ramas, a), c) y 0) estan hechas; b), d) y e), no del todo",
    "b": (
        "a medias: `liquidez_tomada` caduca al abrir la sesion en `bf1dc0b` (F33, A-46); la caja "
        "por operacion no: NOCTURNO-01OCT.md §5 la deja «detrás de F35», y nada la cierra"
    ),
    "d": (
        "a medias: RN-006 en ADR-0064 (`stable/F36d-orden-stop-pivote`); RN-007 espera el umbral "
        "(Next Action H)"
    ),
    "A4": (
        "a medias: la memoria de la suite en `stable/F31c-memoria-suite` y "
        "`stable/F31d-ci-linux-memoria`; la propuesta sobre ADR-0057 §5, sin aplicar (ningun "
        "commit la toca)"
    ),
    "22": (
        "a medias: la sesion 02 se grabo e ingirio (`stable/F19-sesion-02-videos`), pero no hay "
        "`knowledge/feedback/*-sesion-02/` y A-35 y A-44 siguen ABIERTAS"
    ),
    "2": (
        "a medias: el libro esta en el corpus (`stable/F36f-registro-marzo`), pero marzo no esta "
        "en `knowledge/cases/visto/` ni hay CONFIRM del trader"
    ),
}


def arranque(linea: str) -> str:
    t = linea.strip()
    # Se corta en el ultimo espacio antes del limite: una ruta o un id partidos dirian otra cosa.
    return t if len(t) <= MAX else t[:MAX].rsplit(" ", 1)[0].rstrip() + "…"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", required=True, type=Path)
    salida: Path = ap.parse_args().salida.resolve()
    if salida == RAIZ or RAIZ in salida.parents:
        print("ERROR: --salida tiene que estar FUERA del repositorio", file=sys.stderr)
        return 2
    salida.mkdir(parents=True, exist_ok=True)
    historia = (RAIZ / "docs" / "state" / "HISTORIA.md").read_text(encoding="utf-8")
    archivo1 = historia.split("\n# Archivo 1 ", 1)[1]
    na = archivo1.split("\n## Next Action\n", 1)[1].split("\n## ", 1)[0].split("\n")
    corte = next(i for i, ln in enumerate(na) if ln.startswith("LO QUE DECIA NEXT ACTION"))
    puntos: dict[str, str] = {}
    for ln in na[corte:]:
        m = re.match(r"\s*(?:(\d+)\.|(A\d)\.|(\w)\))\s", ln)
        if m:
            clave = next(g for g in m.groups() if g)
            # «0.» (la lista vieja) y «0)» (rama de A3) comparten clave: la rama de A3 es «0)».
            if clave == "0" and not re.match(r"\s*0\)", ln):
                continue
            puntos.setdefault(clave, ln)
    faltan = [p for p in ORDEN if p not in puntos]
    assert not faltan, faltan
    tabla = ["| Punto | Texto literal (arranque) | Evidencia de que esta hecho | Destino |"]
    tabla.append("|---|---|---|---|")
    lineas = []
    for p in ORDEN:
        texto = arranque(puntos[p]).replace("|", "\\|")
        if p in EVIDENCIA:
            ev, destino = EVIDENCIA[p], "solo HISTORIA"
        else:
            ev = PARCIAL.get(p, "sin evidencia")
            destino = "PROJECT_STATE, «Pendientes heredados (sin verificar)»"
            lineas.append(f"- {arranque(puntos[p])}")
        tabla.append(f"| {p} | {texto} | {ev} | {destino} |")
    (salida / "tabla.md").write_text("\n".join(tabla) + "\n", encoding="utf-8", newline="\n")
    (salida / "pendientes.md").write_text("\n".join(lineas) + "\n", encoding="utf-8", newline="\n")
    print(f"{len(ORDEN)} puntos; {len(EVIDENCIA)} a HISTORIA; {len(lineas)} se quedan")
    return 0


if __name__ == "__main__":
    sys.exit(main())
