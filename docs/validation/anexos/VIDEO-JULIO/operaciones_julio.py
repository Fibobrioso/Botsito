"""F3 de trabajo/video-julio: las operaciones de los 13 casos dev de julio, con la hora de Madrid.

Lee solo `knowledge/cases/dev/caso-eurusd-2026-07-*.yaml` (construccion, ADR-0078; 0 reservados y
0 ocultos en julio, fase 0). Imprime, por dia, cada operacion: n, sesion, direccion, entrada, stop,
instante UTC (el llenado) y la hora de Madrid (UTC+2 en julio, ADR-0069). Escribe
`operaciones-julio.txt` junto a este guion, en UTF-8 y con \\n.

Uso (la raiz del repositorio y el fichero de salida, por argumento: CLAUDE.md, «Ensayos aislados»):
  uv run python docs/validation/anexos/VIDEO-JULIO/operaciones_julio.py <raiz> <salida>
"""

from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path

import yaml

if len(sys.argv) != 3:
    sys.exit("uso: operaciones_julio.py <raiz del repositorio> <fichero de salida>")
RAIZ = Path(sys.argv[1]).resolve()
SALIDA = Path(sys.argv[2]).resolve()
DEV = RAIZ / "knowledge" / "cases" / "dev"


def main() -> int:
    lineas = ["# Operaciones de los 13 casos dev de julio de 2026 (hora de Madrid = UTC+2)"]
    total = 0
    casos = sorted(DEV.glob("caso-eurusd-2026-07-*.yaml"))
    for ruta in casos:
        doc = yaml.safe_load(ruta.read_text(encoding="utf-8"))
        ops = sorted(doc["operaciones"], key=lambda o: o["instante_utc"])
        lineas.append(f"\n## {doc['dia']} ({len(ops)} operaciones)")
        for n, op in enumerate(ops, 1):
            utc = datetime.fromisoformat(op["instante_utc"])
            madrid = (utc + timedelta(hours=2)).strftime("%H:%M:%S")
            lineas.append(
                f"{doc['dia']} #{n} | {op['sesion']} | {op['direccion']} | entrada {op['entrada']} | "
                f"stop {op['stop']} | {op['instante_utc']} | Madrid {madrid}"
            )
        total += len(ops)
    lineas.append(f"\n# {len(casos)} casos, {total} operaciones")
    SALIDA.write_text("\n".join(lineas) + "\n", encoding="utf-8", newline="\n")
    sys.stdout.write(f"OK: {len(casos)} casos, {total} operaciones -> {SALIDA.name}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
