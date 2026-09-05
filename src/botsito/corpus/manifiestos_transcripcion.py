"""Manifiestos INMUTABLES de transcripcion (F04, ADR-0007): carga, esquema, activos, comprobacion.

Un manifiesto por transcripcion cruda en `knowledge/corpus/transcripciones/<id>.yaml`
(versionado; el historial de git lo vigila como a la evidencia). `reemplaza_a` enlaza una
retranscripcion con la anterior; `activos()` da la vigente por video. `comprobar` recomputa: la
cruda en disco debe tener el sha256 del manifiesto y `corregida.jsonl` debe ser exactamente
`cruda + glosario actual` (la corregida es regenerable, no se guarda su hash).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from botsito.comun import ids
from botsito.comun.documentos import activos as _activos
from botsito.comun.documentos import ficheros_de, sha256_hex
from botsito.comun.yaml_estricto import YamlError, cargar_yaml
from botsito.corpus.glosario import Glosario, aplicar, correcciones_jsonl
from botsito.corpus.pipeline_transcripcion import (
    CARPETA_DATOS,
    DIRECTORIO_MANIFIESTOS,
    FICHERO_CORRECCIONES,
    FICHERO_CORREGIDA,
    FICHERO_CRUDA,
    SCHEMA_VERSION,
)
from botsito.corpus.transcripcion import a_jsonl, desde_jsonl

CAMPOS_OBLIGATORIOS = (
    "schema_version",
    "transcripcion_id",
    "video_id",
    "fichero_video",
    "sha256_video",
    "sha256_wav",
    "duracion_video_s",
    "duracion_wav_s",
    "muestras",
    "carpeta",
    "motor",
    "ffmpeg",
    "corte",
    "silencios_detectados",
    "fragmentos",
    "cortes_forzados_m",
    "segmentos",
    "recortados",
    "descartados",
    "ms_con_habla",
    "senales",
    "hueco_transcripcion_s",
    "huecos",
    "sha256_cruda",
    "glosario_sha256_inicial",
    "generado_el",
)
CAMPOS_OPCIONALES = ("reemplaza_a",)


class ManifiestoTranscripcionError(ValueError):
    """El manifiesto no cumple su esquema o no coincide con el disco."""


@dataclass(frozen=True, slots=True)
class Transcripcion:
    id: str
    video_id: str
    nombre: str
    sha256_cruda: str
    carpeta: str
    segmentos: int
    supersede: str | None  # reemplaza_a (mismo nombre que evidencia/feedback para `activos`)
    doc: dict[str, Any]


def cargar_manifiesto(ruta: Path) -> Transcripcion:
    try:
        doc = cargar_yaml(ruta.read_text(encoding="utf-8"))
    except YamlError as exc:
        raise ManifiestoTranscripcionError(f"{ruta.name}: {exc}") from exc
    if not isinstance(doc, dict):
        raise ManifiestoTranscripcionError(f"{ruta.name}: no es un mapa")
    return validar(doc, ruta.name)


def validar(doc: dict[str, Any], origen: str) -> Transcripcion:
    faltan = [c for c in CAMPOS_OBLIGATORIOS if c not in doc]
    if faltan:
        raise ManifiestoTranscripcionError(f"{origen}: faltan campos {faltan}")
    ajenos = sorted(set(doc) - set(CAMPOS_OBLIGATORIOS) - set(CAMPOS_OPCIONALES))
    if ajenos:
        raise ManifiestoTranscripcionError(f"{origen}: campos desconocidos {ajenos}")
    if doc["schema_version"] != SCHEMA_VERSION:
        raise ManifiestoTranscripcionError(f"{origen}: schema_version no soportada")
    tid = doc["transcripcion_id"]
    if not ids.es_id_de("transcripcion", tid):
        raise ManifiestoTranscripcionError(f"{origen}: transcripcion_id invalido {tid!r}")
    if origen != "manifiesto" and Path(origen).stem != tid:
        raise ManifiestoTranscripcionError(f"{origen}: el fichero debe llamarse {tid}.yaml")
    for c in ("video_id", "fichero_video", "sha256_video", "sha256_wav", "carpeta", "sha256_cruda"):
        if not isinstance(doc[c], str) or not doc[c].strip():
            raise ManifiestoTranscripcionError(f"{origen}: {c} debe ser texto no vacio")
    for c in ("sha256_video", "sha256_wav", "sha256_cruda", "glosario_sha256_inicial"):
        v = doc[c]
        if not isinstance(v, str) or len(v) != 64 or any(ch not in "0123456789abcdef" for ch in v):
            raise ManifiestoTranscripcionError(f"{origen}: {c} invalido")
    if not tid.endswith(doc["sha256_cruda"][:8]):
        raise ManifiestoTranscripcionError(
            f"{origen}: el sufijo del id no coincide con sha256_cruda"
        )
    nombre = tid[len(f"tr-{doc['video_id']}-") : -9]
    if not nombre or not str(doc["carpeta"]).endswith(f"/{doc['video_id']}/{nombre}"):
        raise ManifiestoTranscripcionError(
            f"{origen}: carpeta {doc['carpeta']!r} no coincide con el id"
        )
    for c in (
        "muestras",
        "segmentos",
        "recortados",
        "descartados",
        "ms_con_habla",
        "silencios_detectados",
    ):
        v = doc[c]
        if isinstance(v, bool) or not isinstance(v, int) or v < 0:
            raise ManifiestoTranscripcionError(f"{origen}: {c} debe ser entero >= 0")
    if doc["segmentos"] < 1:
        raise ManifiestoTranscripcionError(
            f"{origen}: una transcripcion sin segmentos no se registra"
        )
    for c in ("motor", "corte", "senales"):
        if not isinstance(doc[c], dict):
            raise ManifiestoTranscripcionError(f"{origen}: {c} debe ser un mapa")
    if not isinstance(doc["motor"].get("modelo"), str):
        raise ManifiestoTranscripcionError(f"{origen}: motor.modelo ausente")
    for c in ("fragmentos", "cortes_forzados_m", "huecos"):
        if not isinstance(doc[c], list):
            raise ManifiestoTranscripcionError(f"{origen}: {c} debe ser una lista")
    if "reemplaza_a" in doc and not ids.es_id_de("transcripcion", doc["reemplaza_a"]):
        raise ManifiestoTranscripcionError(f"{origen}: reemplaza_a debe ser un transcripcion_id")
    return Transcripcion(
        tid,
        str(doc["video_id"]),
        nombre,
        str(doc["sha256_cruda"]),
        str(doc["carpeta"]),
        int(doc["segmentos"]),
        doc.get("reemplaza_a"),
        doc,
    )


def cargar_todos(repo: Path) -> list[Transcripcion]:
    carpeta = repo / DIRECTORIO_MANIFIESTOS
    if not carpeta.is_dir():
        return []
    items = [
        cargar_manifiesto(p)
        for p in ficheros_de(carpeta, ManifiestoTranscripcionError, DIRECTORIO_MANIFIESTOS)
    ]
    conocidos = {t.id for t in items}
    for t in items:
        if t.supersede and t.supersede not in conocidos:
            raise ManifiestoTranscripcionError(f"{t.id}: reemplaza_a {t.supersede} no existe")
        if t.supersede == t.id:
            raise ManifiestoTranscripcionError(f"{t.id}: no puede reemplazarse a si misma")
    return items


def activos(items: list[Transcripcion]) -> list[Transcripcion]:
    return _activos(items)


def activa_de(items: list[Transcripcion], video_id: str, tid: str | None = None) -> Transcripcion:
    if tid is not None:
        for t in items:
            if t.id == tid:
                return t
        raise ManifiestoTranscripcionError(f"no existe la transcripcion {tid}")
    vivas = [t for t in activos(items) if t.video_id == video_id]
    if not vivas:
        raise ManifiestoTranscripcionError(f"no hay transcripcion activa para {video_id}")
    if len(vivas) > 1:
        raise ManifiestoTranscripcionError(
            f"{video_id} tiene {len(vivas)} transcripciones activas {[t.id for t in vivas]}: "
            "indica --transcripcion o marca reemplaza_a"
        )
    return vivas[0]


def carpeta_de(carpeta_datos: Path, t: Transcripcion) -> Path:
    return carpeta_datos / Path(t.carpeta)


def comprobar(
    items: list[Transcripcion], carpeta_datos: Path, glosario: Glosario | None
) -> tuple[list[str], list[str]]:
    """(errores, avisos). Carpeta ausente = aviso (los datos no viajan en git); cruda alterada,
    corregida que no es cruda + glosario, o correcciones con otro glosario = error."""
    errores: list[str] = []
    avisos: list[str] = []
    for t in items:
        carpeta = carpeta_de(carpeta_datos, t)
        cruda = carpeta / FICHERO_CRUDA
        if not cruda.is_file():
            avisos.append(f"{t.id}: {FICHERO_CRUDA} no esta en esta maquina ({carpeta})")
            continue
        datos = cruda.read_bytes()
        if sha256_hex(datos) != t.sha256_cruda:
            errores.append(f"{t.id}: {FICHERO_CRUDA} alterada (sha256 distinto del manifiesto)")
            continue
        segmentos = desde_jsonl(datos.decode("utf-8"))
        if len(segmentos) != t.segmentos:
            errores.append(f"{t.id}: {len(segmentos)} segmentos, el manifiesto dice {t.segmentos}")
        if glosario is None:
            continue
        corregida, registro, dudas = aplicar(segmentos, glosario, t.id)
        esperada = a_jsonl(corregida)
        fichero = carpeta / FICHERO_CORREGIDA
        if not fichero.is_file() or fichero.read_bytes().decode("utf-8") != esperada:
            errores.append(
                f"{t.id}: {FICHERO_CORREGIDA} no es cruda + glosario ({glosario.version}); "
                "regenera con `botsito corpus glossary apply`"
            )
        correcciones = carpeta / FICHERO_CORRECCIONES
        if not correcciones.is_file() or correcciones.read_bytes().decode(
            "utf-8"
        ) != correcciones_jsonl(glosario, registro, dudas):
            errores.append(f"{t.id}: {FICHERO_CORRECCIONES} no coincide con el glosario actual")
    return errores, avisos


def ruta_datos(carpeta_datos: Path, video_id: str, nombre: str) -> Path:
    return carpeta_datos / CARPETA_DATOS / video_id / nombre
