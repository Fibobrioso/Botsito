"""VISOR-CONSTRUCCION (R3.2), comprobacion de P2: cuantas ordenes de la corrida 2 de `main`
se colocan en el MISMO 0 que una orden ya LLENADA de la misma sesion.

ADR-0064, decision 1: «Un punto ya usado no se vuelve a colocar. Usado es con la orden enviada,
aceptada o rechazada.» ADR-0074 §1: el 1 se recalcula «hasta el llenado». En 2026-01-29 11-15 la
traza (`traza_por_cierre.py`) ensena o17 en el punto de o16 despues de que o16 se llenara: este
guion cuenta cuantas veces pasa lo mismo en toda la salida, por el precio de la orden (el 0), que
es el nivel del punto. Es un RECUENTO por el precio: el punto exacto (nivel e instante de la vela
contraria) solo lo da la traza, y se comprueba en los dias que la tienen.

Lee solo «### Ordenes» de la salida de `main` (`anexos/MARGEN-LOTE/`, dias dev) y no copia las dos
columnas de margen, que van en USD.

    uv run python docs/validation/anexos/VISOR-CONSTRUCCION/reentradas.py
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
SALIDA = (
    RAIZ
    / "docs/validation/anexos/MARGEN-LOTE"
    / "diaria.DIAGNOSTICO.a35=cierre_vela_contraria.a44=sin_tope.cuenta=diaria.txt"
)
CABECERA = "### Ordenes (dia"
FIN = "### "


def filas() -> list[list[str]]:
    dentro = False
    salida: list[list[str]] = []
    for linea in SALIDA.read_text(encoding="utf-8").splitlines():
        texto = linea.split("] ", 1)[-1] if linea.startswith("[") else linea
        texto = texto.split("] ", 1)[-1] if texto.startswith("[") else texto
        while texto.startswith("["):
            texto = texto.split("] ", 1)[-1]
        if texto.startswith(CABECERA):
            dentro = True
            continue
        if dentro and texto.startswith(FIN):
            break
        if dentro and texto.count(" | ") >= 7:
            salida.append([c.strip() for c in texto.split(" | ")])
    return salida


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    por_sesion: dict[tuple[str, str], list[list[str]]] = defaultdict(list)
    for f in filas():
        por_sesion[(f[0], f[1])].append(f)
    total = 0
    llenadas_total = 0
    sesiones = 0
    print(
        "dia | sesion | orden | colocada UTC | 0 | resultado | la orden llenada antes en ese 0"
        " (instante del llenado)"
    )
    for (dia, ses), ordenes in sorted(por_sesion.items()):
        ordenes.sort(key=lambda f: f[3])
        llenadas: dict[str, tuple[str, str]] = {}
        en_la_sesion = 0
        for f in ordenes:
            oid, colocada, precio, resultado = f[2], f[3], f[4], f[5]
            if precio in llenadas and colocada > llenadas[precio][1]:
                antes, cuando = llenadas[precio]
                print(
                    f"{dia} | {ses} | {oid} | {colocada} | {precio} | {resultado} | "
                    f"{antes} ({cuando})"
                )
                llenadas_total += 1 if resultado == "llenada" else 0
                en_la_sesion += 1
            if resultado == "llenada" and precio not in llenadas:
                llenadas[precio] = (oid, f[7])
        total += en_la_sesion
        sesiones += 1 if en_la_sesion else 0
    print(
        f"ordenes en el 0 de una orden ya llenada de su sesion: {total}, en {sesiones} sesiones;"
        f" de ellas, llenadas: {llenadas_total}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
