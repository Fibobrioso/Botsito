"""Parte en ficheros el volcado de los escenarios SINTETICOS de `trabajo/cuenta-por-mes`: la salida
estandar de `pytest -s tests/unit/test_cuenta_por_mes.py::test_el_volcado_de_los_escenarios`
corrido en un clon de `main` (8aeed0b) con el modulo de escenarios y el test de la rama copiados
dentro. Cada salida va entre `<<<VOLCADO ruta>>>` y `<<<FIN>>>`
(`tests/unit/escenarios_cuenta_por_mes.py`, `volcado`). No importa nada del repositorio: solo lee
el volcado y escribe en la carpeta de salida, las dos por argumento (CLAUDE.md, «Ensayos
aislados»). Los fines de linea CRLF de la salida estandar de Windows vuelven a LF.

Uso: `uv run python partir_volcado.py <volcado> <carpeta de salida>`."""

from __future__ import annotations

import sys
from pathlib import Path

INICIO = "<<<VOLCADO "
FIN = "<<<FIN>>>"


def partir(texto: str) -> dict[str, str]:
    salidas: dict[str, str] = {}
    actual: str | None = None
    lineas: list[str] = []
    for linea in texto.replace("\r\n", "\n").split("\n"):
        if actual is None:
            if linea.startswith(INICIO) and linea.endswith(">>>"):
                actual, lineas = linea[len(INICIO) : -3], []
        elif linea == FIN:
            salidas[actual] = "".join(x + "\n" for x in lineas)
            actual = None
        else:
            lineas.append(linea)
    if actual is not None:
        raise SystemExit(f"volcado cortado: {actual} sin {FIN}")
    return salidas


if __name__ == "__main__":
    volcado, salida = Path(sys.argv[1]), Path(sys.argv[2])
    for ruta, contenido in sorted(partir(volcado.read_text(encoding="utf-8")).items()):
        destino = salida / ruta
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_bytes(contenido.encode("utf-8"))
        print(f"{ruta}: {len(contenido.encode('utf-8'))} bytes")
