"""Ambiguedades abiertas del modelo, legibles por maquina (F10, ADR-0011).

`knowledge/spec/ambiguedades.yaml` es la fuente; la tabla de PROJECT_STATE es su reflejo (un
test lo exige). F09 valida el objetivo `ambiguedad` de un registro contra estos ids.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from botsito.comun import ids
from botsito.comun.yaml_estricto import YamlError, cargar_yaml

FICHERO_AMBIGUEDADES = "knowledge/spec/ambiguedades.yaml"
ESTADOS = ("ABIERTA", "RESUELTA")
CAMPOS = (
    "id",
    "titulo",
    "pregunta",
    "resuelve_en",
    "evidencia",
    "parametros",
    "contradiccion",
    "estado",
    "bloqueante",
)


class AmbiguedadError(ValueError):
    """El fichero de ambiguedades no cumple su esquema."""


@dataclass(frozen=True, slots=True)
class Ambiguedad:
    id: str
    titulo: str
    pregunta: str
    resuelve_en: tuple[str, ...]
    evidencia: tuple[str, ...]
    parametros: tuple[str, ...]
    contradiccion: str | None
    estado: str
    bloqueante: bool


def _lista_de_textos(bruto: object, campo: str, aid: str) -> tuple[str, ...]:
    if not isinstance(bruto, list) or not all(isinstance(x, str) and x.strip() for x in bruto):
        raise AmbiguedadError(f"{aid}: {campo} debe ser una lista de textos")
    return tuple(bruto)


def _ambiguedad(bruto: object) -> Ambiguedad:
    if not isinstance(bruto, dict):
        raise AmbiguedadError("cada ambiguedad es un mapa")
    aid = str(bruto.get("id"))
    if not ids.es_id_de("ambiguedad", aid):
        raise AmbiguedadError(f"id invalido {aid!r} (formato A-N)")
    faltan = [c for c in CAMPOS if c not in bruto]
    extra = sorted(set(bruto) - set(CAMPOS))
    if faltan or extra:
        raise AmbiguedadError(f"{aid}: faltan {faltan}, sobran {extra}")
    for c in ("titulo", "pregunta"):
        if not isinstance(bruto[c], str) or not bruto[c].strip():
            raise AmbiguedadError(f"{aid}: {c} vacio")
    if bruto["estado"] not in ESTADOS:
        raise AmbiguedadError(f"{aid}: estado {bruto['estado']!r} no esta en {ESTADOS}")
    if not isinstance(bruto["bloqueante"], bool):
        raise AmbiguedadError(f"{aid}: bloqueante debe ser true/false")
    contradiccion = bruto["contradiccion"]
    if contradiccion is not None and (not isinstance(contradiccion, str) or not contradiccion):
        raise AmbiguedadError(f"{aid}: contradiccion debe ser un tema o null")
    evidencia = _lista_de_textos(bruto["evidencia"], "evidencia", aid)
    if not evidencia:
        raise AmbiguedadError(f"{aid}: una ambiguedad cita al menos un item de evidencia")
    for e in evidencia:
        if not ids.es_id_de("evidence", e):
            raise AmbiguedadError(f"{aid}: {e!r} no es un id de evidencia")
    return Ambiguedad(
        aid,
        str(bruto["titulo"]).strip(),
        " ".join(str(bruto["pregunta"]).split()),
        _lista_de_textos(bruto["resuelve_en"], "resuelve_en", aid),
        evidencia,
        _lista_de_textos(bruto["parametros"], "parametros", aid),
        contradiccion,
        str(bruto["estado"]),
        bool(bruto["bloqueante"]),
    )


def cargar_ambiguedades(ruta: Path) -> list[Ambiguedad]:
    """Carga estricta; ids unicos y en orden numerico."""
    try:
        doc = cargar_yaml(ruta.read_text(encoding="utf-8"))
    except (OSError, YamlError) as exc:
        raise AmbiguedadError(f"{ruta.name}: {exc}") from exc
    if not isinstance(doc, dict) or set(doc) != {"ambiguedades"}:
        raise AmbiguedadError(f"{ruta.name}: solo se admite la clave 'ambiguedades'")
    if not isinstance(doc["ambiguedades"], list):
        raise AmbiguedadError(f"{ruta.name}: 'ambiguedades' debe ser una lista")
    salida = [_ambiguedad(b) for b in doc["ambiguedades"]]
    vistos: set[str] = set()
    for a in salida:
        if a.id in vistos:
            raise AmbiguedadError(f"{ruta.name}: id repetido {a.id}")
        vistos.add(a.id)
    numeros = [int(a.id[2:]) for a in salida]
    if numeros != sorted(numeros):
        raise AmbiguedadError(f"{ruta.name}: las ambiguedades van en orden numerico")
    return salida


def validar_contra_contexto(
    ambiguedades: list[Ambiguedad],
    ids_evidencia: set[str],
    nombres_parametros: set[str],
    temas_contradiccion: set[str],
) -> list[str]:
    """Cada evidencia citada existe, cada parametro esta en el registro y cada contradiccion
    citada esta abierta (o la ambiguedad esta RESUELTA)."""
    problemas: list[str] = []
    for a in ambiguedades:
        for e in a.evidencia:
            if e not in ids_evidencia:
                problemas.append(f"{a.id}: evidencia {e} no existe")
        for p in a.parametros:
            if p not in nombres_parametros:
                problemas.append(f"{a.id}: parametro {p} no esta en el registro")
        if a.contradiccion and a.estado == "ABIERTA" and a.contradiccion not in temas_contradiccion:
            problemas.append(f"{a.id}: no hay contradiccion abierta sobre {a.contradiccion}")
    return problemas


def como_dict(a: Ambiguedad) -> dict[str, Any]:
    return {
        "id": a.id,
        "titulo": a.titulo,
        "pregunta": a.pregunta,
        "resuelve_en": list(a.resuelve_en),
        "evidencia": list(a.evidencia),
        "parametros": list(a.parametros),
        "contradiccion": a.contradiccion,
        "estado": a.estado,
        "bloqueante": a.bloqueante,
    }
