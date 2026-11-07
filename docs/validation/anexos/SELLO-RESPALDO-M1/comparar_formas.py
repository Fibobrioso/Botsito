"""SELLO-RESPALDO-M1, fase 0 c): compara, DIA A DIA, dos salidas de `prototipo_sello.py`.

Solo lee las dos salidas que recibe. Una OPERACION del bot es una posicion; se compara por lo que
D2 del encargo llama cambiar una operacion: que entre o no, el lado, la vela de entrada y el
resultado en R (la sesion, la salida y la fuente se ensenan tambien). Las ordenes se comparan sin
su id (que se renumera si una forma coloca una mas): colocada, tipo, lado, resultado y lo que dice
la M1 k de una cancelada en un cierre sin ticks. Nada agregado: una linea por dia.

    uv run python -B docs/validation/anexos/SELLO-RESPALDO-M1/comparar_formas.py <salida A> <salida B>
"""

from __future__ import annotations

import sys
from pathlib import Path


def leer(ruta: Path) -> dict[str, dict[str, list[str]]]:
    dias: dict[str, dict[str, list[str]]] = {}
    dia, seccion = "", ""
    for ln in ruta.read_text(encoding="utf-8").splitlines():
        if ln.startswith("## "):
            dia = ln[3:].strip()
            dias[dia] = {"ordenes": [], "posiciones": []}
        elif ln.startswith("ordenes:"):
            seccion = "ordenes"
        elif ln.startswith("posiciones:"):
            seccion = "posiciones"
        elif ln.startswith("  ") and dia:
            c = [x.strip() for x in ln.split("|")]
            if seccion == "ordenes":
                # sin id; el instante del resultado, al minuto (el 1 ms de (c2) no es un cambio)
                dias[dia]["ordenes"].append(" | ".join([c[1], c[2], c[3], c[4], c[5][:5], c[6]]))
            else:
                # sesion, lado, vela de entrada, salida y R (sin id ni instantes al ms)
                dias[dia]["posiciones"].append(" | ".join([c[1], c[2], c[4], c[5], c[7]]))
    return dias


def main(a: Path, b: Path) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    da, db = leer(a), leer(b)
    print(f"# {a.name} frente a {b.name}, por dia")
    for dia in sorted(set(da) | set(db)):
        pa, pb = da.get(dia, {}).get("posiciones", []), db.get(dia, {}).get("posiciones", [])
        oa, ob = da.get(dia, {}).get("ordenes", []), db.get(dia, {}).get("ordenes", [])
        solo_a = [x for x in pa if x not in pb]
        solo_b = [x for x in pb if x not in pa]
        ops = "operaciones IGUALES" if not solo_a and not solo_b else "operaciones DISTINTAS"
        ords = "ordenes iguales" if oa == ob else "ordenes distintas"
        print(f"## {dia}: {ops}; {ords}")
        for x in solo_a:
            print(f"  solo en {a.name}: {x}")
        for x in solo_b:
            print(f"  solo en {b.name}: {x}")
        if oa != ob:
            for x in oa:
                if x not in ob:
                    print(f"  orden solo en {a.name}: {x}")
            for x in ob:
                if x not in oa:
                    print(f"  orden solo en {b.name}: {x}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    sys.exit(main(Path(sys.argv[1]), Path(sys.argv[2])))
