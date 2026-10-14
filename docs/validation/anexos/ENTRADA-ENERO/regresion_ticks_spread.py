"""Regresion de la fase 1 de trabajo/entrada-enero: ticks_spread.py de main frente al de la rama.

Carga los dos guiones como modulos (el de main, copiado con `git show main:scripts/ticks_spread.py`
a la carpeta de trabajo, sin tocar una linea; se le da la raiz del repo por su global `RAIZ`), los
corre sobre los ticks de construccion de hoy (abril, julio y agosto, sin dias de desfase) y compara
sus salidas linea a linea, salvo la cabecera VENTANA, que cambia a proposito.

  uv run python regresion_ticks_spread.py <raiz del repo> <guion de main> <carpeta de salida>
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

raiz, guion_main, salida = Path(sys.argv[1]).resolve(), Path(sys.argv[2]), Path(sys.argv[3])


def cargar(nombre: str, ruta: Path):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


viejo = cargar("ticks_spread_main", guion_main)
viejo.RAIZ = raiz
nuevo = cargar("ticks_spread_rama", raiz / "scripts" / "ticks_spread.py")
a, b = salida / "ticks_spread_main.txt", salida / "ticks_spread_rama.txt"
assert viejo.main(["--salida", str(a)]) == 0
assert nuevo.main(["--salida", str(b)], raiz=raiz) == 0
la, lb = a.read_text(encoding="utf-8").splitlines(), b.read_text(encoding="utf-8").splitlines()
distintas = [(x, y) for x, y in zip(la, lb, strict=True) if x != y]
print(f"lineas: main {len(la)}, rama {len(lb)}; distintas {len(distintas)}")
for x, y in distintas:
    print(f"- main: {x}\n+ rama: {y}")
