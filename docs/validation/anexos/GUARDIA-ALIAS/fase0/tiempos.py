"""Fase 0.c: si GetFullPathNameW y GetLongPathNameW (ctypes) estan disponibles desde el hook, y
cuanto tardan por ruta, sobre el repo INVENTADO (`Bot v3 prueba`, creado por medir_k.py) y sobre
un fichero bueno (src/). Solo metadatos: nada se abre. Uso: python tiempos.py <carpeta de
trabajo>. Tambien: que hace posixpath (lo que haria Linux sin realpath de verdad) con las formas."""

import ctypes
import os
import posixpath
import sys
import time
from ctypes import wintypes
from pathlib import Path

RAIZ = Path(sys.argv[1]) / "Bot v3 prueba"
R = str(RAIZ)
RF = R.replace("\\", "/")
k32 = ctypes.windll.kernel32
GetFullPathNameW = k32.GetFullPathNameW
GetFullPathNameW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.LPWSTR, ctypes.c_void_p]
GetFullPathNameW.restype = wintypes.DWORD
GetLongPathNameW = k32.GetLongPathNameW
GetLongPathNameW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
GetLongPathNameW.restype = wintypes.DWORD
GetShortPathNameW = k32.GetShortPathNameW
GetShortPathNameW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
GetShortPathNameW.restype = wintypes.DWORD


def llamar(fn, ruta):
    buf = ctypes.create_unicode_buffer(32768)
    if fn is GetFullPathNameW:
        n = fn(ruta, 32768, buf, None)
    else:
        n = fn(ruta, buf, 32768)
    return buf.value if n else None


def medir(fn, ruta, veces=200):
    t0 = time.perf_counter()
    for _ in range(veces):
        salida = llamar(fn, ruta)
    dt = (time.perf_counter() - t0) / veces
    return salida, dt


CORTA = llamar(GetShortPathNameW, R)
BUENO = "src\\botsito\\cli.py"
unidad, sin = R[0], R[2:]
formas = [
    ("absoluta", f"{R}\\{BUENO}"),
    ("\\\\?\\", f"\\\\?\\{R}\\{BUENO}"),
    ("//?/", f"//?/{RF}/{BUENO.replace(chr(92), '/')}"),
    ("UNC localhost", f"\\\\localhost\\{unidad}${sin}\\{BUENO}"),
    ("\\\\?\\UNC\\localhost", f"\\\\?\\UNC\\localhost\\{unidad}${sin}\\{BUENO}"),
    ("8.3", f"{CORTA}\\{BUENO}"),
    ("punto final", f"{R}.\\{BUENO}"),
    ("espacio final", f"{R} \\{BUENO}"),
    ("con . y ..", f"{R}\\.\\src\\..\\src\\botsito\\cli.py"),
    ("no existe", f"{R}\\no\\existe.txt"),
    ("8.3 no existe", f"{CORTA}\\no\\existe.txt"),
]
print("| forma | GetFullPathNameW -> (resumen) | t full (us) | GetLongPathNameW -> | t long (us) | existe |")
print("|---|---|---|---|---|---|")
for etiqueta, p in formas:
    full, t_full = medir(GetFullPathNameW, p)
    larga, t_long = medir(GetLongPathNameW, full or p)

    def resumen(x):
        if x is None:
            return "None"
        return x.replace(R, "<R>").replace(CORTA, "<R 8.3>").replace(RF, "<R/>")

    print(
        f"| {etiqueta} | {resumen(full)} | {t_full * 1e6:.1f} | {resumen(larga)} | "
        f"{t_long * 1e6:.1f} | {Path(p).exists()} |"
    )

print()
print("os.path.normpath / posixpath.normpath (lo que haria Linux sin tocar el disco):")
for etiqueta, p in formas[:5]:
    print(f"- {etiqueta}: nt={os.path.normpath(p).replace(R, '<R>')!r} posix={posixpath.normpath(p).replace(R, '<R>').replace(RF, '<R/>')!r}")
print()
print("normcase de la guardia vs raiz (cuantos coinciden sin canonizar):")
sys.path.insert(0, str(Path(sys.argv[2]) / ".claude" / "hooks"))
import guardia  # noqa: E402

pol = guardia.Politica(RAIZ)
for etiqueta, p in formas:
    print(f"- {etiqueta}: relativa={pol.relativa(guardia._absoluta(p, R))!r}")
