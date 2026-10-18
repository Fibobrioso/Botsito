"""Medida 2 de MARGEN-LOTE.md (fase 1, ANTES del cambio): sobre una salida del arnes con las cinco
columnas de margen de «### Ordenes» (rama trabajo/margen-lote), cuantos rechazos son por
`volumen_max_lotes` y cuantas ordenes rechazaria el MARGEN, por mes, contadas por orden y por
sesion (una misma caja se recoloca varias veces, CORRIDA-CONSTRUCCION.md §3.12). Solo lee la
salida; no cambia nada ni decide nada.

Uso: uv run python docs/validation/anexos/MARGEN-LOTE/medida_2.py <salida> --fraccion 0.95

«Rechazaria el margen» se cuenta de dos maneras, con las columnas `margen requerido` y `margen
libre al colocar` de cada orden (medidas al colocar, con la unica funcion de margen del broker):
- FTMO: requerido > libre (lo que MT5 rechaza con el margen libre de ese instante);
- el bot: requerido > fraccion x libre (lo que el limite del bot recortaria; la fraccion es el
  parametro `lote_margen_libre_fraccion`, que todavia no existe en el registro cuando corre esta
  medida: por eso llega por argumento y el informe lo dice).
Las ordenes ya rechazadas por volumen se cuentan aparte y tambien dentro del margen si su margen
requerido supera el libre: son las que el margen cortaria igual aunque el volumen no existiera.
Las ordenes con `-` en el margen (sin medida) se cuentan y se listan por recuento.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path

ORDENES = "### Ordenes ("
FIN = "### Rechazos por motivo"
SIN_MEDIDA = "-"


def _cuerpo(ln: str) -> str:
    """Quita el rotulo de diagnostico ([...][...] ) que llevan todas las lineas de la salida."""
    return ln.split("] ", 1)[-1] if ln.startswith("[") else ln


def leer(ruta: Path) -> list[list[str]]:
    filas: list[list[str]] = []
    dentro = False
    for ln in ruta.read_text(encoding="utf-8").splitlines():
        c = _cuerpo(ln)
        if c.startswith(ORDENES):
            dentro = True
            continue
        if dentro and c.startswith(FIN):
            break
        if dentro and c[:4].isdigit() and " | " in c:
            filas.append(c.split(" | "))
    return filas


def main(ruta: Path, fraccion: Decimal) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    filas = leer(ruta)
    print(
        f"{ruta.name}: {len(filas)} ordenes en «### Ordenes»; fraccion del margen libre {fraccion}"
    )
    por_mes: dict[str, Counter[str]] = defaultdict(Counter)
    sesiones: dict[str, dict[str, set[tuple[str, str]]]] = defaultdict(lambda: defaultdict(set))
    for f in filas:
        dia, sesion, resultado, motivo = f[0], f[1], f[5], f[6]
        requerido, libre = f[10], f[11]
        mes = dia[:7]
        clave = (dia, sesion)
        por_mes[mes]["ordenes"] += 1
        sesiones[mes]["ordenes"].add(clave)
        por_volumen = resultado == "rechazada" and motivo == "volumen_max_lotes"
        if por_volumen:
            por_mes[mes]["rechazadas por volumen"] += 1
            sesiones[mes]["rechazadas por volumen"].add(clave)
        if requerido == SIN_MEDIDA or libre == SIN_MEDIDA:
            por_mes[mes]["sin medida de margen"] += 1
            continue
        req, lib = Decimal(requerido), Decimal(libre)
        if req > lib:
            por_mes[mes]["margen FTMO: requerido > libre"] += 1
            sesiones[mes]["margen FTMO: requerido > libre"].add(clave)
            if not por_volumen:
                por_mes[mes]["margen FTMO sin rechazo por volumen"] += 1
                sesiones[mes]["margen FTMO sin rechazo por volumen"].add(clave)
        if req > fraccion * lib:
            por_mes[mes]["bot: requerido > fraccion x libre"] += 1
            sesiones[mes]["bot: requerido > fraccion x libre"].add(clave)
    claves = (
        "ordenes",
        "rechazadas por volumen",
        "margen FTMO: requerido > libre",
        "margen FTMO sin rechazo por volumen",
        "bot: requerido > fraccion x libre",
        "sin medida de margen",
    )
    print("POR ORDEN · mes | " + " | ".join(claves))
    total: Counter[str] = Counter()
    for mes in sorted(por_mes):
        print(f"{mes} | " + " | ".join(str(por_mes[mes][k]) for k in claves))
        total.update(por_mes[mes])
    print("total | " + " | ".join(str(total[k]) for k in claves))
    print("POR SESION · mes | " + " | ".join(claves[:-1]))
    total_s: Counter[str] = Counter()
    for mes in sorted(sesiones):
        print(f"{mes} | " + " | ".join(str(len(sesiones[mes][k])) for k in claves[:-1]))
        for k in claves[:-1]:
            total_s[k] += len(sesiones[mes][k])
    print("total | " + " | ".join(str(total_s[k]) for k in claves[:-1]))
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("salida", type=Path)
    p.add_argument("--fraccion", type=Decimal, required=True)
    p.add_argument(
        "--escribir", type=Path, help="ademas de la pantalla, el mismo texto a este fichero"
    )
    a = p.parse_args()
    if a.escribir is not None:
        import io

        buffer = io.StringIO()
        real = sys.stdout
        sys.stdout = buffer  # type: ignore[assignment]
        codigo = main(a.salida, a.fraccion)
        sys.stdout = real
        a.escribir.write_text(buffer.getvalue(), encoding="utf-8")
        print(buffer.getvalue(), end="")
        raise SystemExit(codigo)
    raise SystemExit(main(a.salida, a.fraccion))
