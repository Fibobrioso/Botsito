"""VISOR-CONSTRUCCION (R3.2), las sesiones sin orden: el resumen, por sesion, de los tramos de gates
que `traza_por_cierre.py --gates` deja en `dias/<fecha>.traza.txt`.

Para cada sesion pedida cuenta los cierres de M1 por la combinacion de RN-005
(`se_desarrolla_en_el_lado_de_ruido`), RN-009 (`zonas_desarrolladas_superan`) y RN-001
(`en_ventana`, con los `detenido_por_*` encendidos), y da el primer cierre de cada combinacion. No
lee nada mas que esas trazas, que ya cumplen la regla de la rama (solo el dia dev, nada en dinero).

    uv run python docs/validation/anexos/VISOR-CONSTRUCCION/resumen_gates.py <fecha> <sesion> ...
        (pares fecha sesion: 2026-01-30 07-11 2026-04-17 07-11 ...)
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

DIAS = Path(__file__).resolve().parent / "dias"
SESION = re.compile(r"^== Sesion (\S+):")
INSTANTE = r"(\d\d:\d\d:\d\dZ \([^)]*\))"
TRAMO = re.compile(rf"^    {INSTANTE} - {INSTANTE}, (\d+) \| (.*)$")
CABECERA_GATES = "  gates, en tramos"


def _valor(campo: str) -> str:
    return campo.split(",", 1)[0].strip()


def resumen(fecha: str, sesion: str) -> list[str]:
    ruta = DIAS / f"{fecha}.traza.txt"
    salida = [f"== {fecha} {sesion}"]
    if not ruta.exists():
        return [*salida, "  sin traza"]
    dentro_sesion = dentro_gates = False
    cuenta: Counter[tuple[str, str, str]] = Counter()
    primero: dict[tuple[str, str, str], str] = {}
    max_zonas = 0
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        m = SESION.match(linea)
        if m:
            dentro_sesion = m.group(1) == sesion
            dentro_gates = False
            continue
        if not dentro_sesion:
            continue
        if linea.startswith(CABECERA_GATES):
            dentro_gates = True
            continue
        if dentro_gates and not linea.startswith("    "):
            dentro_gates = False
        if not dentro_gates:
            continue
        t = TRAMO.match(linea)
        if t is None:
            continue
        ruido, superan, ventana = (c.strip() for c in t.group(4).split(" | "))
        partes_sup = superan.split(",")
        if len(partes_sup) > 1 and partes_sup[1].strip().isdigit():
            max_zonas = max(max_zonas, int(partes_sup[1]))
        # «NO, sin zona o sin toma» (antes de la toma, o sin caja) no es un cierre libre de gates
        t_ruido = "sin zona" if "sin zona o sin toma" in ruido else _valor(ruido)
        clave = (t_ruido, _valor(superan), ventana)
        cuenta[clave] += int(t.group(3))
        primero.setdefault(clave, t.group(1))
    if not cuenta:
        return [*salida, "  sin tramos de gates"]
    salida.append(
        "  cierres por (RN-005 lado de ruido | RN-009 zonas de control > tope | RN-001 en_ventana,"
        " detenidos): n, desde"
    )
    for clave, n in sorted(cuenta.items(), key=lambda kv: primero[kv[0]]):
        salida.append(f"    {clave[0]} | {clave[1]} | {clave[2]}: {n}, desde {primero[clave]}")
    salida.append(f"  zonas de control, como mucho: {max_zonas}")
    return salida


def main(args: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    if len(args) % 2:
        print("pares fecha sesion")
        return 2
    for i in range(0, len(args), 2):
        print("\n".join(resumen(args[i], args[i + 1])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
