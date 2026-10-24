"""Fase 0.c, segunda parte: que hace os.path.realpath (ntpath, GetFinalPathNameByHandle) con las
mismas formas, y cuanto tarda; es lo que ya usa `_ffmpeg_formas_de_la_ruta`. Solo metadatos.
Uso: python tiempos2.py <carpeta de trabajo>."""

import ctypes
import os
import sys
import time
from pathlib import Path

RAIZ = Path(sys.argv[1]) / "Bot v3 prueba"
R = str(RAIZ)
RF = R.replace("\\", "/")
buf = ctypes.create_unicode_buffer(1024)
ctypes.windll.kernel32.GetShortPathNameW(R, buf, 1024)
CORTA = buf.value
BUENO = "src\\botsito\\cli.py"
unidad, sin = R[0], R[2:]
formas = [
    ("absoluta", f"{R}\\{BUENO}"),
    ("\\\\?\\", f"\\\\?\\{R}\\{BUENO}"),
    ("//?/", f"//?/{RF}/{BUENO.replace(chr(92), '/')}"),
    ("UNC localhost", f"\\\\localhost\\{unidad}${sin}\\{BUENO}"),
    ("\\\\?\\UNC\\localhost", f"\\\\?\\UNC\\localhost\\{unidad}${sin}\\{BUENO}"),
    ("UNC 127.0.0.1", f"\\\\127.0.0.1\\{unidad}${sin}\\{BUENO}"),
    ("8.3", f"{CORTA}\\{BUENO}"),
    ("punto final", f"{R}.\\{BUENO}"),
    ("espacio final", f"{R} \\{BUENO}"),
    ("con . y ..", f"{R}\\.\\src\\..\\src\\botsito\\cli.py"),
    ("no existe", f"{R}\\no\\existe.txt"),
    ("8.3 no existe", f"{CORTA}\\no\\existe.txt"),
    ("\\\\?\\ no existe", f"\\\\?\\{R}\\no\\existe.txt"),
    ("otra maquina", f"\\\\otra-maquina\\C$\\x\\y.txt"),
    ("dispositivo \\\\.\\", f"\\\\.\\C:\\x\\y.txt"),
]


def resumen(x):
    return x.replace(R, "<R>").replace(CORTA, "<R 8.3>").replace(RF, "<R/>")


print(f"python {sys.version.split()[0]}")
print("| forma | os.path.realpath -> | t (us) | Path.resolve() -> | t (us) |")
print("|---|---|---|---|---|")
for etiqueta, p in formas:
    veces = 50
    t0 = time.perf_counter()
    for _ in range(veces):
        rp = os.path.realpath(p)
    t_rp = (time.perf_counter() - t0) / veces
    t0 = time.perf_counter()
    for _ in range(veces):
        rs = str(Path(p).resolve())
    t_rs = (time.perf_counter() - t0) / veces
    print(f"| {etiqueta} | {resumen(rp)} | {t_rp * 1e6:.0f} | {resumen(rs)} | {t_rs * 1e6:.0f} |")
print()
print("nombre del equipo (socket.gethostname):", "<se omite>" if True else "")
print("os.name:", os.name, "| sep:", repr(os.sep), "| altsep:", repr(os.altsep))
