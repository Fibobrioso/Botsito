"""Ambiguedades abiertas del modelo, legibles por maquina (F10, ADR-0011).

`knowledge/spec/ambiguedades.yaml` es la fuente; la tabla de PROJECT_STATE es su reflejo (un
test lo exige). F09 valida el objetivo `ambiguedad` de un registro contra estos ids.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from botsito.comun import ids
from botsito.comun.yaml_estricto import YamlError, leer_yaml

_ES_FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}$", re.ASCII)
FICHERO_AMBIGUEDADES = "knowledge/spec/ambiguedades.yaml"
# ABIERTA es el unico estado que se SIGUE PREGUNTANDO: entra en el cuestionario de la sesion
# siguiente (`cases/cuestionario.py`) y en "corriendo con un valor en revision" de `spec status`.
# DECIDIDA nace el 2026-09-12 (ADR-0022) porque faltaba: una ambiguedad de alcance, metodo o
# herramienta la cierra el CONSULTOR, no el trader, y hasta hoy no habia forma de cerrarla -A-15,
# A-16 y A-17 llevaban decididas y abiertas desde el 2026-09-09-. Tiene que ser un ESTADO y no un
# campo junto a ABIERTA: si fuera un campo, `cuestionario.py` le volveria a preguntar al trader lo
# que el consultor ya decidio, que es justo lo que el kit existe para evitar.
ESTADOS = ("ABIERTA", "RESUELTA", "DECIDIDA")
# Que hace falta para cerrarla (2026-09-16). Una MEDICION la cierra un dato -la ficha del
# simbolo, el reloj del servidor, una comparacion de velas- y no se le pregunta al trader; una
# PREGUNTA, si. Hasta
# entonces `cuestionario.py` metia TODA abierta en la sesion siguiente, y A-16, A-27 y A-28 -que lo
# dicen en su propio texto: "MEDICION, no pregunta al trader"- le habrian llegado como preguntas.
CLASES = ("medicion", "pregunta")
CAMPOS = (
    "id",
    "titulo",
    "pregunta",
    "resuelve_en",
    "evidencia",
    "parametros",
    "contradiccion",
    "estado",
    # Obligatorios-nulables, como `contradiccion`: van en las 21 entradas, con null cuando no
    # aplica. Solo DECIDIDA los lleva con valor, y la guardia lo exige en los dos sentidos.
    "decision",
    "decidida_el",
    "bloqueante",
)
# Opcional en el esquema, como `recibido_el` en el feedback (ADR-0023): las cerradas no la
# necesitan. Obligatoria por guardia en toda ABIERTA (`abiertas_sin_clase`).
CAMPOS_OPCIONALES = ("clase",)


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
    decision: str | None
    decidida_el: str | None
    bloqueante: bool
    clase: str | None = None


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
    extra = sorted(set(bruto) - set(CAMPOS) - set(CAMPOS_OPCIONALES))
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
    decision, decidida_el = bruto["decision"], bruto["decidida_el"]
    if bruto["estado"] == "DECIDIDA":
        if not (isinstance(decision, str) and ids.es_id_de("decision", decision)):
            raise AmbiguedadError(
                f"{aid}: DECIDIDA exige `decision` con un ADR-NNNN, no {decision!r}"
            )
        if not (isinstance(decidida_el, str) and _ES_FECHA.match(decidida_el)):
            raise AmbiguedadError(
                f"{aid}: DECIDIDA exige `decidida_el` AAAA-MM-DD, no {decidida_el!r}"
            )
    elif decision is not None or decidida_el is not None:
        raise AmbiguedadError(
            f"{aid}: `decision` y `decidida_el` solo van en DECIDIDA; aqui esta {bruto['estado']}"
        )
    clase = bruto.get("clase")
    if clase is not None and clase not in CLASES:
        raise AmbiguedadError(f"{aid}: clase {clase!r} no esta en {CLASES}")
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
        str(decision) if decision is not None else None,
        str(decidida_el) if decidida_el is not None else None,
        bool(bruto["bloqueante"]),
        str(clase) if clase is not None else None,
    )


def cargar_ambiguedades(ruta: Path) -> list[Ambiguedad]:
    """Carga estricta; ids unicos y en orden numerico."""
    try:
        doc = leer_yaml(ruta)
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


def abiertas_sin_clase(ambiguedades: list[Ambiguedad]) -> list[str]:
    """Toda ABIERTA declara si es medicion o pregunta.

    Vive aparte de `validar_contra_contexto` a proposito: esa la usa tambien el kit al construir
    paquetes de repositorios de prueba, y el campo es opcional en el esquema (como `recibido_el`,
    ADR-0023). La exige `knowledge validate` sobre el fichero real, que es el que alimenta el
    cuestionario de la sesion siguiente.
    """
    return [
        f"{a.id}: esta ABIERTA y no declara `clase` (medicion | pregunta); sin ella el "
        f"cuestionario no sabe si preguntarsela al trader"
        for a in ambiguedades
        if a.estado == "ABIERTA" and a.clase is None
    ]
