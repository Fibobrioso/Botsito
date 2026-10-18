"""Fase 4 de MARGEN-LOTE.md: sobre una salida del arnes CON el limite de ADR-0081 (quince columnas
en «### Ordenes» y la seccion «### Ordenes no enviadas por el bot»), por mes: los rechazos por
motivo, cuantas ordenes se colocaron con el lote limitado y por que limite, y el riesgo efectivo de
las ordenes del bot (cuantas con el riesgo entero del registro, la mediana y el minimo, en % del
saldo). Solo lee la salida; no decide nada.

Uso: uv run python docs/validation/anexos/MARGEN-LOTE/fase4_medidas.py <salida> [--escribir <txt>]

El riesgo entero se lee del registro (`riesgo_por_operacion`): una orden lo arriesga «entero» si su
columna `riesgo (% del saldo)` queda a menos de un paso de lote de el (el redondeo hacia abajo al
paso deja el riesgo un poco por debajo incluso sin limite): aqui se cuenta como entero si el lote
colocado es el lote del riesgo (columna `limite` = ninguno), y limitado si no.
"""

from __future__ import annotations

import argparse
import io
import sys
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path
from statistics import median

ORDENES = "### Ordenes ("
NO_ENVIADAS = "### Ordenes no enviadas por el bot ("
RECHAZOS = "### Rechazos por motivo"
SIN_MEDIDA = "-"


def _cuerpo(ln: str) -> str:
    return ln.split("] ", 1)[-1] if ln.startswith("[") else ln


def leer(ruta: Path) -> tuple[list[list[str]], list[list[str]], list[list[str]]]:
    ordenes: list[list[str]] = []
    no_enviadas: list[list[str]] = []
    rechazos: list[list[str]] = []
    seccion = None
    for ln in ruta.read_text(encoding="utf-8").splitlines():
        c = _cuerpo(ln)
        if c.startswith(ORDENES):
            seccion = "ordenes"
            continue
        if c.startswith(NO_ENVIADAS):
            seccion = "no_enviadas"
            continue
        if c.startswith(RECHAZOS):
            seccion = "rechazos"
            continue
        if c.startswith("### "):
            seccion = None
            continue
        if seccion and c[:4].isdigit() and " | " in c:
            {"ordenes": ordenes, "no_enviadas": no_enviadas, "rechazos": rechazos}[seccion].append(
                c.split(" | ")
            )
    return ordenes, no_enviadas, rechazos


def main(ruta: Path) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ordenes, no_enviadas, rechazos = leer(ruta)
    print(f"{ruta.name}: {len(ordenes)} ordenes, {len(no_enviadas)} no enviadas")
    print("RECHAZOS POR MOTIVO (mes | motivo | peticion | n)")
    for r in rechazos:
        print("  " + " | ".join(r))
    print(
        "LIMITE QUE MORDIO, POR ORDEN · mes | ordenes | ninguno | volumen | margen | "
        "volumen+margen | otro"
    )
    por_mes: dict[str, Counter[str]] = defaultdict(Counter)
    riesgos: dict[str, list[Decimal]] = defaultdict(list)
    sesiones_limitadas: dict[str, set[tuple[str, str]]] = defaultdict(set)
    for f in ordenes:
        mes = f[0][:7]
        limite = f[14] if len(f) > 14 else SIN_MEDIDA
        clave = limite if limite in ("ninguno", "volumen", "margen", "volumen+margen") else "otro"
        por_mes[mes][clave] += 1
        por_mes[mes]["ordenes"] += 1
        if clave not in ("ninguno", "otro"):
            sesiones_limitadas[mes].add((f[0], f[1]))
        if f[12] != SIN_MEDIDA and f[5] != "rechazada":
            riesgos[mes].append(Decimal(f[12]))
    claves = ("ordenes", "ninguno", "volumen", "margen", "volumen+margen", "otro")
    total: Counter[str] = Counter()
    for mes in sorted(por_mes):
        print(f"  {mes} | " + " | ".join(str(por_mes[mes][k]) for k in claves))
        total.update(por_mes[mes])
    print("  total | " + " | ".join(str(total[k]) for k in claves))
    print(
        "SESIONES con alguna orden limitada: "
        + ", ".join(f"{m} {len(s)}" for m, s in sorted(sesiones_limitadas.items()))
        + f"; total {sum(len(s) for s in sesiones_limitadas.values())}"
    )
    print(
        "RIESGO EFECTIVO de las ordenes colocadas (no rechazadas), % del saldo al colocar · "
        "mes | n | con el riesgo entero (limite ninguno) | mediana | minimo | maximo"
    )
    todos: list[Decimal] = []
    enteros_total = 0
    for mes in sorted(riesgos):
        rs = riesgos[mes]
        enteros = sum(
            1 for f in ordenes if f[0][:7] == mes and f[5] != "rechazada" and f[14] == "ninguno"
        )
        enteros_total += enteros
        todos += rs
        print(f"  {mes} | {len(rs)} | {enteros} | {median(rs):.3f} | {min(rs):.3f} | {max(rs):.3f}")
    if todos:
        print(
            f"  total | {len(todos)} | {enteros_total} | {median(todos):.3f} | {min(todos):.3f} | "
            f"{max(todos):.3f}"
        )
    print(
        "NO ENVIADAS por motivo: "
        + (
            ", ".join(f"{k} {v}" for k, v in sorted(Counter(f[4] for f in no_enviadas).items()))
            or "ninguna"
        )
    )
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("salida", type=Path)
    p.add_argument("--escribir", type=Path)
    a = p.parse_args()
    if a.escribir is not None:
        buffer = io.StringIO()
        real = sys.stdout
        sys.stdout = buffer  # type: ignore[assignment]
        codigo = main(a.salida)
        sys.stdout = real
        a.escribir.write_text(buffer.getvalue(), encoding="utf-8", newline="\n")
        print(buffer.getvalue(), end="")
        raise SystemExit(codigo)
    raise SystemExit(main(a.salida))
