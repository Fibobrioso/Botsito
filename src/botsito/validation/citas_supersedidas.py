"""G1: un item de evidencia supersedido no se cita desde la spec (trabajo/guardias-citas).

La condicion, tal como la fijo el consultor el 2026-10-05 (docs/validation/GUARDIAS-CITAS.md):
«En todo fichero bajo knowledge/spec/, un id ev-* supersedido solo puede aparecer dentro del mismo
valor escalar de YAML, o de la misma linea de comentario, que nombra su sustituto. Cualquier otra
aparicion falla.» Se escanea el TEXTO entero, comentarios incluidos, sin lista de campos:
enumerar campos deja escapar el que nadie penso. Un supersedido solo se nombra para contar la
sustitucion; la spec cita el item vigente.

Niega por defecto: se vigila TODO fichero bajo `knowledge/spec/`, tambien uno nuevo, salvo los de
`EXCLUIDOS`, que estan a la vista y hoy vacios. Un fichero que no es YAML, o que no se puede leer
como YAML, no tiene valores escalares: ahi toda aparicion de un supersedido falla. `docs/spec/`
queda fuera porque es GENERADO desde aqui y `tests/contract/test_spec_docs_generados.py` exige que
lo reproduzca.

Lee el sistema de ficheros, no git: en `validation/` solo `Historial` lee git
(`tests/unit/test_historial_sin_git.py`). Solo ids: no lee ninguna cita ni ninguna transcripcion.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

import yaml

DIRECTORIO = "knowledge/spec"
# Rutas relativas a la raiz (con `/`) que G1 no mira, cada una con su motivo en un comentario.
# Vacia desde que nacio: excluir un fichero es una decision que se ve en el diff.
EXCLUIDOS: tuple[str, ...] = ()
ID_EVIDENCIA = re.compile(r"\bev-[a-z0-9]+-\d{6}-[0-9a-f]{8}\b", re.ASCII)
_EXTENSIONES_YAML = (".yaml", ".yml")


def sustitutos(items: Iterable[Any]) -> dict[str, list[str]]:
    """id supersedido -> su cadena de sustitutos, del inmediato al vigente.

    Nombrar cualquiera de la cadena cuenta como nombrar su sustituto. La cadena se corta si
    vuelve sobre si misma (los ciclos ya los niega `validar_contra_manifiesto`)."""
    siguiente = {it.supersede: it.id for it in items if getattr(it, "supersede", None)}
    cadenas: dict[str, list[str]] = {}
    for viejo in siguiente:
        cadena: list[str] = []
        actual = viejo
        while actual in siguiente and siguiente[actual] not in cadena:
            actual = siguiente[actual]
            cadena.append(actual)
        cadenas[viejo] = cadena
    return cadenas


def ficheros_vigilados(repo: Path) -> list[Path]:
    """Todo fichero bajo `knowledge/spec/`, recursivo, menos `EXCLUIDOS`."""
    raiz = repo / DIRECTORIO
    if not raiz.is_dir():
        return []
    return sorted(
        p
        for p in raiz.rglob("*")
        if p.is_file() and p.relative_to(repo).as_posix() not in EXCLUIDOS
    )


def _escalares(texto: str) -> list[tuple[int, int, str]] | None:
    """(inicio, fin, valor) de cada escalar del YAML, por posicion en el texto; None si no se
    puede leer como YAML."""
    try:
        nodos = list(yaml.compose_all(texto, Loader=yaml.SafeLoader))
    except yaml.YAMLError:
        return None
    escalares: list[tuple[int, int, str]] = []
    pendientes: list[Any] = [n for n in nodos if n is not None]
    while pendientes:
        nodo = pendientes.pop()
        if isinstance(nodo, yaml.ScalarNode):
            escalares.append((nodo.start_mark.index, nodo.end_mark.index, str(nodo.value)))
        elif isinstance(nodo, yaml.SequenceNode):
            pendientes.extend(nodo.value)
        elif isinstance(nodo, yaml.MappingNode):
            for clave, valor in nodo.value:
                pendientes.extend((clave, valor))
    return escalares


def _comentario(texto: str, pos: int, escalares: list[tuple[int, int, str]]) -> str | None:
    """El comentario de la linea de `pos` si `pos` cae en el: desde el primer `#` de la linea que
    no esta dentro de un escalar hasta el final de la linea."""
    inicio = texto.rfind("\n", 0, pos) + 1
    fin = texto.find("\n", pos)
    fin = len(texto) if fin == -1 else fin
    for i in range(inicio, pos):
        fuera_de_escalar = not any(a <= i < b for a, b, _ in escalares)
        if texto[i] == "#" and fuera_de_escalar and (i == inicio or texto[i - 1] in " \t"):
            return texto[i:fin]
    return None


def problemas_en_texto(
    ruta: str, texto: str, cadenas: Mapping[str, list[str]], es_yaml: bool
) -> list[str]:
    """Cada aparicion de un supersedido que no comparte valor escalar o linea de comentario con
    su sustituto, con fichero y linea."""
    apariciones = [m for m in ID_EVIDENCIA.finditer(texto) if m.group() in cadenas]
    if not apariciones:
        return []
    escalares = _escalares(texto) if es_yaml else None
    problemas: list[str] = []
    for m in apariciones:
        viejo, pos = m.group(), m.start()
        cadena = cadenas[viejo]
        donde: str | None = None
        for a, b, valor in escalares or []:
            if a <= pos < b:
                donde = valor
                break
        if donde is None and escalares is not None:
            donde = _comentario(texto, pos, escalares)
        if donde is not None and any(s in donde for s in cadena):
            continue
        linea = texto.count("\n", 0, pos) + 1
        sustituto = cadena[0] if cadena else "ninguno"
        vigente = f" (vigente: {cadena[-1]})" if len(cadena) > 1 else ""
        problemas.append(
            f"{ruta}:{linea}: nombra {viejo}, supersedido por {sustituto}{vigente}; un "
            f"supersedido solo aparece en el mismo valor o la misma linea de comentario que su "
            f"sustituto"
        )
    return problemas


def citas_a_supersedidos(repo: Path, items: Iterable[Any]) -> tuple[list[str], int]:
    """(problemas, ficheros mirados) de G1 sobre todo `knowledge/spec/`."""
    cadenas = sustitutos(items)
    vigilados = ficheros_vigilados(repo)
    problemas: list[str] = []
    for p in vigilados:
        texto = p.read_text(encoding="utf-8", errors="replace")
        problemas += problemas_en_texto(
            p.relative_to(repo).as_posix(), texto, cadenas, p.suffix in _EXTENSIONES_YAML
        )
    return problemas, len(vigilados)
