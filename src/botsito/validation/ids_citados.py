"""La guardia de ids citados en los DOCUMENTOS (2026-09-22, rama `trabajo/guardia-ids-docs`).

La que comprueba que un id citado existe corria solo sobre `knowledge/**` (`cases/ambiguedades.py`,
`cases/paquete.py`); nada miraba `docs/**`, `CLAUDE.md` ni `PROJECT_STATE.md`, y un id inventado
en un documento no lo paraba nadie. Medido ese dia: 13 citas de 4 ids que no existen, ninguna una
fabricacion, pero por suerte y no por diseno. Es el patron 5 -lo escrito y lo que existe se
separan y nada los compara-.

**UNA SOLA DEFINICION DE CADA COSA.** Que es un id: `comun.ids.FUENTE`, la gramatica del trailer
`Fuente:`, aplicada con `fullmatch` a cada tramo `[A-Za-z0-9-]` del texto (el tramo solo trocea,
no decide). Que ids existen: el conjunto que recibe esta funcion, que es el MISMO con el que
`knowledge validate` valida los trailers (`ids_de_fuente`).

**LA EXCEPCION NOMBRA LA CONDICION Y VIVE EN EL DOCUMENTO** (patron 3: no una lista de ids
exentos en el codigo). Un documento puede citar a proposito un id que no existe -el ejemplo de un
ADR inventado, la salida de una copia desechable- si lo DECLARA en un bloque con nombre fijo, que se
ve al renderizar:

    ```ids-inexistentes
    ev-v4-003710-f32c06e4 — el motivo, obligatorio
    ```

(puede ir dentro de un recuadro `>`). Cuatro reglas: la declaracion exime ese id SOLO en ese
documento; si el id declarado EXISTE, falla (declaracion obsoleta); si el id no aparece citado
FUERA del bloque, falla (declaracion muerta: la mencion dentro del propio bloque no cuenta, o la
regla no podria fallar nunca); y sin motivo, falla. Un documento tiene como mucho un bloque.
"""

from __future__ import annotations

import re
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

from botsito.comun import ids

BLOQUE = "ids-inexistentes"
DOCUMENTOS_RAIZ = ("CLAUDE.md", "PROJECT_STATE.md")
DIRECTORIO_DOCS = "docs"
_TRAMO = re.compile(r"[A-Za-z0-9-]+")
_CITA = re.compile(r"^\s*(?:>\s*)*")
_APERTURA = re.compile(r"^\s*(?:>\s*)*```" + re.escape(BLOQUE) + r"\s*$")
_CIERRE = re.compile(r"^\s*(?:>\s*)*```\s*$")
_SEPARADOR = " — "


@dataclass(frozen=True)
class _Declaracion:
    id: str
    linea: int
    motivo: str


def documentos(repo: Path) -> list[Path]:
    """`docs/**` (todo fichero de texto) mas `CLAUDE.md` y `PROJECT_STATE.md`."""
    salida = [repo / r for r in DOCUMENTOS_RAIZ if (repo / r).is_file()]
    base = repo / DIRECTORIO_DOCS
    if base.is_dir():
        salida += sorted(p for p in base.rglob("*") if p.is_file())
    return salida


def _ids_de(linea: str) -> Iterator[str]:
    for m in _TRAMO.finditer(linea):
        if ids.FUENTE.fullmatch(m.group(0)):
            yield m.group(0)


def _leer(rel: str, lineas: list[str]) -> tuple[list[_Declaracion], set[int], list[str]]:
    """Declaraciones, lineas del bloque (que no cuentan como cita) y problemas de forma."""
    decl: list[_Declaracion] = []
    del_bloque: set[int] = set()
    problemas: list[str] = []
    bloques = 0
    dentro = False
    for n, linea in enumerate(lineas, start=1):
        if not dentro and _APERTURA.match(linea):
            dentro = True
            bloques += 1
            del_bloque.add(n)
            if bloques == 2:
                problemas.append(f"{rel}:{n}: segundo bloque {BLOQUE} (uno por documento)")
            continue
        if dentro:
            del_bloque.add(n)
            if _CIERRE.match(linea):
                dentro = False
                continue
            cuerpo = _CITA.sub("", linea, count=1).strip()
            if not cuerpo:
                continue
            # El id es el primer token; el resto tiene que ser `— motivo`, con texto.
            id_, _, resto = cuerpo.partition(" ")
            motivo = resto.strip().removeprefix(_SEPARADOR.strip())
            if not ids.FUENTE.fullmatch(id_):
                problemas.append(f"{rel}:{n}: linea de {BLOQUE} sin un id al principio")
            elif not resto.strip().startswith(_SEPARADOR.strip()) or not motivo.strip():
                problemas.append(f"{rel}:{n}: {id_} declarado sin motivo (`id — motivo`)")
            else:
                decl.append(_Declaracion(id_, n, motivo.strip()))
    if dentro:
        problemas.append(f"{rel}: bloque {BLOQUE} sin cerrar")
    return decl, del_bloque, problemas


def problemas_de_ids_citados(repo: Path, existentes: set[str]) -> list[str]:
    """Cada id citado en los documentos existe, o esta declarado en su documento con motivo.

    El error de una cita nombra el fichero, la linea y el id, y nada mas.
    """
    problemas: list[str] = []
    for ruta in documentos(repo):
        try:
            lineas = ruta.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue  # binarios: no citan
        rel = ruta.relative_to(repo).as_posix()
        declaraciones, del_bloque, forma = _leer(rel, lineas)
        problemas += forma
        declarados = {d.id for d in declaraciones}
        citados: set[str] = set()
        for n, linea in enumerate(lineas, start=1):
            if n in del_bloque:
                continue
            for id_ in _ids_de(linea):
                citados.add(id_)
                if id_ not in existentes and id_ not in declarados:
                    problemas.append(f"{rel}:{n}: {id_}")
        for d in declaraciones:
            if d.id in existentes:
                problemas.append(f"{rel}:{d.linea}: {d.id} declarado inexistente y SI existe")
            elif d.id not in citados:
                problemas.append(f"{rel}:{d.linea}: {d.id} declarado y no citado en el documento")
    return problemas
