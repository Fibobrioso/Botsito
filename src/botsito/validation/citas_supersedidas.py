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

`EXCEPCIONES` son PARES (ambiguedad, id supersedido), cada uno con su motivo, no ficheros ni
campos: la aparicion pasa solo si esta en un valor del objeto cuyo `id` es esa ambiguedad. Una
excepcion que ya no se usa es un FALLO, para que no quede viva sin uso (respuesta del consultor del
2026-10-06 a la parada de A-11). Hoy no hay ninguna (`trabajo/respaldo-a11`, 2026-10-07).

Lee el sistema de ficheros, no git: en `validation/` solo `Historial` lee git
(`tests/unit/test_historial_sin_git.py`). Solo ids: no lee ninguna cita ni ninguna transcripcion.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class Excepcion:
    ambiguedad: str
    id: str
    motivo: str


DIRECTORIO = "knowledge/spec"
# Rutas relativas a la raiz (con `/`) que G1 no mira, cada una con su motivo en un comentario.
# Vacia desde que nacio: excluir un fichero es una decision que se ve en el diff.
EXCLUIDOS: tuple[str, ...] = ()
# Vacia desde el 2026-10-07 (trabajo/respaldo-a11, respuesta del consultor a la fase 0, D-c): A-11
# dejo de citar ev-v4-001207-0c4ffd4b, la unica excepcion que hubo. El mecanismo se conserva, como
# EXCLUIDOS: anadir un par vuelve a ser una decision que se ve en el diff, y un test exige que este
# vacia (tests/unit/test_citas_supersedidas.py).
EXCEPCIONES: tuple[Excepcion, ...] = ()
ID_EVIDENCIA = re.compile(r"\bev-[a-z0-9]+-\d{6}-[0-9a-f]{8}\b", re.ASCII)
_EXTENSIONES_YAML = (".yaml", ".yml")


@dataclass(frozen=True)
class _Escalar:
    inicio: int
    fin: int
    valor: str
    dueno: str | None  # el `id` del objeto mas cercano que lo contiene, si lo tiene


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


def _id_del_objeto(nodo: yaml.MappingNode) -> str | None:
    for clave, valor in nodo.value:
        if isinstance(clave, yaml.ScalarNode) and clave.value == "id":
            return str(valor.value) if isinstance(valor, yaml.ScalarNode) else None
    return None


def _escalares(texto: str) -> list[_Escalar] | None:
    """Cada escalar del YAML con su posicion en el texto y el `id` del objeto que lo contiene;
    None si no se puede leer como YAML."""
    try:
        nodos = list(yaml.compose_all(texto, Loader=yaml.SafeLoader))
    except yaml.YAMLError:
        return None
    escalares: list[_Escalar] = []
    pendientes: list[tuple[Any, str | None]] = [(n, None) for n in nodos if n is not None]
    while pendientes:
        nodo, dueno = pendientes.pop()
        if isinstance(nodo, yaml.ScalarNode):
            escalares.append(
                _Escalar(nodo.start_mark.index, nodo.end_mark.index, str(nodo.value), dueno)
            )
        elif isinstance(nodo, yaml.SequenceNode):
            pendientes.extend((hijo, dueno) for hijo in nodo.value)
        elif isinstance(nodo, yaml.MappingNode):
            propio = _id_del_objeto(nodo) or dueno
            for clave, valor in nodo.value:
                pendientes.extend(((clave, propio), (valor, propio)))
    return escalares


def _comentario(texto: str, pos: int, escalares: list[_Escalar]) -> str | None:
    """El comentario de la linea de `pos` si `pos` cae en el: desde el primer `#` de la linea que
    no esta dentro de un escalar hasta el final de la linea."""
    inicio = texto.rfind("\n", 0, pos) + 1
    fin = texto.find("\n", pos)
    fin = len(texto) if fin == -1 else fin
    for i in range(inicio, pos):
        fuera_de_escalar = not any(e.inicio <= i < e.fin for e in escalares)
        if texto[i] == "#" and fuera_de_escalar and (i == inicio or texto[i - 1] in " \t"):
            return texto[i:fin]
    return None


def problemas_en_texto(
    ruta: str,
    texto: str,
    cadenas: Mapping[str, list[str]],
    es_yaml: bool,
    excepciones: Iterable[Excepcion] = (),
    usadas: set[Excepcion] | None = None,
) -> list[str]:
    """Cada aparicion de un supersedido que no comparte valor escalar o linea de comentario con
    su sustituto, con fichero y linea. Las que cubre una excepcion pasan y se anotan en `usadas`."""
    apariciones = [m for m in ID_EVIDENCIA.finditer(texto) if m.group() in cadenas]
    if not apariciones:
        return []
    por_par = {(e.ambiguedad, e.id): e for e in excepciones}
    escalares = _escalares(texto) if es_yaml else None
    problemas: list[str] = []
    for m in apariciones:
        viejo, pos = m.group(), m.start()
        cadena = cadenas[viejo]
        escalar = next((e for e in escalares or [] if e.inicio <= pos < e.fin), None)
        if escalar is not None:
            donde: str | None = escalar.valor
            excepcion = por_par.get((escalar.dueno or "", viejo))
            if excepcion is not None:
                if usadas is not None:
                    usadas.add(excepcion)
                continue
        else:
            donde = _comentario(texto, pos, escalares) if escalares is not None else None
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


def citas_a_supersedidos(
    repo: Path, items: Iterable[Any], excepciones: Iterable[Excepcion] = EXCEPCIONES
) -> tuple[list[str], int]:
    """(problemas, ficheros mirados) de G1 sobre todo `knowledge/spec/`. Una excepcion que no
    cubre ninguna aparicion es un problema: ya no hace falta y se quita."""
    excepciones = tuple(excepciones)
    cadenas = sustitutos(items)
    vigilados = ficheros_vigilados(repo)
    usadas: set[Excepcion] = set()
    problemas: list[str] = []
    for p in vigilados:
        texto = p.read_text(encoding="utf-8", errors="replace")
        problemas += problemas_en_texto(
            p.relative_to(repo).as_posix(),
            texto,
            cadenas,
            p.suffix in _EXTENSIONES_YAML,
            excepciones,
            usadas,
        )
    # Sin uso solo puede quedar la de un id que en este repo SI esta supersedido: en un
    # `knowledge/` sin ese item (los minimos de los tests de la CLI) no hay nada que exceptuar.
    problemas += [
        f"excepcion de G1 sin uso: {e.ambiguedad} ya no cita {e.id}; se quita de EXCEPCIONES "
        f"(src/botsito/validation/citas_supersedidas.py)"
        for e in excepciones
        if e not in usadas and e.id in cadenas
    ]
    return problemas, len(vigilados)
