"""Guardias contra el historial de git (F06 evidencia, F09 feedback; seccion H del plan).

Los hooks se saltan con --no-verify; el historial no. Dos guardias:

1. Inmutabilidad por contenido: para cada fichero protegido que alguna vez se anadio bajo un
   directorio (evidencia, feedback), su blob en HEAD debe ser identico al del commit que lo anadio y
   el fichero debe seguir existiendo. Cubre ediciones escondidas en commits de merge, que
   `git log --name-status` no muestra.
2. Trazabilidad: todo commit posterior a un punto dado que toque la especificacion o los casos debe
   llevar un trailer `Fuente:` con ids de evidencia, de feedback o de ADR.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from botsito.evidence.modelo import FICHERO_CONTRADICCIONES

DIRECTORIO_EVIDENCIA = "knowledge/evidence"
DIRECTORIO_FEEDBACK = "knowledge/feedback"
DIRECTORIOS_CON_FUENTE = ("knowledge/spec/", "knowledge/cases/")
EXENTOS = (FICHERO_CONTRADICCIONES, "README.md")
_ID_FUENTE = re.compile(r"^(ev-[a-z0-9]+-\d{6}-[0-9a-f]{8}|fb-[0-9a-z-]+-[0-9a-f]{8}|ADR-\d{4})$")
_TRAILER = re.compile(r"^Fuente:\s*(.+?)\s*$", re.M)


def _es_protegido(ruta: str, directorio: str) -> bool:
    return (
        ruta.startswith(directorio + "/")
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


def modificaciones_en_historial(
    repo: Path, directorio: str = DIRECTORIO_EVIDENCIA
) -> list[str] | None:
    """Ficheros protegidos modificados, borrados o renombrados respecto a su primer commit.

    None si no hay git. Incluye el arbol de trabajo: una edicion sin commitear tambien cuenta.
    """
    historico = _git(
        repo, "log", "--format=", "--name-only", "--diff-filter=A", "--no-renames", "--", directorio
    )
    if historico is None:
        return None
    rastreados_txt = _git(repo, "ls-files", "--", directorio) or ""
    rastreados = {linea.strip() for linea in rastreados_txt.splitlines() if linea.strip()}
    anadidos = sorted(
        {r.strip() for r in historico.splitlines() if _es_protegido(r.strip(), directorio)}
    )
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
        if (repo / ruta).exists():
            actual = _git(repo, "hash-object", "--", ruta)
            if actual and blob_origen and actual.strip() != blob_origen:
                violaciones.append(f"modificado en el arbol de trabajo: {ruta}")
    return violaciones


def modificaciones_preparadas(
    repo: Path, directorio: str = DIRECTORIO_EVIDENCIA
) -> list[str] | None:
    """Cambios en el indice que tocan ficheros protegidos (para el hook pre-commit)."""
    salida = _git(repo, "diff", "--cached", "--name-status", "--", directorio)
    if salida is None:
        return None
    out: list[str] = []
    for linea in salida.splitlines():
        partes = linea.split("\t")
        if len(partes) < 2:
            continue
        estado, rutas = partes[0], partes[1:]
        if estado[0] in ("M", "D", "R", "C", "T") and any(
            _es_protegido(r, directorio) for r in rutas
        ):
            out.append(f"indice: {estado} {' -> '.join(rutas)}")
    return out


def fuentes_de_mensaje(mensaje: str) -> list[str]:
    """Ids declarados en trailers `Fuente:` (separados por comas o espacios)."""
    ids: list[str] = []
    for m in _TRAILER.finditer(mensaje):
        ids.extend(x for x in re.split(r"[,\s]+", m.group(1)) if x)
    return ids


def commits_sin_fuente(
    repo: Path,
    desde: str | None,
    rutas: tuple[str, ...] = DIRECTORIOS_CON_FUENTE,
    ids_validos: set[str] | None = None,
) -> list[str] | None:
    """Commits (desde `desde`, exclusivo) que tocan `rutas` sin un trailer `Fuente:` valido.

    `ids_validos`, si se da, exige ademas que cada id exista (los ADR se comprueban por formato).
    None si no hay git o `desde` no existe.
    """
    rango = f"{desde}..HEAD" if desde else "HEAD"
    if desde and _git(repo, "rev-parse", "--verify", "-q", desde) is None:
        return None
    salida = _git(repo, "log", "--format=%H%x1f%B%x1e", rango, "--", *rutas)
    if salida is None:
        return None
    problemas: list[str] = []
    for bloque in salida.split("\x1e"):
        if "\x1f" not in bloque:
            continue
        sha, mensaje = bloque.split("\x1f", 1)
        sha = sha.strip()
        if not sha:
            continue
        ids = fuentes_de_mensaje(mensaje)
        if not ids:
            problemas.append(f"{sha[:7]}: toca spec/cases sin trailer 'Fuente:'")
            continue
        for i in ids:
            if not _ID_FUENTE.match(i):
                problemas.append(f"{sha[:7]}: fuente con formato invalido {i!r}")
            elif ids_validos is not None and not i.startswith("ADR-") and i not in ids_validos:
                problemas.append(f"{sha[:7]}: fuente inexistente {i}")
    return problemas
