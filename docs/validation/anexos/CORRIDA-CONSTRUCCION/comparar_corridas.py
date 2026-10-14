"""Compara dos salidas del arnes por (dia, sesion): que operaciones del bot y que parejas cambian
(fase 2 del encargo: «de la 3 frente a la 2, solo la lista de dias y sesiones en que cambia alguna
operacion del bot o alguna pareja, con que cambia. Sin elegir lectura»). Lee SOLO las filas de
«Diferencias por operacion» de los dos ficheros commiteados; no corre nada.

Uso: uv run python comparar_corridas.py <salida A> <salida B>
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path


def filas(ruta: Path) -> list[list[str]]:
    salida = []
    for ln in ruta.read_text(encoding="utf-8").splitlines():
        cuerpo = ln.split("] ", 1)[-1]
        if cuerpo.startswith(("trader | ", "bot | ")):
            salida.append(cuerpo.split(" | ", 6))
    return salida


Clave = tuple[str, str]


def por_sesion(ruta: Path) -> tuple[dict[Clave, set[str]], dict[Clave, set[str]]]:
    """(operaciones del bot, parejas) por (dia, sesion). Una operacion del bot con pareja no sale
    aparte: se reconstruye de la fila del trader (`PAREJA bot <instante> <entrada>`)."""
    bot: dict[tuple[str, str], set[str]] = defaultdict(set)
    parejas: dict[tuple[str, str], set[str]] = defaultdict(set)
    for quien, dia, sesion, lado, instante, entrada, resultado in filas(ruta):
        clave = (dia, sesion)
        if quien == "bot":
            bot[clave].add(f"{lado} {instante} {entrada}")
        elif resultado.startswith("PAREJA bot "):
            _, _, b_instante, b_entrada, *_ = resultado.split(" ", 4)
            bot[clave].add(f"{lado} {b_instante} {b_entrada}")
            parejas[clave].add(f"trader {instante} {entrada} <-> bot {b_instante} {b_entrada}")
    return bot, parejas


def main(a: Path, b: Path) -> int:
    sys.stdout.reconfigure(encoding="utf-8")  # por si una fila lleva «Δ»; la consola, cp1252
    bot_a, par_a = por_sesion(a)
    bot_b, par_b = por_sesion(b)
    claves = sorted(set(bot_a) | set(bot_b) | set(par_a) | set(par_b))
    cambios = 0
    for clave in claves:
        if bot_a[clave] == bot_b[clave] and par_a[clave] == par_b[clave]:
            continue
        cambios += 1
        print(f"{clave[0]} {clave[1]}:")
        for s in sorted(bot_a[clave] - bot_b[clave]):
            print(f"  bot solo en A: {s}")
        for s in sorted(bot_b[clave] - bot_a[clave]):
            print(f"  bot solo en B: {s}")
        for s in sorted(par_a[clave] - par_b[clave]):
            print(f"  pareja solo en A: {s}")
        for s in sorted(par_b[clave] - par_a[clave]):
            print(f"  pareja solo en B: {s}")
    print(
        f"A = {a.name}; B = {b.name}; sesiones con alguna diferencia: {cambios}; operaciones del "
        f"bot A {sum(len(v) for v in bot_a.values())}, B {sum(len(v) for v in bot_b.values())}; "
        f"parejas A {sum(len(v) for v in par_a.values())}, B {sum(len(v) for v in par_b.values())}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]), Path(sys.argv[2])))
