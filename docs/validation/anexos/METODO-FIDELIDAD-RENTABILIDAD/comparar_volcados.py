"""Compara los volcados de main y de la rama: hashes, que la rama empiece por main byte a byte, y
lo que la rama anade. Uso: python comparar_volcados.py <clon main> <clon rama>"""

import hashlib
import sys
from pathlib import Path

CABECERA = "## El metodo de ADR-0092"
main, rama = Path(sys.argv[1]), Path(sys.argv[2])
print(
    "fichero | sha256 main | sha256 rama | sha256 de la rama hasta la seccion nueva | igual a main"
)
for nombre in ("hueco", "stop", "viva"):
    a = (main / f"volcado-{nombre}.txt").read_bytes()
    b = (rama / f"volcado-{nombre}.txt").read_bytes()
    corte = b.index(("\n\n" + CABECERA).encode())
    prefijo = b[:corte] + b"\n"
    h = lambda x: hashlib.sha256(x).hexdigest()[:16]  # noqa: E731
    print(f"volcado-{nombre}.txt | {h(a)} | {h(b)} | {h(prefijo)} | {prefijo == a}")
    assert CABECERA.encode() not in a
print()
print("lo que la rama anade en volcado-stop.txt:")
b = (rama / "volcado-stop.txt").read_text(encoding="utf-8")
print(b[b.index(CABECERA) :])
