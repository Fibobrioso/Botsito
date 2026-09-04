"""Inmutabilidad de la evidencia contra el historial de git (F06, seccion H del plan).

Los hooks se saltan con --no-verify; el historial no. La comprobacion es por contenido, no por
diffs: para cada fichero de evidencia que alguna vez se anadio, su blob actual en HEAD debe ser
identico al blob del commit que lo anadio, y el fichero debe seguir existiendo. Asi se detecta
tambien una edicion escondida en un commit de merge, que `git log --name-status` no muestra.
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


def _git(repo: Path, *args: str) -> str | None:
    resultado = subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, text=True, check=False
    )
    return resultado.stdout if resultado.returncode == 0 else None


def _blob(repo: Path, revision: str, ruta: str) -> str | None:
    salida = _git(repo, "rev-parse", "--verify", "-q", f"{revision}:{ruta}")
    return salida.strip() if salida else None


def modificaciones_en_historial(repo: Path) -> list[str] | None:
    """Ficheros de evidencia modificados, borrados o renombrados respecto a su primer commit.

    None si no hay git. Cubre ediciones dentro de commits de merge y renombrados (el nombre viejo
    figura como borrado). Incluye el arbol de trabajo: una edicion sin commitear tambien cuenta.
    """
    historico = _git(
        repo, "log", "--format=", "--name-only", "--diff-filter=A", "--no-renames", "--", DIRECTORIO
    )
    if historico is None:
        return None
    rastreados_txt = _git(repo, "ls-files", "--", DIRECTORIO) or ""
    rastreados = {linea.strip() for linea in rastreados_txt.splitlines() if linea.strip()}
    anadidos = sorted({r.strip() for r in historico.splitlines() if _es_protegido(r.strip())})
    violaciones: list[str] = []
    for ruta in anadidos:
        if ruta not in rastreados:
            violaciones.append(f"borrado o renombrado: {ruta}")
            continue
        primero = (
            _git(repo, "log", "--format=%H", "--diff-filter=A", "--no-renames", "--", ruta) or ""
        )
        commits = primero.split()
        if not commits:
            continue
        origen = commits[-1]  # el mas antiguo
        blob_origen = _blob(repo, origen, ruta)
        blob_head = _blob(repo, "HEAD", ruta)
        if blob_origen and blob_head and blob_origen != blob_head:
            violaciones.append(f"modificado desde {origen[:7]}: {ruta}")
            continue
        fichero = repo / ruta
        if fichero.exists():
            actual = _git(repo, "hash-object", "--", ruta)
            if actual and blob_origen and actual.strip() != blob_origen:
                violaciones.append(f"modificado en el arbol de trabajo: {ruta}")
    return violaciones


def modificaciones_preparadas(repo: Path) -> list[str] | None:
    """Cambios en el indice que tocan evidencia protegida (para el hook pre-commit)."""
    salida = _git(repo, "diff", "--cached", "--name-status", "--", DIRECTORIO)
    if salida is None:
        return None
    out: list[str] = []
    for linea in salida.splitlines():
        partes = linea.split("\t")
        if len(partes) < 2:
            continue
        estado, rutas = partes[0], partes[1:]
        if estado[0] in ("M", "D", "R", "C", "T") and any(_es_protegido(r) for r in rutas):
            out.append(f"indice: {estado} {' -> '.join(rutas)}")
    return out
