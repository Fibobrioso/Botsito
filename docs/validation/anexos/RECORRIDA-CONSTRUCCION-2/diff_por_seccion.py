"""Un `diff` normal entre dos salidas del arnes, repartido por SECCION (D3 de
trabajo/recorrida-construccion-2): cuantas lineas quita y cuantas pone en cada «## » / «### » de
cada lado, y, para las tablas por dia, cuantas de esas lineas son de cada mes. Solo LEE el diff y
las dos salidas (ninguna vela, ningun tick) y no imprime ninguna linea de ellas.

Uso (desde la raiz):
    uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/diff_por_seccion.py \\
        <salida vieja> <salida nueva> <diff>
"""

from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HUNK = re.compile(r"^(\d+)(?:,(\d+))?([acd])(\d+)(?:,(\d+))?$")
ROTULO = "[DIAGNOSTICO"
MES = re.compile(r"^(?:trader \| |bot \| )?(\d{4}-\d{2})")


def _cuerpo(ln: str) -> str:
    return ln.split("] ", 1)[1] if ln.startswith(ROTULO) and "] " in ln else ln


def secciones(lineas: list[str]) -> list[str]:
    """La seccion de cada linea (1-indexada en la lista devuelta con un hueco en 0)."""
    actual = "(cabecera)"
    salida = [""]
    for ln in lineas:
        c = _cuerpo(ln)
        if c.startswith("## ") or c.startswith("### "):
            actual = c.split(" (")[0] if not c.startswith("### Cuenta de") else c
        salida.append(actual)
    return salida


def _rango(a: str, b: str | None) -> range:
    return range(int(a), int(b or a) + 1)


def main(vieja: Path, nueva: Path, diff: Path) -> int:
    sys.stdout.reconfigure(encoding="utf-8", newline="\n")  # type: ignore[union-attr]
    lv = vieja.read_text(encoding="utf-8").splitlines()
    ln_ = nueva.read_text(encoding="utf-8").splitlines()
    sv, sn = secciones(lv), secciones(ln_)
    quitadas: Counter[str] = Counter()
    puestas: Counter[str] = Counter()
    meses_q: dict[str, Counter[str]] = defaultdict(Counter)
    meses_p: dict[str, Counter[str]] = defaultdict(Counter)
    orden: list[str] = []
    for linea in diff.read_text(encoding="utf-8").splitlines():
        m = HUNK.match(linea)
        if not m:
            continue
        a1, a2, op, b1, b2 = m.groups()
        if op in "cd":
            for i in _rango(a1, a2):
                s = sv[i]
                quitadas[s] += 1
                mm = MES.match(_cuerpo(lv[i - 1]))
                meses_q[s][mm.group(1) if mm else "-"] += 1
                orden.append(s) if s not in orden else None
        if op in "ac":
            for i in _rango(b1, b2):
                s = sn[i]
                puestas[s] += 1
                mm = MES.match(_cuerpo(ln_[i - 1]))
                meses_p[s][mm.group(1) if mm else "-"] += 1
                orden.append(s) if s not in orden else None
    print(f"# {diff.name}: {vieja.parent.name}/{vieja.name} -> {nueva.parent.name}/{nueva.name}")
    print(f"# lineas: vieja {len(lv)}, nueva {len(ln_)}; quitadas {sum(quitadas.values())}, "
          f"puestas {sum(puestas.values())}")  # fmt: skip
    print("seccion | quitadas | puestas | quitadas por mes | puestas por mes")
    for s in orden:
        q = ", ".join(f"{k} {v}" for k, v in sorted(meses_q[s].items())) or "-"
        p = ", ".join(f"{k} {v}" for k, v in sorted(meses_p[s].items())) or "-"
        print(f"{s} | {quitadas[s]} | {puestas[s]} | {q} | {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])))
