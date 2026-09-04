"""Inmutabilidad de la evidencia contra el historial de git (F06, seccion H del plan).

Los hooks se saltan con --no-verify; el historial no. Un fichero de evidencia (salvo el generado
`_contradicciones.yaml` y los README) solo puede aparecer en el historial como anadido. Cualquier
commit que lo modifique, renombre o borre es una violacion, este donde este en la historia.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from botsito.evidence.modelo import FICHERO_CONTRADICCIONES

DIRECTORIO = "knowledge/evidence"
EXENTOS = (FICHERO_CONTRADICCIONES, "README.md")


def _es_protegido(ruta: str) -> bool:
    return (
        ruta.startswith(DIRECTORIO + "/")
        and ruta.endswith(".yaml")
        and Path(ruta).name not in EXENTOS
        and not Path(ruta).name.startswith("_")
    )


def _violaciones(salida: str, origen: str) -> list[str]:
    out: list[str] = []
    for linea in salida.splitlines():
        partes = linea.split("\t")
        if len(partes) < 2:
            continue
        estado, rutas = partes[0], partes[1:]
        if estado[0] in ("M", "D", "R", "C", "T") and any(_es_protegido(r) for r in rutas):
            out.append(f"{origen}: {estado} {' -> '.join(rutas)}")
    return out


def modificaciones_en_historial(repo: Path) -> list[str] | None:
    """Ficheros de evidencia modificados, borrados o renombrados en algun commit.

    None si no hay git.
    """
    resultado = subprocess.run(
        ["git", "log", "--format=@%h", "--name-status", "--", DIRECTORIO],
        cwd=repo,
        capture_output=True,
        text=True,
        check=False,
    )
    if resultado.returncode != 0:
        return None
    violaciones: list[str] = []
    commit = "?"
    bloque: list[str] = []
    for linea in resultado.stdout.splitlines() + ["@fin"]:
        if linea.startswith("@"):
            violaciones.extend(_violaciones("\n".join(bloque), commit))
            commit, bloque = linea[1:], []
        elif linea.strip():
            bloque.append(linea)
    return violaciones


def modificaciones_preparadas(repo: Path) -> list[str] | None:
    """Lo mismo sobre el indice (para el hook pre-commit)."""
    resultado = subprocess.run(
        ["git", "diff", "--cached", "--name-status", "--", DIRECTORIO],
        cwd=repo,
        capture_output=True,
        text=True,
        check=False,
    )
    if resultado.returncode != 0:
        return None
    return _violaciones(resultado.stdout, "indice")
