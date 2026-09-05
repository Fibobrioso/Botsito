"""Guardias contra el historial de git (F06 evidencia, F09 feedback; seccion H del plan).

Los hooks se saltan con --no-verify; el historial no. Dos guardias:

1. Inmutabilidad por contenido: para cada fichero protegido que alguna vez se anadio bajo un
   directorio (evidencia, feedback), su blob en HEAD debe ser identico al del commit que lo anadio y
   el fichero debe seguir existiendo. Cubre ediciones y adiciones escondidas en commits de merge
   (`git log -m`), que sin `-m` no se muestran.
2. Trazabilidad: todo commit posterior a un punto dado que toque la especificacion o los casos debe
   llevar un trailer `Fuente:` con ids de evidencia, de feedback o de ADR.

Toda salida de git se decodifica como UTF-8 con `core.quotepath=false`: en Windows la consola es
cp1252 y un mensaje de commit con una mayuscula acentuada dejaba la salida en `None`, que se leia
como "sin problemas". `None` significa ahora una sola cosa: no hay git o la referencia no existe;
quien llama decide si eso es un error.
"""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

from botsito.comun import ids

DIRECTORIO_EVIDENCIA = "knowledge/evidence"
DIRECTORIO_FEEDBACK = "knowledge/feedback"
DIRECTORIO_MANIFIESTOS = "data/manifests"
DIRECTORIOS_CON_FUENTE = ("knowledge/spec/", "knowledge/cases/")
# README y todo `_*.yaml` (p. ej. `_contradicciones.yaml`, GENERADO) quedan fuera de la guardia.
EXENTOS = ("README.md",)
# Ancla de la trazabilidad: el tag es legible; el SHA sobrevive a un clon sin tags.
ANCLA_FUENTE = ("stable/F06", "b6b82f2f164c5ca48bde692467b55f1267cf992b")
_ID_FUENTE = ids.FUENTE
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
        ["git", "-c", "core.quotepath=false", *args],
        cwd=repo,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    return resultado.stdout if resultado.returncode == 0 else None


def hay_git(repo: Path) -> bool:
    """True si `repo` esta dentro de un repositorio git con al menos un commit."""
    return _git(repo, "rev-parse", "--verify", "-q", "HEAD") is not None


def historial_evaluable(repo: Path) -> str | None:
    """Motivo por el que las guardias de historial NO se pueden evaluar, o None si se puede.

    Un clon superficial no tiene el commit que anadio cada fichero (todo pareceria intacto) y un
    proyecto que no es la raiz del repositorio git recibe rutas con otro prefijo (nada pareceria
    protegido). En ambos casos la respuesta correcta es "no evaluable", no "sin violaciones".
    """
    superficial = _git(repo, "rev-parse", "--is-shallow-repository")
    if superficial is not None and superficial.strip() == "true":
        return "clon superficial: haz git fetch --unshallow"
    raiz = _git(repo, "rev-parse", "--show-toplevel")
    if raiz is not None and os.path.normcase(str(Path(raiz.strip()).resolve())) != os.path.normcase(
        str(repo.resolve())
    ):
        return f"el proyecto no es la raiz del repositorio git ({raiz.strip()})"
    return None


def ancla_desviada(repo: Path, tag: str, sha: str) -> str | None:
    """Si el tag existe y no apunta al SHA del ancla, alguien lo movio: eso es un error."""
    real = _git(repo, "rev-parse", "--verify", "-q", f"{tag}^{{commit}}")
    if real is None or real.strip() == sha:
        return None
    return f"el tag {tag} apunta a {real.strip()[:7]}, no al ancla {sha[:7]}: alguien lo movio"


def resolver(repo: Path, *candidatos: str) -> str | None:
    """Primera referencia (tag, rama o SHA) que existe en este clon."""
    for ref in candidatos:
        if _git(repo, "rev-parse", "--verify", "-q", f"{ref}^{{commit}}") is not None:
            return ref
    return None


def _blob(repo: Path, revision: str, ruta: str) -> str | None:
    salida = _git(repo, "rev-parse", "--verify", "-q", f"{revision}:{ruta}")
    return salida.strip() if salida else None


def modificaciones_en_historial(
    repo: Path, directorio: str = DIRECTORIO_EVIDENCIA
) -> list[str] | None:
    """Ficheros protegidos modificados, borrados o renombrados respecto a su primer commit.

    None si no hay git. Incluye el arbol de trabajo: una edicion sin commitear tambien cuenta.
    """
    if historial_evaluable(repo) is not None:
        return None
    historico = _git(
        repo,
        "log",
        "-m",
        "--format=",
        "--name-only",
        "--diff-filter=A",
        "--no-renames",
        "--",
        directorio,
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
            _git(repo, "log", "-m", "--format=%H", "--diff-filter=A", "--no-renames", "--", ruta)
            or ""
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
    """Ids declarados en trailers `Fuente:` (separados por comas o espacios).

    Solo cuenta el cuerpo: un asunto `Fuente: ADR-0001` no es un trailer.
    """
    ids: list[str] = []
    cuerpo = mensaje.split("\n", 1)[1] if "\n" in mensaje else ""
    for m in _TRAILER.finditer(cuerpo):
        ids.extend(x for x in re.split(r"[,\s]+", m.group(1)) if x)
    return ids


def commits_sin_fuente(
    repo: Path,
    desde: str | None,
    rutas: tuple[str, ...] = DIRECTORIOS_CON_FUENTE,
    ids_validos: set[str] | None = None,
) -> list[str] | None:
    """Commits (desde `desde`, exclusivo) que tocan `rutas` sin un trailer `Fuente:` valido.

    `ids_validos`, si se da, exige ademas que cada id exista: evidencia, feedback y ADR por igual
    (un `ADR-9999` que no existe no es una fuente). None si no hay git, `desde` no existe o el
    historial no es evaluable (clon superficial).
    """
    rango = f"{desde}..HEAD" if desde else "HEAD"
    if desde and _git(repo, "rev-parse", "--verify", "-q", f"{desde}^{{commit}}") is None:
        return None
    if historial_evaluable(repo) is not None:
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
            elif ids_validos is not None and i not in ids_validos:
                problemas.append(f"{sha[:7]}: fuente inexistente {i}")
    return problemas
