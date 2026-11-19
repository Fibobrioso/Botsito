"""D0 de trabajo/activar-sesion-07: el delta FILA POR FILA de julio de 2026 entre dos corridas del
arnes, leido SOLO de sus salidas (no corre nada ni lee velas).

Uso:
  uv run python docs/validation/anexos/ACTIVAR-SESION-07/delta_julio.py \
      <patrones base> <patrones nuevo> <arnes base> <arnes nuevo>

- `<patrones ...>`: la salida de `anexos/RECORRIDA-CONSTRUCCION-2/patrones.py <arnes> --filas`
  (con los CR quitados), de la que se leen las filas de 2026-07 tras «-- filas».
- `<arnes ...>`: la salida de `motor arnes --simular`, de la que se lee SOLO el rn003 de cada
  sesion de julio en su linea de «## Por sesion» (la misma expresion que `patrones.py`). Las
  salidas del arnes se quedan en `data/`; al repositorio va solo lo que imprime este guion.

Imprime: el rn003 de cada sesion de julio en una y otra (y cuales cambian); las filas de julio que
cambian de patron, las que aparecen y las que desaparecen, cada una con su patron y su fila. Una
fila se identifica por quien, dia, sesion, lado, instante y entrada (sus seis primeros campos); el
resto de la fila (la pareja o el bot mas cercano) no forma parte de la identidad.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

MES = "2026-07"
FILA = re.compile(r"^(T0|P\d)( [^:\[]*)?((?: \[[^\]]*\])*): ((?:trader|bot) \| .*)$")
POR_SESION = re.compile(
    r"^(\d{4}-\d{2}-\d{2}) (\S+) \| trader (\d+) \| bot (\d+) \| rn003 (\S+) \|"
)
ROTULO = "[DIAGNOSTICO"


def _cuerpo(ln: str) -> str:
    if ln.startswith(ROTULO) and "] " in ln:
        return ln.split("] ", 1)[1]
    return ln


def filas_de_julio(ruta: Path) -> dict[str, list[str]]:
    """identidad -> lista de patrones (con su detalle); una identidad puede repetirse."""
    salida: dict[str, list[str]] = {}
    dentro = False
    for ln in ruta.read_text(encoding="utf-8").splitlines():
        if ln == "-- filas":
            dentro = True
            continue
        if not dentro:
            continue
        m = FILA.match(ln)
        if not m:
            continue
        fila = m.group(4)
        campos = fila.split(" | ")
        if len(campos) < 7 or not campos[1].startswith(MES):
            continue
        identidad = " | ".join(campos[:6])
        patron = f"{m.group(1)}{m.group(2) or ''}{m.group(3) or ''}"
        salida.setdefault(identidad, []).append(patron)
    return salida


def rn003_de_julio(ruta: Path) -> dict[tuple[str, str], str]:
    sesgo: dict[tuple[str, str], str] = {}
    for ln in ruta.read_text(encoding="utf-8").splitlines():
        m = POR_SESION.match(_cuerpo(ln))
        if m and m.group(1).startswith(MES):
            sesgo[(m.group(1), m.group(2))] = m.group(5)
    return sesgo


def main(pb: Path, pn: Path, ab: Path, an: Path) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    base, nuevo = filas_de_julio(pb), filas_de_julio(pn)
    sb, sn = rn003_de_julio(ab), rn003_de_julio(an)
    print(f"delta de {MES}: base {pb.name} / {ab.name}; nuevo {pn.name} / {an.name}")
    print(f"filas de {MES}: base {sum(map(len, base.values()))}, nuevo {sum(map(len, nuevo.values()))}")
    print()
    print("## rn003 por sesion (base -> nuevo)")
    cambian = 0
    for clave in sorted(set(sb) | set(sn)):
        a, b = sb.get(clave, "-"), sn.get(clave, "-")
        marca = "" if a == b else "   <- cambia"
        cambian += a != b
        print(f"{clave[0]} {clave[1]}: {a} -> {b}{marca}")
    print(f"sesiones de {MES}: {len(set(sb) | set(sn))}; cambian de rn003: {cambian}")
    print()
    cambio, aparece, desaparece = [], [], []
    for identidad in sorted(set(base) | set(nuevo)):
        a, b = sorted(base.get(identidad, [])), sorted(nuevo.get(identidad, []))
        if a == b:
            continue
        if not a:
            aparece += [(p, identidad) for p in b]
        elif not b:
            desaparece += [(p, identidad) for p in a]
        else:
            cambio.append((a, b, identidad))
    print(f"## filas que cambian de patron: {len(cambio)}")
    for a, b, identidad in cambio:
        print(f"{' + '.join(a)} -> {' + '.join(b)}: {identidad}")
    print(f"## filas que aparecen: {len(aparece)}")
    for p, identidad in aparece:
        print(f"+ {p}: {identidad}")
    print(f"## filas que desaparecen: {len(desaparece)}")
    for p, identidad in desaparece:
        print(f"- {p}: {identidad}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(*(Path(a) for a in sys.argv[1:5])))
