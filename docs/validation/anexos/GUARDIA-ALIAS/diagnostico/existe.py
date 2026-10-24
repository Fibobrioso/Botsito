"""Que cada forma de la raiz del repo INVENTADO llega de verdad al mismo fichero falso (solo
os.path.exists, metadatos; nada se abre). Uso: python existe.py <carpeta de trabajo>."""

import ctypes
import sys
from pathlib import Path

RAIZ = Path(sys.argv[1]) / "Bot v3 prueba"
R = str(RAIZ)
buf = ctypes.create_unicode_buffer(1024)
ctypes.windll.kernel32.GetShortPathNameW(R, buf, 1024)
CORTA = buf.value
print("8.3 distinta de la larga:", CORTA != R, "| ultimo tramo 8.3:", Path(CORTA).name)
rel = "src\\botsito\\cli.py"  # el fichero bueno, que tambien existe; mismas formas
unidad, sin = R[0], R[2:]
for etiqueta, p in (
    ("\\\\?\\", f"\\\\?\\{R}\\{rel}"),
    ("//?/", f"//?/{R.replace(chr(92), '/')}/{rel.replace(chr(92), '/')}"),
    ("UNC \\\\localhost\\C$", f"\\\\localhost\\{unidad}${sin}\\{rel}"),
    ("\\\\?\\UNC\\localhost", f"\\\\?\\UNC\\localhost\\{unidad}${sin}\\{rel}"),
    ("8.3", f"{CORTA}\\{rel}"),
    ("punto final", f"{R}.\\{rel}"),
    ("espacio final", f"{R} \\{rel}"),
):
    print(f"{etiqueta}: existe={Path(p).exists()}")
