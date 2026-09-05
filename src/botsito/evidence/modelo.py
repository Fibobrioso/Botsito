"""EvidenceItem (F06): la unidad minima de conocimiento extraido del corpus.

Un item es una cita verificable (video, t0, t1, fotogramas) con la cita literal, una afirmacion
normalizada que no anade nada que la cita no diga, un tema, un valor opcional, y quien lo extrajo
y quien lo reviso. Es INMUTABLE: su id incluye un hash del contenido, el nombre del fichero es el
id, y el historial de git se vigila (`historial.py`). Una correccion es un item nuevo que
`supersede` al anterior.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml

from botsito.comun import ids
from botsito.comun.documentos import (
    activos,
    cargar_directorio,
    ciclos_de_supersede,
    hash_corto,
    normalizar_texto,
    vacio,
)
from botsito.comun.yaml_estricto import YamlError, cargar_yaml

__all__ = ["activos", "ciclos_de_supersede"]

TIPOS = ("RULE_STATEMENT", "PARAMETER", "EXAMPLE_TRADE", "NO_TRADE", "MANAGEMENT", "UNKNOWN")
MODALIDADES = ("audio", "pantalla", "ambas")
CONFIANZAS = ("alta", "media", "baja")
EXTRACTORES = ("humano", "llm")
PROVENANCES = ("botsito", "bot-v2")
FICHERO_CONTRADICCIONES = "_contradicciones.yaml"
TOLERANCIA_DURACION_S = 1  # redondeo de ffprobe; no es un valor de negocio
import re  # noqa: E402  # tiempos e ids de video: patrones locales de este modelo

_ID = ids.EVIDENCIA
_VIDEO_ID = re.compile(r"^[a-z0-9]+$", re.ASCII)
CAMPOS_TEXTO = (
    "video_id",
    "t0",
    "t1",
    "cita_literal",
    "afirmacion",
    "tema",
    "revisado_por",
    "valor",
    "supersede",
    "notas",
)
_TIEMPO = re.compile(r"^(\d+):(\d{2}):(\d{2})(?:\.(\d+))?$", re.ASCII)
_TEMA = ids.TEMA
CAMPOS_OBLIGATORIOS = (
    "video_id",
    "t0",
    "t1",
    "modalidad",
    "tipo",
    "cita_literal",
    "afirmacion",
    "tema",
    "confianza",
    "extractor",
    "revisado_por",
    "provenance",
)
CAMPOS_OPCIONALES = ("fotogramas", "valor", "supersede", "notas")


class EvidenciaError(ValueError):
    """Un item no cumple el esquema o no cita algo verificable."""


def parse_tiempo(texto: str) -> float:
    m = _TIEMPO.match(str(texto).strip())
    if not m:
        raise EvidenciaError(f"tiempo invalido {texto!r}: formato h:mm:ss[.d]")
    h, mm, ss, frac = m.groups()
    if int(mm) >= 60 or int(ss) >= 60:
        raise EvidenciaError(f"tiempo invalido {texto!r}")
    return int(h) * 3600 + int(mm) * 60 + int(ss) + (float("0." + frac) if frac else 0.0)


def formato_hhmmss(segundos: float) -> str:
    s = int(segundos)
    return f"{s // 3600:02d}{s % 3600 // 60:02d}{s % 60:02d}"


_normalizar_texto = normalizar_texto
_vacio = vacio


def limpiar_campos(campos: dict[str, Any]) -> dict[str, Any]:
    """Textos normalizados y campos vacios fuera, ANTES de calcular el id (ver feedback)."""
    limpio: dict[str, Any] = {}
    for k, v in campos.items():
        if k == "fotogramas" and isinstance(v, list | tuple):
            v = [_normalizar_texto(x) for x in v if not _vacio(x)]
        elif isinstance(v, str):
            v = _normalizar_texto(v)
        if not _vacio(v):
            limpio[k] = v
    return limpio


@dataclass(frozen=True, slots=True)
class EvidenceItem:
    id: str
    video_id: str
    t0: str
    t1: str
    modalidad: str
    tipo: str
    cita_literal: str
    afirmacion: str
    tema: str
    confianza: str
    extractor: str
    revisado_por: str
    provenance: str
    fotogramas: tuple[str, ...] = ()
    valor: str | None = None
    supersede: str | None = None
    notas: str | None = None

    @property
    def t0_s(self) -> float:
        return parse_tiempo(self.t0)

    @property
    def t1_s(self) -> float:
        return parse_tiempo(self.t1)


def contenido_canonico(campos: dict[str, Any]) -> str:
    """Representacion estable del contenido (sin `id`): claves ordenadas, textos normalizados."""
    limpio: dict[str, Any] = {}
    for clave in (*CAMPOS_OBLIGATORIOS, *CAMPOS_OPCIONALES):
        if clave not in campos or _vacio(campos[clave]):
            continue  # un campo en blanco no forma parte del contenido (ni del id)
        v = campos[clave]
        if clave == "fotogramas":
            limpio[clave] = sorted(_normalizar_texto(x) for x in v)
        elif isinstance(v, str):
            limpio[clave] = _normalizar_texto(v)
        else:
            limpio[clave] = v
    return json.dumps(limpio, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def hash_contenido(campos: dict[str, Any]) -> str:
    return hash_corto(contenido_canonico(campos))


def calcular_id(campos: dict[str, Any]) -> str:
    if _vacio(campos.get("t0")) or _vacio(campos.get("video_id")):
        raise EvidenciaError("video_id y t0 son obligatorios para calcular el id")
    marca = formato_hhmmss(parse_tiempo(campos["t0"]))
    return f"ev-{campos['video_id']}-{marca}-{hash_contenido(campos)}"


def _validar_campos(campos: dict[str, Any], origen: str) -> None:
    faltan = [c for c in CAMPOS_OBLIGATORIOS if _vacio(campos.get(c))]
    if faltan:
        raise EvidenciaError(f"{origen}: faltan campos obligatorios {faltan}")
    desconocidos = set(campos) - set(CAMPOS_OBLIGATORIOS) - set(CAMPOS_OPCIONALES) - {"id"}
    if desconocidos:
        raise EvidenciaError(f"{origen}: campos desconocidos {sorted(desconocidos)}")
    for clave in CAMPOS_TEXTO:
        if campos.get(clave) is not None and not isinstance(campos[clave], str):
            tipo_real = type(campos[clave]).__name__
            raise EvidenciaError(f"{origen}: {clave} debe ser texto entre comillas, no {tipo_real}")
    if not _VIDEO_ID.match(str(campos["video_id"])):
        raise EvidenciaError(
            f"{origen}: video_id {campos['video_id']!r} invalido (minusculas y digitos, p. ej. v4)"
        )
    for clave, permitidos in (
        ("tipo", TIPOS),
        ("modalidad", MODALIDADES),
        ("confianza", CONFIANZAS),
        ("extractor", EXTRACTORES),
        ("provenance", PROVENANCES),
    ):
        if campos[clave] not in permitidos:
            raise EvidenciaError(f"{origen}: {clave} {campos[clave]!r} no esta en {permitidos}")
    if not _TEMA.match(str(campos["tema"])):
        raise EvidenciaError(f"{origen}: tema invalido {campos['tema']!r} (p. ej. stop.nivel)")
    t0, t1 = parse_tiempo(campos["t0"]), parse_tiempo(campos["t1"])
    if not t0 < t1:
        raise EvidenciaError(f"{origen}: t0 debe ser menor que t1")
    cita = _normalizar_texto(campos["cita_literal"])
    afirmacion = _normalizar_texto(campos["afirmacion"])
    if len(cita) < 5:
        raise EvidenciaError(
            f"{origen}: la cita literal es obligatoria y no puede ser un placeholder"
        )
    if len(afirmacion) > 2 * len(cita) + 40:
        raise EvidenciaError(
            f"{origen}: la afirmacion es mucho mas larga que la cita; "
            "no se anade lo que la cita no dice"
        )
    if not _normalizar_texto(campos["revisado_por"]):
        raise EvidenciaError(f"{origen}: revisado_por es obligatorio")
    fotos = campos.get("fotogramas")
    if fotos is not None and (
        not isinstance(fotos, list) or not all(isinstance(x, str) and x for x in fotos)
    ):
        raise EvidenciaError(f"{origen}: fotogramas debe ser una lista de rutas")
    if campos.get("supersede") is not None and not _ID.match(str(campos["supersede"])):
        raise EvidenciaError(f"{origen}: supersede debe ser un id de evidencia")


def item_desde_dict(campos: dict[str, Any], origen: str = "item") -> EvidenceItem:
    _validar_campos(campos, origen)
    esperado = calcular_id(campos)
    if not _ID.match(esperado):
        raise EvidenciaError(f"{origen}: id calculado {esperado!r} fuera de formato")
    declarado = campos.get("id")
    if declarado != esperado:
        raise EvidenciaError(
            f"{origen}: id {declarado!r} no coincide con el contenido (esperado {esperado}); "
            "un item no se edita: se crea otro que lo supersede"
        )
    return EvidenceItem(
        id=esperado,
        video_id=str(campos["video_id"]),
        t0=str(campos["t0"]),
        t1=str(campos["t1"]),
        modalidad=str(campos["modalidad"]),
        tipo=str(campos["tipo"]),
        cita_literal=_normalizar_texto(campos["cita_literal"]),
        afirmacion=_normalizar_texto(campos["afirmacion"]),
        tema=str(campos["tema"]),
        confianza=str(campos["confianza"]),
        extractor=str(campos["extractor"]),
        revisado_por=_normalizar_texto(campos["revisado_por"]),
        provenance=str(campos["provenance"]),
        fotogramas=tuple(sorted(_normalizar_texto(x) for x in campos.get("fotogramas") or [])),
        valor=_normalizar_texto(campos["valor"]) if campos.get("valor") is not None else None,
        supersede=str(campos["supersede"]) if campos.get("supersede") else None,
        notas=_normalizar_texto(campos["notas"]) if campos.get("notas") else None,
    )


def cargar_item(ruta: Path) -> EvidenceItem:
    try:
        doc = cargar_yaml(ruta.read_text(encoding="utf-8"))
    except YamlError as exc:
        raise EvidenciaError(f"{ruta.name}: {exc}") from exc
    if not isinstance(doc, dict):
        raise EvidenciaError(f"{ruta.name}: no es un mapa YAML")
    item = item_desde_dict(doc, ruta.name)
    if ruta.stem != item.id:
        raise EvidenciaError(f"{ruta.name}: el nombre del fichero debe ser {item.id}.yaml")
    return item


def cargar_evidencia(directorio: Path) -> list[EvidenceItem]:
    """Todos los items bajo `directorio`; un fichero que no sea `*.yaml` (salvo README y `_*`)
    es error."""
    return cargar_directorio(directorio, cargar_item, EvidenciaError, "evidencia", lambda i: i.id)


def validar_contra_manifiesto(items: list[EvidenceItem], manifiesto: dict[str, Any]) -> list[str]:
    """La cita apunta a un video real, dentro de su duracion, y a fotogramas inventariados."""
    problemas: list[str] = []
    duraciones: dict[str, float] = {}
    for v in manifiesto.get("videos") or []:
        if not isinstance(v, dict):
            problemas.append(f"manifiesto: entrada de video invalida {v!r}")
            continue
        d = v.get("duracion_s")
        if isinstance(d, bool) or not isinstance(d, int | float):
            problemas.append(f"manifiesto: duracion_s no numerica en {v.get('video_id')!r}")
            continue
        duraciones[str(v.get("video_id"))] = float(d)
    rutas = {str(f.get("ruta")) for f in (manifiesto.get("ficheros") or []) if isinstance(f, dict)}
    por_id = {i.id: i for i in items}
    ids = set(por_id)
    for it in items:
        if it.video_id not in duraciones:
            problemas.append(f"{it.id}: video {it.video_id!r} no esta en el manifiesto")
        elif it.t1_s > duraciones[it.video_id] + TOLERANCIA_DURACION_S:
            problemas.append(
                f"{it.id}: t1 {it.t1} supera la duracion del video "
                f"({duraciones[it.video_id]:.1f} s)"
            )
        for foto in it.fotogramas:
            if foto not in rutas:
                problemas.append(f"{it.id}: fotograma no inventariado {foto!r}")
        if it.supersede and it.supersede not in ids:
            problemas.append(f"{it.id}: supersede a {it.supersede}, que no existe")
        if it.supersede == it.id:
            problemas.append(f"{it.id}: no puede supersederse a si mismo")
        elif it.supersede in por_id and por_id[it.supersede].tema != it.tema:
            problemas.append(
                f"{it.id}: supersede a {it.supersede}, de tema {por_id[it.supersede].tema!r}, "
                f"no {it.tema!r}; una correccion habla del mismo tema"
            )
    problemas += ciclos_de_supersede({i.id: i.supersede for i in items})
    return problemas


def escribir_item(
    directorio: Path,
    campos: dict[str, Any],
    comprobar: Callable[[EvidenceItem], list[str]] | None = None,
) -> Path:
    """Crea el fichero de un item nuevo con su id calculado. Nunca sobreescribe.

    `comprobar` recibe el item validado y devuelve problemas de contexto (video fuera del
    manifiesto, fotograma no inventariado...). Con alguno, no se escribe nada.
    """
    campos = limpiar_campos(campos)
    _validar_campos(campos, "nuevo")
    campos["id"] = calcular_id(campos)
    item = item_desde_dict(campos, "nuevo")
    problemas = comprobar(item) if comprobar else []
    if problemas:
        raise EvidenciaError("; ".join(problemas))
    carpeta = directorio / item.video_id
    carpeta.mkdir(parents=True, exist_ok=True)
    ruta = carpeta / f"{item.id}.yaml"
    if ruta.exists():
        raise EvidenciaError(f"ya existe {ruta.name}: mismo contenido, misma cita")
    doc: dict[str, Any] = {"id": item.id}
    for k, v in asdict(item).items():
        if k == "id" or v in (None, (), ""):
            continue
        doc[k] = list(v) if isinstance(v, tuple) else v
    ruta.write_text(
        yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=100),
        encoding="utf-8",
        newline="\n",
    )
    try:
        cargar_item(ruta)  # invariante: lo escrito se puede volver a cargar
    except EvidenciaError:
        ruta.unlink()
        raise
    return ruta
