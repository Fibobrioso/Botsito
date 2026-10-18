"""Fase 0 de VISOR-CONSTRUCCION, 4.c: las listas de R3.1 rehechas sobre la salida de main de hoy
(anexos/MARGEN-LOTE), frente a la de R3.1 (anexos/CORRIDA-CONSTRUCCION). Solo lee salidas
commiteadas de dias dev; no abre el visor ni lee velas."""

from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
A = RAIZ / "docs/validation/anexos"
HOY = A / "MARGEN-LOTE/diaria.DIAGNOSTICO.a35=cierre_vela_contraria.a44=sin_tope.cuenta=diaria.txt"
R31 = (
    A
    / "CORRIDA-CONSTRUCCION/diaria.DIAGNOSTICO.a35=cierre_vela_contraria.a44=sin_tope.cuenta=diaria.txt"
)
PAT_HOY = A / "MARGEN-LOTE/patrones.txt"
PAT_R31 = A / "CORRIDA-CONSTRUCCION/patrones.txt"

CATORCE = [
    ("2026-01-30", "07-11"),
    ("2026-04-17", "07-11"),
    ("2026-04-27", "11-15"),
    ("2026-07-01", "11-15"),
    ("2026-07-09", "07-11"),
    ("2026-07-14", "07-11"),
    ("2026-07-14", "11-15"),
    ("2026-07-16", "11-15"),
    ("2026-08-03", "07-11"),
    ("2026-08-11", "07-11"),
    ("2026-08-19", "11-15"),
    ("2026-08-21", "11-15"),
    ("2026-08-25", "07-11"),
    ("2026-08-27", "11-15"),
]
DOS = [("2026-01-08", "11-15"), ("2026-08-14", "07-11")]
TRES_PI = [("2026-04-16", "07-11"), ("2026-07-08", "11-15"), ("2026-07-13", "11-15")]


def cuerpo(ln: str) -> str:
    return ln.split("] ", 1)[-1] if ln.startswith("[") else ln


def secciones(ruta: Path) -> dict[str, list[str]]:
    out: dict[str, list[str]] = defaultdict(list)
    actual = None
    for ln in ruta.read_text(encoding="utf-8").splitlines():
        c = cuerpo(ln)
        if c.startswith("## Por sesion"):
            actual = "por_sesion"
            continue
        if c.startswith("### Ordenes ("):
            actual = "ordenes"
            continue
        if c.startswith("#"):
            actual = None
            continue
        if actual and c[:4].isdigit():
            out[actual].append(c)
    return out


def por_sesion(lineas: list[str]) -> dict[tuple[str, str], dict[str, str]]:
    d = {}
    for ln in lineas:
        cab, *resto = ln.split(" | ")
        dia, ses = cab.split(" ")[:2]
        campos = {"bot": resto[1].split()[-1], "rn003": resto[2].split()[-1]}
        hechos = resto[3]
        m = re.search(r"orden_dimensionada:(\S+)", hechos)
        campos["orden_dimensionada"] = m.group(1) if m else "?"
        m = re.search(r"liquidez_tomada:(\S+)", hechos)
        campos["liquidez_tomada"] = m.group(1) if m else "?"
        campos["disparadas"] = resto[4].replace("disparadas ", "")
        campos["bloqueadas"] = resto[5].replace("bloqueadas ", "")
        d[(dia, ses)] = campos
    return d


def ordenes(lineas: list[str]) -> dict[tuple[str, str], Counter[str]]:
    d: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    for ln in lineas:
        f = ln.split(" | ")
        clave = (f[0], f[1])
        d[clave][f[5] if f[5] != "rechazada" else f"rechazada:{f[6]}"] += 1
    return d


def p2(ruta: Path) -> dict[tuple[str, str], list[str]]:
    d: dict[tuple[str, str], list[str]] = defaultdict(list)
    for ln in ruta.read_text(encoding="utf-8").splitlines():
        if ln.startswith("P2 entrada"):
            fila = ln.split(": ", 1)[1]
            f = fila.split(" | ")
            m = re.search(r"\[Δentrada ([^\]]+)\]", ln)
            delta = m.group(1) if m else "?"
            d[(f[1], f[2])].append(f"{f[3]} {delta}")
    return d


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    hoy, r31 = secciones(HOY), secciones(R31)
    ps_hoy, ps_r31 = por_sesion(hoy["por_sesion"]), por_sesion(r31["por_sesion"])
    or_hoy, or_r31 = ordenes(hoy["ordenes"]), ordenes(r31["ordenes"])
    print("== P2 (entrada): R3.1 frente a hoy, por sesion ==")
    p2_hoy, p2_r31 = p2(PAT_HOY), p2(PAT_R31)
    for clave in sorted(set(p2_hoy) | set(p2_r31)):
        estado = (
            "sigue"
            if clave in p2_hoy and clave in p2_r31
            else ("nueva" if clave in p2_hoy else "desaparece")
        )
        print(
            f"{clave[0]} {clave[1]} | {estado} | hoy: {'; '.join(p2_hoy.get(clave, [])) or '-'} | R3.1: {'; '.join(p2_r31.get(clave, [])) or '-'}"
        )
    print(
        f"P2 filas hoy {sum(len(v) for v in p2_hoy.values())} en {len(p2_hoy)} sesiones; R3.1 {sum(len(v) for v in p2_r31.values())} en {len(p2_r31)}"
    )
    for titulo, lista in (
        ("== Las 14 sin orden (RN-005, RN-009, RN-001) ==", CATORCE),
        ("== Las 2 sin orden_dimensionada ==", DOS),
        ("== Las 3 de precio_invalido de R3.1 ==", TRES_PI),
    ):
        print(titulo)
        for clave in lista:
            h, r = ps_hoy.get(clave, {}), ps_r31.get(clave, {})
            print(f"{clave[0]} {clave[1]}")
            print(
                f"   R3.1: bot {r.get('bot')} | od {r.get('orden_dimensionada')} | ordenes {dict(or_r31.get(clave, {}))} | bloqueadas {r.get('bloqueadas')}"
            )
            print(
                f"   hoy : bot {h.get('bot')} | od {h.get('orden_dimensionada')} | liq {h.get('liquidez_tomada')} | rn003 {h.get('rn003')} | ordenes {dict(or_hoy.get(clave, {}))} | bloqueadas {h.get('bloqueadas')}"
            )
            print(f"         disparadas {h.get('disparadas')}")
    print("== precio_invalido por sesion: hoy y R3.1 ==")
    pi_hoy = {
        k: v["rechazada:precio_invalido"]
        for k, v in or_hoy.items()
        if v.get("rechazada:precio_invalido")
    }
    pi_r31 = {
        k: v["rechazada:precio_invalido"]
        for k, v in or_r31.items()
        if v.get("rechazada:precio_invalido")
    }
    vol_r31 = {k for k, v in or_r31.items() if v.get("rechazada:volumen_max_lotes")}
    for clave in sorted(set(pi_hoy) | set(pi_r31)):
        print(
            f"{clave[0]} {clave[1]} | hoy {pi_hoy.get(clave, 0)} | R3.1 {pi_r31.get(clave, 0)} | volumen en R3.1: {'si' if clave in vol_r31 else 'no'}"
        )
    print(
        f"total precio_invalido hoy {sum(pi_hoy.values())} en {len(pi_hoy)} sesiones; R3.1 {sum(pi_r31.values())} en {len(pi_r31)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
