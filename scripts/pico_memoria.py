"""El pico de memoria de `make check`, medido paso a paso (rama `trabajo/memoria-suite`).

Cada paso de `make check` corre dentro de `medir`, que ejecuta la orden y apunta su pico en un
acumulador dentro del directorio de git (`git rev-parse --git-path botsito-pico`), como el sello:
git nunca lo sigue y no entra en la huella de la guardia. `informe` imprime UNA linea con el pico
mayor y el paso que lo dio, y borra el acumulador; `empezar` lo borra al principio.

QUE SE MIDE, que no es lo mismo en los dos sistemas y la linea lo dice:
- Windows: un Job Object al que se asigna este proceso ANTES de lanzar la orden, asi que todos sus
  descendientes (uv, python, pytest) caen dentro. El Job da la memoria COMPROMETIDA (privada): el
  pico de la SUMA de sus procesos a la vez y el del mayor proceso. Se apunta la suma, que es lo que
  presiona al sistema; incluye este proceso medidor, unos 10-20 MiB.
- Linux y macOS: `getrusage(RUSAGE_CHILDREN).ru_maxrss`, la RSS maxima del MAYOR descendiente
  esperado. No hay suma: el sistema no la da sin muestrear.

Barato: ni muestreo ni hilos; el sistema lleva la cuenta y se lee una vez al acabar.

Uso:
    python scripts/pico_memoria.py empezar
    python scripts/pico_memoria.py medir <paso> -- <orden> [args...]
    python scripts/pico_memoria.py informe
    python scripts/pico_memoria.py ejecutar -- <orden> [args...]   (mide una orden suelta)
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

NOMBRE = "botsito-pico"
MIB = 2**20


def _windows_job() -> object:
    """Crea un Job Object y mete en el a este proceso: sus hijos heredan el Job."""
    import ctypes

    k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    k32.CreateJobObjectW.restype = ctypes.c_void_p
    k32.CreateJobObjectW.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p]
    k32.GetCurrentProcess.restype = ctypes.c_void_p
    k32.AssignProcessToJobObject.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    job = k32.CreateJobObjectW(None, None)
    if not job:
        raise OSError(ctypes.get_last_error(), "CreateJobObjectW")
    if not k32.AssignProcessToJobObject(job, k32.GetCurrentProcess()):
        raise OSError(ctypes.get_last_error(), "AssignProcessToJobObject")
    return job


def _windows_pico(job: object) -> tuple[int, int]:
    """(pico de la suma de los procesos del Job, pico del mayor proceso), en bytes."""
    import ctypes

    class Basica(ctypes.Structure):
        _fields_ = [
            ("PerProcessUserTimeLimit", ctypes.c_int64),
            ("PerJobUserTimeLimit", ctypes.c_int64),
            ("LimitFlags", ctypes.c_uint32),
            ("MinimumWorkingSetSize", ctypes.c_size_t),
            ("MaximumWorkingSetSize", ctypes.c_size_t),
            ("ActiveProcessLimit", ctypes.c_uint32),
            ("Affinity", ctypes.c_size_t),
            ("PriorityClass", ctypes.c_uint32),
            ("SchedulingClass", ctypes.c_uint32),
        ]

    class Extendida(ctypes.Structure):
        _fields_ = [
            ("Basica", Basica),
            ("IoInfo", ctypes.c_uint64 * 6),
            ("ProcessMemoryLimit", ctypes.c_size_t),
            ("JobMemoryLimit", ctypes.c_size_t),
            ("PeakProcessMemoryUsed", ctypes.c_size_t),
            ("PeakJobMemoryUsed", ctypes.c_size_t),
        ]

    k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    k32.QueryInformationJobObject.argtypes = [
        ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_uint32, ctypes.c_void_p
    ]  # fmt: skip
    info = Extendida()
    # 9 = JobObjectExtendedLimitInformation
    if not k32.QueryInformationJobObject(job, 9, ctypes.byref(info), ctypes.sizeof(info), None):
        raise OSError(ctypes.get_last_error(), "QueryInformationJobObject")
    return int(info.PeakJobMemoryUsed), int(info.PeakProcessMemoryUsed)


def correr(orden: list[str]) -> tuple[int, int, str]:
    """Ejecuta `orden` y devuelve (codigo de salida, pico en bytes, que es ese pico)."""
    if sys.platform == "win32":
        job = _windows_job()
        codigo = subprocess.run(orden, check=False).returncode
        suma, mayor = _windows_pico(job)
        return (
            codigo,
            suma,
            (
                f"suma de sus procesos, memoria comprometida, Windows; "
                f"el mayor proceso, {mayor / MIB:.0f} MiB"
            ),
        )
    import resource

    codigo = subprocess.run(orden, check=False).returncode
    maxrss = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    pico = maxrss if sys.platform == "darwin" else maxrss * 1024
    return codigo, pico, f"RSS maxima del mayor proceso, {sys.platform}"


def ruta_acumulador(repo: Path) -> Path | None:
    r = subprocess.run(
        ["git", "rev-parse", "--git-path", NOMBRE],
        cwd=repo,
        capture_output=True,
        encoding="utf-8",
        check=False,
    )
    return (repo / r.stdout.strip()).resolve() if r.returncode == 0 else None


def empezar(repo: Path) -> None:
    ruta = ruta_acumulador(repo)
    if ruta is not None:
        ruta.unlink(missing_ok=True)


def medir(repo: Path, paso: str, orden: list[str]) -> int:
    codigo, pico, que = correr(orden)
    ruta = ruta_acumulador(repo)
    if ruta is not None:
        with ruta.open("a", encoding="utf-8", newline="\n") as f:
            f.write(f"{paso}\t{pico}\t{que}\n")
    return codigo


def linea_de_informe(filas: list[tuple[str, int, str]]) -> str:
    if not filas:
        return "PICO DE MEMORIA de make check: sin medida (ningun paso apunto su pico)"
    paso, pico, que = max(filas, key=lambda f: f[1])
    return f"PICO DE MEMORIA de make check: {pico / MIB:.0f} MiB en `{paso}` ({que})"


def informe(repo: Path) -> str:
    ruta = ruta_acumulador(repo)
    filas: list[tuple[str, int, str]] = []
    if ruta is not None and ruta.exists():
        for linea in ruta.read_text(encoding="utf-8").splitlines():
            paso, pico, que = linea.split("\t", 2)
            filas.append((paso, int(pico), que))
        ruta.unlink()
    return linea_de_informe(filas)


def main(argv: list[str]) -> int:
    repo = Path.cwd()
    if argv[:1] == ["empezar"]:
        empezar(repo)
        return 0
    if argv[:1] == ["informe"]:
        print(informe(repo))
        return 0
    if len(argv) >= 4 and argv[0] == "medir" and argv[2] == "--":
        return medir(repo, argv[1], argv[3:])
    if len(argv) >= 3 and argv[0] == "ejecutar" and argv[1] == "--":
        codigo, pico, que = correr(argv[2:])
        print(f"PICO DE MEMORIA: {pico / MIB:.0f} MiB ({que}); codigo de salida {codigo}")
        return codigo
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
