"""RESPALDO-M1 (encargo, fase 2; respuesta del consultor a la PARADA, punto 5): las 8 sesiones de
S-14 de la sesion 6 (BARRIDO-SESION-6.md §1.d, filas 18, 4, 6, 9, 17 y 20, y las de reserva 26 y
10), en la diaria de RECORRIDA-CONSTRUCCION y en la nueva: si siguen siendo P6 (el bot opera y el
trader no, por `patrones.py`) y si su PRIMERA orden (canceladas incluidas, como la dibuja
`scripts/graficos_sesion.py`) tiene la misma M1 de colocacion, el mismo punto (lo que dibuja el
grafico), el mismo precio y el mismo lado.

`### Ordenes` no trae el lado: se deduce de la caja 1, que en una venta queda por encima del precio
y en una compra por debajo (comprobado en las 291 llenadas de la diaria de RECORRIDA contra el lado
de `entradas-antes-alternancia.txt`: 291 cuadran, RESPALDO-M1.md §3).

Solo LEE las dos salidas que recibe por argumento. SIN NINGUN R: ni el resultado de las
operaciones ni el de la sesion; solo patron, instantes del dia dev, precios de la orden y lado.

    uv run python docs/validation/anexos/RESPALDO-M1/sesiones_s14.py <diaria vieja> <diaria nueva>
"""

from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import patrones  # noqa: E402  (la copia de esta carpeta)

ROTULO = "[DIAGNOSTICO"
# (fila de BARRIDO-SESION-6.md §1.d, dia, sesion), en el orden de la decision 2 del consultor
SESIONES = (
    (18, "2026-07-02", "07-11"),
    (4, "2026-01-15", "11-15"),
    (6, "2026-01-22", "07-11"),
    (9, "2026-04-08", "07-11"),
    (17, "2026-04-28", "11-15"),
    (20, "2026-08-05", "11-15"),
    (26, "2026-08-18", "07-11"),
    (10, "2026-04-10", "11-15"),
)


def sin_rotulo(ln: str) -> str:
    return ln.split("] ", 1)[1] if ln.startswith(ROTULO) and "] " in ln else ln


def primeras(ruta: Path) -> dict[tuple[str, str], tuple[str, str, str, str, str]]:
    """(dia, sesion) -> (id, colocada, precio, punto, lado) de la primera orden colocada."""
    salida: dict[tuple[str, str], tuple[str, str, str, str, str]] = {}
    seccion = ""
    for crudo in ruta.read_text(encoding="utf-8").splitlines():
        ln = sin_rotulo(crudo)
        if ln.startswith("### "):
            seccion = ln
            continue
        if not (seccion.startswith("### Ordenes (") and ln.startswith("20")):
            continue
        p = ln.split(" | ")
        lado = "-" if p[16] == "-" else ("venta" if Decimal(p[16]) > Decimal(p[4]) else "compra")
        clave = (p[0], p[1])
        if clave not in salida or p[3] < salida[clave][1]:
            salida[clave] = (p[2], p[3], p[4], p[15], lado)
    return salida


def p6(ruta: Path) -> dict[tuple[str, str], int]:
    """(dia, sesion) -> filas P6 del bot en la sesion."""
    filas, sesgo = patrones.leer(ruta)
    salida: dict[tuple[str, str], int] = {}
    for patron, _detalle, _marca, fila in patrones.clasificar(filas, sesgo):
        if patron.startswith("P6"):
            p = fila.split(" | ")
            salida[(p[1], p[2])] = salida.get((p[1], p[2]), 0) + 1
    return salida


def main(vieja: Path, nueva: Path) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    pv, pn = p6(vieja), p6(nueva)
    ov, on = primeras(vieja), primeras(nueva)
    print(f"# Las 8 sesiones de S-14: {vieja.name} (vieja) frente a {nueva.name} (nueva); sin R")
    print(
        "fila | dia | sesion | P6 vieja (filas) | P6 nueva (filas) | primera orden vieja (id, "
        "colocada UTC, precio, punto, lado) | primera orden nueva | "
        "M1, punto, precio y lado iguales"
    )
    cambian = 0
    for fila, dia, ses in SESIONES:
        clave = (dia, ses)
        a, b = ov.get(clave), on.get(clave)
        iguales = a is not None and b is not None and a[1:] == b[1:]
        sigue = clave in pv and clave in pn
        cambian += not (iguales and sigue)
        print(
            f"{fila} | {dia} | {ses} | {'si' if clave in pv else 'NO'} ({pv.get(clave, 0)}) | "
            f"{'si' if clave in pn else 'NO'} ({pn.get(clave, 0)}) | "
            f"{', '.join(a) if a else '-'} | {', '.join(b) if b else '-'} | "
            f"{'si' if iguales else 'NO'}"
        )
    print(f"sesiones que cambian (dejan de ser P6 o cambia su primera orden): {cambian}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    sys.exit(main(Path(sys.argv[1]), Path(sys.argv[2])))
