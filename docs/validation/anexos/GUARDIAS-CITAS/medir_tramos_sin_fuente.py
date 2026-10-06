"""Fase 0 de trabajo/guardias-citas, punto c): commits que tocan tramos_no_citables.yaml.

Solo metadatos de git (sha, fecha, asunto y los ids del trailer `Fuente:`); no lee el contenido
del fichero. Por cada commit dice si lleva trailer y cual, con la misma lectura del trailer que
`commits_sin_fuente` (`fuentes_de_mensaje`: solo el cuerpo cuenta). Se miran dos listados: el
de `git log` (lo que vigilaria una guardia como la de spec/cases) y el de `git log -m
--full-history` (que tambien saca los merges que lo traen).

Uso: uv run python docs/validation/anexos/GUARDIAS-CITAS/medir_tramos_sin_fuente.py [<repo>]
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from botsito.comun.historial import fuentes_de_mensaje

RUTA = "knowledge/corpus/tramos_no_citables.yaml"


def _log(repo: Path, *extra: str) -> list[tuple[str, str, str, str]]:
    salida = subprocess.run(
        ["git", "-c", "core.quotepath=false", "log", *extra,
         "--format=%H%x1f%ad%x1f%P%x1f%B%x1e", "--date=format:%Y-%m-%d %H:%M", "--", RUTA],
        cwd=repo, capture_output=True, encoding="utf-8", errors="replace", check=True,
    ).stdout
    filas = []
    for bloque in salida.split("\x1e"):
        if "\x1f" not in bloque:
            continue
        sha, fecha, padres, mensaje = bloque.strip("\n").split("\x1f", 3)
        filas.append((sha.strip(), fecha, padres, mensaje))
    return filas


def main(repo: Path) -> int:
    for titulo, extra in (("git log", ()), ("git log -m --full-history", ("-m", "--full-history"))):
        filas = _log(repo, *extra)
        vistos: set[str] = set()
        sin = 0
        print(f"== {titulo} -- {RUTA}")
        for sha, fecha, padres, mensaje in filas:
            if sha in vistos:
                continue
            vistos.add(sha)
            fuentes = fuentes_de_mensaje(mensaje)
            merge = " (merge)" if len(padres.split()) > 1 else ""
            asunto = mensaje.split("\n", 1)[0][:90]
            marca = ", ".join(fuentes) if fuentes else "SIN Fuente:"
            sin += 0 if fuentes else 1
            print(f"  {sha[:7]} {fecha}{merge} | {marca} | {asunto}")
        print(f"  commits: {len(vistos)}; sin Fuente: {sin}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()))
