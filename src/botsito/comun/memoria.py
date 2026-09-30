"""El pico de memoria del proceso, barato y valido en Windows y en Linux (rama
`trabajo/memoria-suite`).

Lo lleva el sistema operativo, asi que leerlo no cuesta nada: no hay muestreo ni se instrumenta
cada asignacion, que es lo que hace `tracemalloc` y lo que convertia `motor arnes` en un proceso de
750 MB y tres minutos dentro de la suite. Mide el proceso entero (Python, extensiones y el propio
interprete), no solo lo que asigna Python:
- Windows: `PeakWorkingSetSize` de `GetProcessMemoryInfo`, el pico de memoria residente;
- Linux: `ru_maxrss` de `getrusage(RUSAGE_SELF)`, en KiB; macOS lo da en bytes. `exec` conserva
  en el la RSS del proceso que hizo el fork, asi que un proceso recien lanzado arranca con la de
  su padre (rama `fix/ci-linux-memoria`).
"""

from __future__ import annotations

import sys


def pico_del_proceso() -> int:
    """El pico de memoria residente de este proceso desde que arranco, en bytes."""
    if sys.platform == "win32":
        import ctypes
        from ctypes import wintypes

        class Contadores(ctypes.Structure):
            _fields_ = (
                ("cb", wintypes.DWORD),
                ("PageFaultCount", wintypes.DWORD),
                ("PeakWorkingSetSize", ctypes.c_size_t),
                ("WorkingSetSize", ctypes.c_size_t),
                ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                ("PagefileUsage", ctypes.c_size_t),
                ("PeakPagefileUsage", ctypes.c_size_t),
            )

        k32 = ctypes.WinDLL("kernel32", use_last_error=True)
        k32.GetCurrentProcess.restype = wintypes.HANDLE
        k32.K32GetProcessMemoryInfo.argtypes = (
            wintypes.HANDLE, ctypes.POINTER(Contadores), wintypes.DWORD
        )  # fmt: skip
        k32.K32GetProcessMemoryInfo.restype = wintypes.BOOL
        c = Contadores()
        c.cb = ctypes.sizeof(c)
        if not k32.K32GetProcessMemoryInfo(k32.GetCurrentProcess(), ctypes.byref(c), c.cb):
            raise OSError(ctypes.get_last_error(), "GetProcessMemoryInfo")
        return int(c.PeakWorkingSetSize)
    import resource

    maxrss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return maxrss if sys.platform == "darwin" else maxrss * 1024
