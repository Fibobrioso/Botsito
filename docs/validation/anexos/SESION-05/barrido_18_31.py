"""Barrido ancho para la decision (4) del consultor (trabajo/sesion-05): TODA linea de la filtrada
con un entero suelto de 18 a 31 (no pegado a una letra, como el codigo S25), impresa con esos
numeros sustituidos por [N] ANTES de imprimir. Cubre lo que detector_julio.py no veia: un dia sin
la palabra «julio» ni «dia» en la misma linea o en la contigua.

Uso: python barrido_18_31.py <filtrada.md>
"""

import re
import sys
from pathlib import Path

LINEA = re.compile(r"^\[(\d+:\d\d)\] (.*)$")
ALTO = re.compile(r"(?<![\w.,])(\d{1,2})(?![\d]|[.,]\d)")


def main() -> int:
    ruta = Path(sys.argv[1])
    n = 0
    for crudo in ruta.read_text(encoding="utf-8").splitlines():
        m = LINEA.match(crudo)
        if not m:
            continue
        texto = m.group(2)
        if not any(18 <= int(x.group(1)) <= 31 for x in ALTO.finditer(texto)):
            continue
        n += 1
        mascara = ALTO.sub(lambda x: "[N]" if 18 <= int(x.group(1)) <= 31 else x.group(0), texto)
        print(f"[{m.group(1)}] {mascara}")
    print(f"lineas con un entero suelto de 18 a 31: {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
