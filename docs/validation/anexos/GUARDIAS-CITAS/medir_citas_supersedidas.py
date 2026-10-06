"""Fase 0 de trabajo/guardias-citas, punto a): citas a items de evidencia SUPERSEDIDOS.

Solo ids y el campo `supersede` de los items (via `cargar_evidencia`): no imprime ninguna cita ni
ningun texto de la evidencia. Recorre los ficheros VERSIONADOS (`git ls-files`) y, por cada linea
que nombre un id supersedido, da fichero, linea, id y su sustituto.

Uso: uv run python docs/validation/anexos/GUARDIAS-CITAS/medir_citas_supersedidas.py [<repo>]
"""

from __future__ import annotations

import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

from botsito.evidence.modelo import cargar_evidencia

ID_EV = re.compile(r"\bev-[a-z0-9]+-\d{6}-[0-9a-f]{8}\b")


def main(repo: Path) -> int:
    items = cargar_evidencia(repo / "knowledge" / "evidence")
    sustituto = {it.supersede: it.id for it in items if it.supersede}
    print(f"items de evidencia: {len(items)}; supersedidos: {len(sustituto)}")
    for viejo in sorted(sustituto):
        print(f"  {viejo} -> {sustituto[viejo]}")
    versionados = subprocess.run(
        ["git", "-c", "core.quotepath=off", "ls-files", "-z"],
        cwd=repo, capture_output=True, check=True,
    ).stdout.decode("utf-8").split("\0")
    por_fichero: Counter[str] = Counter()
    filas: list[str] = []
    for ruta in sorted(r for r in versionados if r):
        p = repo / ruta
        if not p.is_file():
            continue
        try:
            texto = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for n, linea in enumerate(texto.splitlines(), 1):
            for ev in ID_EV.findall(linea):
                if ev in sustituto:
                    por_fichero[ruta] += 1
                    filas.append(f"{ruta}:{n}: {ev} (sustituto {sustituto[ev]})")
    print("\ncitas a supersedidos por fichero (todos los versionados):")
    for ruta, c in sorted(por_fichero.items()):
        print(f"  {c:4d}  {ruta}")
    vigilados = ("knowledge/spec/", "docs/spec/")
    print("\nen knowledge/spec/ y docs/spec/, una por linea:")
    dentro = [f for f in filas if f.startswith(vigilados)]
    for f in dentro:
        print(f"  {f}")
    print(f"TOTAL en knowledge/spec/ y docs/spec/: {len(dentro)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()))
