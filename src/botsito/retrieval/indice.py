"""Indice en memoria de la base de conocimiento (F08, ADR-0010).

Documentos: items de evidencia (todos; los reemplazados marcados) y segmentos de las
transcripciones ACTIVAS (cruda + corregida si existe). Los fotogramas no tienen texto: entran
como "fotograma de referencia" de cada resultado (`corpus.manifiestos_fotogramas.referencia_en`).
El token de busqueda es el de F07 (`evidence.verificacion.tokens`) con los acentos plegados y los
numeros normalizados: `0,75` = `0.75` = `0.750`; `límite` = `limite`. `tokens()` de F07 no cambia.
"""

from __future__ import annotations

import contextlib
import re
import unicodedata
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from botsito.corpus.fotogramas import nombre_fichero
from botsito.corpus.inventario import InventarioError, cargar_fuentes
from botsito.corpus.manifiestos_fotogramas import Fotogramas, referencia_en
from botsito.corpus.manifiestos_fotogramas import activos as fotogramas_activos
from botsito.corpus.manifiestos_fotogramas import cargar_todos as cargar_fotogramas
from botsito.corpus.manifiestos_fotogramas import carpeta_de as carpeta_fotogramas
from botsito.corpus.manifiestos_transcripcion import (
    Transcripcion,
    activos,
    cargar_todos,
    carpeta_de,
)
from botsito.corpus.pipeline_transcripcion import FICHERO_CRUDA, Capas, cargar_capas
from botsito.corpus.transcripcion import Segmento
from botsito.evidence import contradicciones
from botsito.evidence.modelo import EvidenceItem, cargar_evidencia
from botsito.evidence.verificacion import tokens

TIPO_EVIDENCIA = "evidencia"
TIPO_SEGMENTO = "segmento"
_NUMERO = re.compile(r"^\d+[.,]\d+$")


class RetrievalError(ValueError):
    """Error de dominio de la busqueda (video desconocido, consulta invalida...)."""


def _plegar(token: str) -> str:
    """Sin marcas combinantes (acentos, dieresis, virgulilla): `límite` -> `limite`, `ñ` -> `n`."""
    return "".join(
        c for c in unicodedata.normalize("NFD", token) if unicodedata.category(c) != "Mn"
    )


def token_de_busqueda(texto: str) -> list[str]:
    """Tokens de F07 con acentos plegados y numeros con separador normalizados por `Decimal`
    (como `contradicciones.normalizar_valor`)."""
    salida: list[str] = []
    for t in tokens(texto):
        if _NUMERO.match(t):
            with contextlib.suppress(InvalidOperation):
                t = format(Decimal(t.replace(",", ".")).normalize(), "f")
        salida.append(_plegar(t))
    return salida


@dataclass(frozen=True)
class Documento:
    """Unidad indexada: un item de evidencia o un segmento de una cruda activa."""

    fuente: str
    tipo: str
    video: str
    t0_ms: int
    t1_ms: int
    campos: dict[str, list[str]]  # tokens de busqueda por campo (la frase se busca por campo)
    texto: str  # cita literal o texto de la cruda
    extra: dict[str, Any]

    @property
    def todos(self) -> set[str]:
        return {t for lista in self.campos.values() for t in lista}


@dataclass
class Indice:
    repo: Path
    carpeta_datos: Path
    videos: tuple[str, ...]
    items: list[EvidenceItem]
    documentos: list[Documento]
    segmentos: dict[str, list[Segmento]]  # video -> cruda activa (si esta en la maquina)
    transcripciones: dict[str, str]  # video -> id de la transcripcion activa
    fotogramas: dict[str, Fotogramas]  # video -> manifiesto activo
    contradicciones: list[dict[str, Any]]
    avisos: list[str] = field(default_factory=list)
    reemplazados: dict[str, str] = field(
        default_factory=dict
    )  # item viejo -> item que lo supersede

    def ruta_fotograma(self, referencia: str) -> str | None:
        """Ruta POSIX relativa al repo del fichero del fotograma, si esta en la maquina y dentro
        del repo; None en otro caso (la referencia sigue siendo citable)."""
        fid, _, t = referencia.rpartition("/")
        fr = next((f for f in self.fotogramas.values() if f.id == fid), None)
        if fr is None:
            return None
        fichero = carpeta_fotogramas(self.carpeta_datos, fr) / nombre_fichero(int(t))
        if not fichero.is_file():
            return None
        try:
            return fichero.resolve().relative_to(self.repo.resolve()).as_posix()
        except ValueError:
            return None

    def fotograma_en(self, video: str, t_ms: int) -> dict[str, Any] | None:
        fr = self.fotogramas.get(video)
        if fr is None:
            return None
        ref = referencia_en(fr, t_ms)
        if ref is None:
            return None
        return {"referencia": ref, "ruta": self.ruta_fotograma(ref)}


def _documento_item(it: EvidenceItem, reemplazados: dict[str, str]) -> Documento:
    campos = {
        "cita_literal": token_de_busqueda(it.cita_literal),
        "afirmacion": token_de_busqueda(it.afirmacion),
        "tema": token_de_busqueda(it.tema.replace(".", " ").replace("_", " ")),
        "valor": token_de_busqueda(it.valor or ""),
        "notas": token_de_busqueda(it.notas or ""),
    }
    extra: dict[str, Any] = {
        "afirmacion": it.afirmacion,
        "tema": it.tema,
        "valor": it.valor,
        "tipo_item": it.tipo,
        "confianza": it.confianza,
        "modalidad": it.modalidad,
        "transcripcion": it.transcripcion,
        "provenance": it.provenance,
        "fotogramas": list(it.fotogramas),
        "supersede": it.supersede,
        "reemplazado_por": reemplazados.get(it.id),
    }
    return Documento(
        it.id, TIPO_EVIDENCIA, it.video_id, it.t0_ms, it.t1_ms, campos, it.cita_literal, extra
    )


def _documento_segmento(
    tid: str, video: str, s: Segmento, corregido: str | None, duda: bool
) -> Documento:
    campos = {"cruda": token_de_busqueda(s.texto)}
    if corregido is not None and corregido != s.texto:
        campos["corregida"] = token_de_busqueda(corregido)
    extra: dict[str, Any] = {
        "n": s.n,
        "transcripcion": tid,
        "texto_corregido": corregido if corregido is not None and corregido != s.texto else None,
        "senales": list(s.senales),
        "duda_glosario": duda,
    }
    return Documento(f"{tid}/{s.n}", TIPO_SEGMENTO, video, s.t0_ms, s.t1_ms, campos, s.texto, extra)


def _capas_de(carpeta_datos: Path, t: Transcripcion) -> Capas | None:
    carpeta = carpeta_de(carpeta_datos, t)
    if not (carpeta / FICHERO_CRUDA).is_file():
        return None
    return cargar_capas(carpeta)


def construir_indice(repo: Path, carpeta_datos: Path) -> Indice:
    """Indice completo desde el repo y la carpeta de datos. Crudas o fotogramas ausentes no son
    error: quedan avisos y el indice sirve con lo que hay (solo evidencia, como minimo)."""
    try:
        videos = tuple(
            v.video_id
            for v in cargar_fuentes(repo / "knowledge" / "corpus" / "fuentes.yaml").videos
        )
    except InventarioError as exc:
        raise RetrievalError(str(exc)) from exc
    items = cargar_evidencia(repo / "knowledge" / "evidence")
    reemplazados = {it.supersede: it.id for it in items if it.supersede}
    documentos = [_documento_item(it, reemplazados) for it in items]
    avisos: list[str] = []
    segmentos: dict[str, list[Segmento]] = {}
    transcripciones: dict[str, str] = {}
    for t in activos(cargar_todos(repo)):
        transcripciones[t.video_id] = t.id
        capas = _capas_de(carpeta_datos, t)
        if capas is None:
            avisos.append(f"cruda de {t.id} ausente en data/: {t.video_id} solo por evidencia")
            continue
        segmentos[t.video_id] = capas.cruda
        corregidas = {s.n: s.texto for s in capas.corregida or []}
        for s in capas.cruda:
            documentos.append(
                _documento_segmento(t.id, t.video_id, s, corregidas.get(s.n), s.n in capas.dudas)
            )
    for v in videos:
        if v not in transcripciones:
            avisos.append(f"{v} sin transcripcion activa: solo por evidencia")
    fotogramas = {f.video_id: f for f in fotogramas_activos(cargar_fotogramas(repo))}
    try:
        carpeta_datos.resolve().relative_to(repo.resolve())
    except ValueError:
        avisos.append("la carpeta de datos esta fuera del repo: las rutas de fotogramas se omiten")
    return Indice(
        repo,
        carpeta_datos,
        videos,
        items,
        documentos,
        segmentos,
        transcripciones,
        fotogramas,
        contradicciones.detectar(items),
        avisos,
        reemplazados,
    )
