"""Como resuelve Windows las rutas que empiezan por dos barras y un espacio o tabulador.

Solo apunta a C:/Windows/win.ini (no es del repo). Cada forma en un subproceso con tope de 20 s,
para medir tambien si se cuelga (una busqueda de red).
"""

import os
import subprocess
import sys
import time

B = "\\"
FORMAS = {
    "espacio-localhost-C$": B + B + " localhost" + B + "C$" + B + "Windows" + B + "win.ini",
    "tab-localhost-C$": B + B + "\tlocalhost" + B + "C$" + B + "Windows" + B + "win.ini",
    "espacio-puntopunto-unidad": B + B + " x" + B + ".." + B + "C:" + B + "Windows" + B + "win.ini",
    "barras-espacio-puntopunto-unidad": "// x/../C:/Windows/win.ini",
    "espacio-puntopunto-x2": B + B + " x" + B + ".." + B + ".." + B + "Windows" + B + "win.ini",
    "espacio-punto-dispositivo": B + B + " ." + B + "C:" + B + "Windows" + B + "win.ini",
    "espacio-interrogacion": B + B + " ?" + B + "C:" + B + "Windows" + B + "win.ini",
    "espacio-solo": B + B + " " + B + "C:" + B + "Windows" + B + "win.ini",
    "f1-literal": "// CAPA_HASH = SHA-256 de este fichero sin su linea (docs/validation/CAPA-GENERADA.md).",
    "espacio-puntopunto-raiz": "// x/../../Windows/win.ini",
    "blanco-interior-puntopunto-unidad": B
    + B
    + " a b"
    + B
    + ".."
    + B
    + "C:"
    + B
    + "Windows"
    + B
    + "win.ini",
    "blanco-interior-puntopunto-x2": "// a b/../../Windows/win.ini",
    "control-localhost-sin-espacio": B + B + "localhost" + B + "C$" + B + "Windows" + B + "win.ini",
}

HIJO = r"""
import os, sys, time
r = sys.argv[1]
t = time.time()
out = {}
for nombre, f in (("abspath", os.path.abspath), ("realpath", os.path.realpath), ("normpath", os.path.normpath)):
    try:
        out[nombre] = f(r)
    except Exception as e:
        out[nombre] = "EXC " + type(e).__name__
try:
    with open(r, "rb") as fh:
        out["open"] = "ABRE %d bytes" % len(fh.read())
except Exception as e:
    out["open"] = "NO ABRE " + type(e).__name__ + " " + str(getattr(e, "winerror", ""))
out["isabs"] = os.path.isabs(r)
out["seg"] = round(time.time() - t, 2)
print(repr(out))
"""

for nombre, ruta in FORMAS.items():
    t = time.time()
    try:
        p = subprocess.run(
            [sys.executable, "-c", HIJO, ruta], capture_output=True, text=True, timeout=20
        )
        print(nombre, "|", repr(ruta), "|", p.stdout.strip() or p.stderr.strip()[-300:])
    except subprocess.TimeoutExpired:
        print(nombre, "|", repr(ruta), "| TIMEOUT 20 s")
print("os.name =", os.name)
