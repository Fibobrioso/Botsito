"""Cuestionario de la sesion: una pregunta por origen (parametro UNKNOWN de estrategia,
ambiguedad ABIERTA, contradiccion abierta), fusionando los origenes que el mapa enlaza, cada
una con casos concretos de la evidencia (F10, ADR-0011)."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from botsito.cases.ambiguedades import Ambiguedad
from botsito.config.registro import Estado, Registro
from botsito.evidence.modelo import EvidenceItem

MAX_CASOS = 3


class CuestionarioError(ValueError):
    """No se puede generar una pregunta con lo que hay."""


@dataclass(frozen=True, slots=True)
class EntradaMapa:
    temas: tuple[str, ...]
    ambiguedad: str | None
    opciones: tuple[str, ...]


@dataclass
class Pregunta:
    id: str
    bloqueante: bool
    origenes: list[dict[str, str]]
    titulo: str
    enunciado: str
    respuesta_esperada: dict[str, Any]
    casos: list[dict[str, Any]] = field(default_factory=list)

    def como_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "bloqueante": self.bloqueante,
            "origenes": self.origenes,
            "titulo": self.titulo,
            "enunciado": self.enunciado,
            "respuesta_esperada": self.respuesta_esperada,
            "casos": self.casos,
        }


def _tema_casa(tema_item: str, tema: str) -> bool:
    return tema_item == tema or tema_item.startswith(tema + ".")


def _caso_de(
    item: EvidenceItem, fotograma: Callable[[str, int], dict[str, Any] | None]
) -> dict[str, Any]:
    foto = fotograma(item.video_id, item.t0_ms)
    return {
        "evidencia": item.id,
        "video": item.video_id,
        "t0": item.t0,
        "t1": item.t1,
        "tema": item.tema,
        "valor": item.valor,
        "cita": item.cita_literal,
        "afirmacion": item.afirmacion,
        "fotograma": foto["referencia"] if foto else None,
    }


def _elegir_items(
    items: Sequence[EvidenceItem], ids_directos: Sequence[str], temas: Sequence[str]
) -> list[EvidenceItem]:
    """Primero los ids citados (en su orden), luego por tema: con `valor` antes, y por tiempo."""
    por_id = {i.id: i for i in items}
    elegidos: list[EvidenceItem] = [por_id[i] for i in ids_directos if i in por_id]
    vistos = {i.id for i in elegidos}
    candidatos = [
        i for i in items if i.id not in vistos and any(_tema_casa(i.tema, t) for t in temas)
    ]
    candidatos.sort(key=lambda i: (i.valor is None, i.video_id, i.t0_ms, i.id))
    for c in candidatos:
        if len(elegidos) >= MAX_CASOS:
            break
        elegidos.append(c)
    return elegidos[:MAX_CASOS]


def generar(
    registro: Registro,
    ambiguedades: Sequence[Ambiguedad],
    mapa: Mapping[str, EntradaMapa],
    contradicciones: Sequence[dict[str, Any]],
    items: Sequence[EvidenceItem],
    fotograma: Callable[[str, int], dict[str, Any] | None],
) -> list[Pregunta]:
    """Preguntas en orden: bloqueantes (por numero de ambiguedad), resto de ambiguedades,
    parametros sin ambiguedad (alfabetico), contradicciones sin ambiguedad (por tema)."""
    unknown = [
        n
        for n in registro.por_categoria("estrategia")
        if registro.parametros[n].estado is Estado.UNKNOWN
    ]
    faltan_en_mapa = sorted(set(unknown) - set(mapa))
    if faltan_en_mapa:
        raise CuestionarioError(
            f"parametros UNKNOWN sin entrada en mapa_parametros: {faltan_en_mapa}"
        )
    cubiertos_param: set[str] = set()
    cubiertas_contra: set[str] = set()
    preguntas: list[Pregunta] = []

    def anadir(p: Pregunta, ids_directos: Sequence[str], temas: Sequence[str]) -> None:
        elegidos = _elegir_items(items, ids_directos, temas)
        if not elegidos:
            raise CuestionarioError(
                f"{p.titulo}: ninguna evidencia para la pregunta (origenes {p.origenes})"
            )
        p.casos = [_caso_de(i, fotograma) for i in elegidos]
        preguntas.append(p)

    abiertas = [a for a in ambiguedades if a.estado == "ABIERTA"]
    orden = sorted(abiertas, key=lambda a: (not a.bloqueante, int(a.id[2:])))
    for a in orden:
        origenes = [{"tipo": "ambiguedad", "id": a.id}]
        temas: list[str] = []
        opciones: list[str] = []
        tipos: list[str] = []
        params = [p for p in a.parametros if p in unknown]
        # tambien los parametros cuyo mapa apunta a esta ambiguedad
        params += [n for n in unknown if mapa[n].ambiguedad == a.id and n not in params]
        for n in params:
            origenes.append({"tipo": "parametro", "id": n})
            cubiertos_param.add(n)
            temas += list(mapa[n].temas)
            opciones += [o for o in mapa[n].opciones if o not in opciones]
            tipos.append(registro.parametros[n].tipo)
        if a.contradiccion:
            origenes.append({"tipo": "contradiccion", "id": a.contradiccion})
            cubiertas_contra.add(a.contradiccion)
        p = Pregunta(
            "",
            a.bloqueante,
            origenes,
            a.titulo,
            a.pregunta,
            {"parametros": params, "tipos": tipos, "opciones": opciones or None},
        )
        anadir(p, a.evidencia, temas)
    for n in unknown:
        if n in cubiertos_param:
            continue
        e = mapa[n]
        param = registro.parametros[n]
        p = Pregunta(
            "",
            False,
            [{"tipo": "parametro", "id": n}],
            n,
            f"¿{param.descripcion}? ({param.unidad})",
            {"parametros": [n], "tipos": [param.tipo], "opciones": list(e.opciones) or None},
        )
        anadir(p, [], e.temas)
        cubiertos_param.add(n)
    for c in sorted(contradicciones, key=lambda x: str(x["tema"])):
        tema = str(c["tema"])
        if tema in cubiertas_contra:
            continue
        ids_c = [str(i["id"]) for i in c["items"]]
        p = Pregunta(
            "",
            False,
            [{"tipo": "contradiccion", "id": tema}],
            f"contradiccion {tema}",
            f"¿cual de estos valores es el vigente para {tema}: "
            f"{', '.join(str(v) for v in c['valores'])}?",
            {"parametros": [], "tipos": [], "opciones": [str(v) for v in c["valores"]]},
        )
        anadir(p, ids_c, [tema])
    for k, p in enumerate(preguntas, 1):
        p.id = f"P-{k:02d}"
    return preguntas
