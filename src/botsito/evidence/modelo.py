"""EvidenceItem (F06): la unidad minima de conocimiento extraido del corpus.

Un item es una cita verificable (video, t0, t1, fotogramas) con la cita literal, una afirmacion
normalizada que no anade nada que la cita no diga, un tema, un valor opcional, y quien lo extrajo
y quien lo reviso. Es INMUTABLE: su id incluye un hash del contenido, el nombre del fichero es el
id, y el historial de git se vigila (`historial.py`). Una correccion es un item nuevo que
`supersede` al anterior.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml

from botsito.yaml_estricto import YamlError, cargar_yaml

TIPOS = ("RULE_STATEMENT", "PARAMETER", "EXAMPLE_TRADE", "NO_TRADE", "MANAGEMENT", "UNKNOWN")
MODALIDADES = ("audio", "pantalla", "ambas")
CONFIANZAS = ("alta", "media", "baja")
EXTRACTORES = ("humano", "llm")
PROVENANCES = ("botsito", "bot-v2")
FICHERO_CONTRADICCIONES = "_contradicciones.yaml"
TOLERANCIA_DURACION_S = 1  # redondeo de ffprobe; no es un valor de negocio
_ID = re.compile(r"^ev-[a-z0-9]+-\d{6}-[0-9a-f]{8}$")
_VIDEO_ID = re.compile(r"^[a-z0-9]+$")
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
_TIEMPO = re.compile(r"^(\d+):(\d{2}):(\d{2})(?:\.(\d+))?$")
_TEMA = re.compile(r"^[a-z][a-z0-9_]*(\.[a-z0-9_]+)*$")
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


def _normalizar_texto(valor: object) -> str:
    return " ".join(str(valor).split())


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
        if clave not in campos or campos[clave] is None:
            continue
        v = campos[clave]
        if clave == "fotogramas":
            limpio[clave] = sorted(_normalizar_texto(x) for x in v)
        elif isinstance(v, str):
            limpio[clave] = _normalizar_texto(v)
        else:
            limpio[clave] = v
    return json.dumps(limpio, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def hash_contenido(campos: dict[str, Any]) -> str:
    return hashlib.sha256(contenido_canonico(campos).encode("utf-8")).hexdigest()[:8]


def calcular_id(campos: dict[str, Any]) -> str:
    marca = formato_hhmmss(parse_tiempo(campos["t0"]))
    return f"ev-{campos['video_id']}-{marca}-{hash_contenido(campos)}"


def _validar_campos(campos: dict[str, Any], origen: str) -> None:
    faltan = [c for c in CAMPOS_OBLIGATORIOS if c not in campos or campos[c] in (None, "")]
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
    items: list[EvidenceItem] = []
    for ruta in sorted(directorio.rglob("*.yaml")):
        if ruta.name == FICHERO_CONTRADICCIONES or ruta.name.startswith("_"):
            continue
        items.append(cargar_item(ruta))
    ids = [i.id for i in items]
    repetidos = sorted({i for i in ids if ids.count(i) > 1})
    if repetidos:
        raise EvidenciaError(f"ids repetidos: {repetidos}")
    return items


def validar_contra_manifiesto(items: list[EvidenceItem], manifiesto: dict[str, Any]) -> list[str]:
    """La cita apunta a un video real, dentro de su duracion, y a fotogramas inventariados."""
    problemas: list[str] = []
    duraciones = {v["video_id"]: float(v["duracion_s"]) for v in manifiesto.get("videos", [])}
    rutas = {f["ruta"] for f in manifiesto.get("ficheros", [])}
    ids = {i.id for i in items}
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
    return problemas


def activos(items: list[EvidenceItem]) -> list[EvidenceItem]:
    """Items no superseded por otro."""
    superseded = {i.supersede for i in items if i.supersede}
    return [i for i in items if i.id not in superseded]


def escribir_item(directorio: Path, campos: dict[str, Any]) -> Path:
    """Crea el fichero de un item nuevo con su id calculado. Nunca sobreescribe."""
    campos = {k: v for k, v in campos.items() if v not in (None, "", [], ())}
    campos["id"] = calcular_id(campos)
    item = item_desde_dict(campos, "nuevo")
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
    return ruta
