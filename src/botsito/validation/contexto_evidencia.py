"""Composicion del contexto de verificacion de la evidencia (F07, ADR-0009).

`evidence` y `corpus` son capas hermanas (ADR-0006): `validation` y `retrieval` (ADR-0010) son
quienes juntan las crudas y los fotogramas del corpus con los items de evidencia. Aqui se
construye el `ContextoEvidencia` que consumen `evidence.modelo.validar_contra_manifiesto`,
`evidence.modelo.verificar_citas` y `evidence.propuestas.comprobar`.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from botsito.corpus.manifiestos_fotogramas import Fotogramas, referencias_conocidas
from botsito.corpus.manifiestos_fotogramas import cargar_todos as cargar_fotogramas
from botsito.corpus.manifiestos_transcripcion import (
    Transcripcion,
    activos,
    cargar_todos,
    carpeta_de,
)
from botsito.corpus.pipeline_transcripcion import cargar_cruda, dudas_de
from botsito.corpus.transcripcion import Segmento
from botsito.evidence.propuestas import FICHERO_TEMAS, Temas, cargar_temas
from botsito.evidence.verificacion import ContextoEvidencia, SegmentoCitable


@dataclass
class _Cache:
    crudas: dict[str, Sequence[SegmentoCitable] | None] = field(default_factory=dict)
    dudas: dict[str, set[int]] = field(default_factory=dict)


def construir_contexto(
    repo: Path,
    carpeta_datos: Path,
    manifiesto_corpus: dict[str, Any] | None,
    transcripciones: list[Transcripcion] | None = None,
    fotogramas: list[Fotogramas] | None = None,
) -> tuple[ContextoEvidencia, Temas]:
    """Contexto completo desde los manifiestos del repo. Las crudas se leen perezosamente y
    `None` significa "no esta en esta maquina"."""
    trs = cargar_todos(repo) if transcripciones is None else transcripciones
    frs = cargar_fotogramas(repo) if fotogramas is None else fotogramas
    por_id = {t.id: t for t in trs}
    activas = {t.video_id: t.id for t in activos(trs)}
    reemplazadas = {t.supersede: t.id for t in trs if t.supersede}
    cache = _Cache()

    def crudas(tid: str) -> Sequence[SegmentoCitable] | None:
        if tid not in cache.crudas:
            t = por_id.get(tid)
            carpeta = carpeta_de(carpeta_datos, t) if t else None
            if carpeta is not None and (carpeta / "cruda.jsonl").is_file():
                segmentos: list[Segmento] = cargar_cruda(carpeta)
                cache.crudas[tid] = segmentos
            else:
                cache.crudas[tid] = None
        return cache.crudas[tid]

    def dudas(tid: str) -> set[int]:
        if tid not in cache.dudas:
            t = por_id.get(tid)
            cache.dudas[tid] = dudas_de(carpeta_de(carpeta_datos, t)) if t else set()
        return cache.dudas[tid]

    ruta_temas = repo / FICHERO_TEMAS
    # Sin taxonomia (repos de prueba sin F07) el contexto sigue sirviendo para citas y
    # referencias; `propuestas.comprobar` rechazara cualquier tema por raiz desconocida.
    temas = cargar_temas(ruta_temas) if ruta_temas.is_file() else Temas(frozenset(), frozenset())
    contexto = ContextoEvidencia(
        referencias=referencias_conocidas(frs, manifiesto_corpus),
        crudas=crudas,
        transcripciones={t.id: t.video_id for t in trs},
        activas=activas,
        reemplazadas=reemplazadas,
        dudas=dudas,
        temas_raiz=temas.raices,
        valores_cerrados=temas.valores_cerrados,
    )
    return contexto, temas
