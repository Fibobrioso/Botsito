# ruff: noqa: E501  (textos de salida)
"""Recuentos sobre DOS SALIDAS YA VISTAS del arnes (docs/validation/anexos/RESPALDO-M1/):
cuenta-arrastrada.txt (la linea base vigente, ADR-0070 §3, NOTA del 2026-10-29) y
diaria.DIAGNOSTICO.cuenta=diaria.txt (un DIAGNOSTICO, --diagnostico-cuenta-diaria: no cuenta por
ADR-0070 §3; solo contraste descriptivo). No corre el arnes ni lee nada mas.

c) operaciones del trader en dias en que la cuenta arrastrada ya estaba congelada: dias de la curva
   de equity sin equity minima ("-") y sin ninguna orden del bot, posteriores al ultimo dia con orden.
e) |Δentrada| y |Δinstante| de las PAREJA y de las SIN PAREJA con «bot mas cercano en la sesion»,
   por tramos.

Uso: python recuentos_vistos.py <carpeta RESPALDO-M1>
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

ARRASTRADA = "cuenta-arrastrada.txt"
DIARIA = "diaria.DIAGNOSTICO.cuenta=diaria.txt"

R_DELTA = re.compile(r"Δentrada ([+-]?\d+) puntos, Δinstante ([+-])(\d+) min (\d+) s")


def seccion(lineas: list[str], cabecera: str) -> list[str]:
    dentro, salida = False, []
    for ln in lineas:
        if ln.startswith(cabecera):
            dentro = True
            continue
        if dentro and (ln.startswith("## ") or ln.startswith("### ")):
            break
        if dentro:
            salida.append(ln)
    return salida


def tramo_puntos(p: int) -> str:
    p = abs(p)
    if p <= 3:
        return "0-3"
    if p <= 5:
        return "4-5"
    if p <= 10:
        return "6-10"
    return ">10"


def tramo_min(seg: int) -> str:
    if seg <= 15 * 60:
        return "0-15"
    if seg <= 30 * 60:
        return "16-30"
    return ">30"


def deltas(lineas: list[str]) -> dict[str, tuple[Counter[str], Counter[str], int]]:
    por_op = seccion(lineas, "### Por operacion")
    grupos: dict[str, list[tuple[int, int]]] = {
        "PAREJA": [],
        "SIN PAREJA, bot mas cercano (todas)": [],
        "SIN PAREJA, bot mas cercano del MISMO lado": [],
        "SIN PAREJA, bot mas cercano del OTRO lado": [],
    }
    for ln in por_op:
        if not ln.startswith("trader |"):
            continue
        campos = ln.split(" | ")
        lado, resultado = campos[3], campos[6]
        m = R_DELTA.search(resultado)
        if resultado.startswith("PAREJA"):
            clave = "PAREJA"
        elif "bot mas cercano en la sesion: " in resultado:
            lado_bot = resultado.split("bot mas cercano en la sesion: ", 1)[1].split(" ", 1)[0]
            assert m is not None, ln
            seg = int(m.group(3)) * 60 + int(m.group(4))
            grupos["SIN PAREJA, bot mas cercano (todas)"].append((int(m.group(1)), seg))
            clave = (
                "SIN PAREJA, bot mas cercano del MISMO lado"
                if lado_bot == lado
                else "SIN PAREJA, bot mas cercano del OTRO lado"
            )
        else:
            continue
        assert m is not None, ln
        seg = int(m.group(3)) * 60 + int(m.group(4))
        grupos[clave].append((int(m.group(1)), seg))
    return {
        k: (Counter(tramo_puntos(p) for p, _ in v), Counter(tramo_min(s) for _, s in v), len(v))
        for k, v in grupos.items()
    }


def congelados(lineas: list[str]) -> None:
    curva = [ln.split(" | ") for ln in seccion(lineas, "### Curva de equity") if " | " in ln]
    ordenes = seccion(lineas, "### Ordenes (dia")
    dias_orden = sorted(
        {ln.split(" | ")[0] for ln in ordenes if re.match(r"\d{4}-\d{2}-\d{2} \|", ln)}
    )
    ultimo = dias_orden[-1]
    sin_marca = [c[0] for c in curva if c[3].strip() == "-"]
    tras = [c[0] for c in curva if c[0] > ultimo]
    assert set(tras) <= set(sin_marca), "un dia posterior a la ultima orden tiene equity minima"
    saldos = {c[2] for c in curva if c[0] >= ultimo}
    print(
        f"ultimo dia con alguna orden del bot: {ultimo}; dias de la curva posteriores: {len(tras)}"
    )
    print(f"saldo final en esos dias (todos iguales): {sorted(saldos)}")
    por_op = seccion(lineas, "### Por operacion")
    trader = [ln.split(" | ") for ln in por_op if ln.startswith("trader |")]
    en_tras = [t for t in trader if t[1] > ultimo]
    print(f"operaciones del trader en la salida: {len(trader)}")
    print(f"operaciones del trader en dias posteriores a {ultimo}: {len(en_tras)}")
    print(
        "  por mes: "
        + ", ".join(f"{k} {v}" for k, v in sorted(Counter(t[1][:7] for t in en_tras).items()))
    )
    print(f"operaciones del trader el propio {ultimo}: {sum(1 for t in trader if t[1] == ultimo)}")
    con_orden = {ln.split(" | ")[0] for ln in ordenes if re.match(r"\d{4}-\d{2}-\d{2} \|", ln)}
    print(f"dias con alguna orden del bot: {len(con_orden)}")


def main() -> None:
    carpeta = Path(sys.argv[1])
    for nombre in (ARRASTRADA, DIARIA):
        prefijo = "[DIAGNOSTICO-CUENTA-diaria] "
        lineas = [
            ln[len(prefijo) :] if ln.startswith(prefijo) else ln
            for ln in (carpeta / nombre).read_text(encoding="utf-8").splitlines()
        ]
        print(f"=== {nombre}")
        if nombre == ARRASTRADA:
            congelados(lineas)
        for grupo, (cp, cm, n) in deltas(lineas).items():
            print(f"{grupo}: {n}")
            print(
                "  |Δentrada| puntos: "
                + ", ".join(f"{t} {cp[t]}" for t in ("0-3", "4-5", "6-10", ">10"))
            )
            print(
                "  |Δinstante| min:   "
                + ", ".join(f"{t} {cm[t]}" for t in ("0-15", "16-30", ">30"))
            )


if __name__ == "__main__":
    main()
