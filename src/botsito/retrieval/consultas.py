"""Consultas sobre el indice (F08, ADR-0010): `buscar` (texto) y `en_instante` (instante).

Orden fijo (video, t0_ms, tipo: evidencia antes que segmento, fuente); sin puntuacion. Cada
resultado lleva fuente (`ev-*`, `tr-*/n`, `fr-*/t_ms` o `contradiccion` con sus `ev-*`).
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any

from botsito.corpus.transcripcion import Segmento, texto_entre
from botsito.evidence.verificacion import COMODIN, CitaError, buscar_secuencia
from botsito.retrieval.indice import (
    TIPO_EVIDENCIA,
    TIPO_SEGMENTO,
    Documento,
    Indice,
    RetrievalError,
    token_de_busqueda,
)

TIPO_FOTOGRAMA = "fotograma"
TIPO_CONTRADICCION = "contradiccion"
MARGEN_MAX_MS = 120_000
_ORDEN_TIPO = {TIPO_EVIDENCIA: 0, TIPO_SEGMENTO: 1, TIPO_FOTOGRAMA: 2, TIPO_CONTRADICCION: 3}


@dataclass(frozen=True)
class Resultado:
    fuente: str
    tipo: str
    video: str
    t0_ms: int
    t1_ms: int
    texto: str
    fotograma: dict[str, Any] | None
    extra: dict[str, Any]

    def como_dict(self) -> dict[str, Any]:
        return {
            "fuente": self.fuente,
            "tipo": self.tipo,
            "video": self.video,
            "t0_ms": self.t0_ms,
            "t1_ms": self.t1_ms,
            "texto": self.texto,
            "fotograma": self.fotograma,
            "extra": self.extra,
        }


@dataclass(frozen=True)
class Opciones:
    video: str | None = None
    tema: str | None = None
    desde_ms: int | None = None
    hasta_ms: int | None = None
    solo: str | None = None  # evidencia | cruda
    frase: bool = False
    prefijo: bool = False
    top: int | None = None


@dataclass
class Respuesta:
    resultados: list[Resultado]
    avisos: list[str] = field(default_factory=list)


def _orden(r: Resultado) -> tuple[str, int, int, str]:
    return (r.video, r.t0_ms, _ORDEN_TIPO.get(r.tipo, 9), r.fuente)


def _comprobar_opciones(indice: Indice, opciones: Opciones) -> None:
    if opciones.video is not None and opciones.video not in indice.videos:
        raise RetrievalError(
            f"video desconocido {opciones.video!r} (fuentes.yaml: {list(indice.videos)})"
        )
    if (opciones.desde_ms is not None or opciones.hasta_ms is not None) and opciones.video is None:
        raise RetrievalError("--desde/--hasta exigen --video")
    if (
        opciones.desde_ms is not None
        and opciones.hasta_ms is not None
        and opciones.desde_ms > opciones.hasta_ms
    ):
        raise RetrievalError("--desde es posterior a --hasta")
    if opciones.solo not in (None, "evidencia", "cruda"):
        raise RetrievalError("--solo admite evidencia o cruda")
    if opciones.top is not None and opciones.top < 1:
        raise RetrievalError("--top debe ser >= 1")


def _trozos(texto: str) -> list[list[str]]:
    if "[" in texto.replace(COMODIN, "") or "]" in texto.replace(COMODIN, ""):
        raise RetrievalError("la frase solo admite corchetes en el comodin [...]")
    trozos = [token_de_busqueda(p) for p in texto.split(COMODIN)]
    if any(not t for t in trozos):
        raise RetrievalError("un trozo de la frase esta vacio (comodin al borde o duplicado)")
    return trozos


def _casa_and(doc: Documento, terminos: list[str], prefijo: bool) -> bool:
    todos = doc.todos
    if not prefijo:
        return all(t in todos for t in terminos)
    return all(any(x.startswith(t) for x in todos) for t in terminos)


def _casa_frase_item(doc: Documento, trozos: list[list[str]]) -> bool:
    return any(buscar_secuencia(lista, trozos) for lista in doc.campos.values() if lista)


def _filtra(doc: Documento, opciones: Opciones) -> bool:
    if opciones.video and doc.video != opciones.video:
        return False
    if opciones.solo == "evidencia" and doc.tipo != TIPO_EVIDENCIA:
        return False
    if opciones.solo == "cruda" and doc.tipo != TIPO_SEGMENTO:
        return False
    if opciones.tema:
        if doc.tipo != TIPO_EVIDENCIA:
            return False
        tema = str(doc.extra.get("tema"))
        if not (tema == opciones.tema or tema.startswith(opciones.tema + ".")):
            return False
    if opciones.desde_ms is not None and doc.t1_ms < opciones.desde_ms:
        return False
    return not (opciones.hasta_ms is not None and doc.t0_ms > opciones.hasta_ms)


def _resultado(indice: Indice, doc: Documento) -> Resultado:
    return Resultado(
        doc.fuente,
        doc.tipo,
        doc.video,
        doc.t0_ms,
        doc.t1_ms,
        doc.texto,
        indice.fotograma_en(doc.video, doc.t0_ms),
        dict(doc.extra),
    )


def _frase_en_cruda(
    indice: Indice, video: str, trozos: list[list[str]], opciones: Opciones
) -> list[Resultado]:
    """La frase puede cruzar segmentos: se busca sobre el flujo de tokens de toda la cruda y se
    devuelven los segmentos tocados (`tr-*/n0` o `tr-*/n0-n1`)."""
    segmentos = indice.segmentos.get(video)
    tid = indice.transcripciones.get(video)
    if not segmentos or tid is None:
        return []
    docs = {
        d.extra["n"]: d for d in indice.documentos if d.tipo == TIPO_SEGMENTO and d.video == video
    }
    flujo: list[str] = []
    dueno: list[int] = []
    for s in segmentos:
        capa = docs[s.n].campos.get("corregida") or docs[s.n].campos["cruda"]
        flujo.extend(capa)
        dueno.extend([s.n] * len(capa))
    salida: list[Resultado] = []
    vistos: set[tuple[int, int]] = set()
    por_n = {s.n: s for s in segmentos}
    for inicio, fin, _cortes in buscar_secuencia(flujo, trozos):
        n0, n1 = dueno[inicio], dueno[fin - 1]
        if (n0, n1) in vistos:
            continue
        vistos.add((n0, n1))
        tocados = [por_n[n] for n in range(n0, n1 + 1) if n in por_n]
        if not tocados:
            continue
        fuente = f"{tid}/{n0}" if n0 == n1 else f"{tid}/{n0}-{n1}"
        base = docs[n0]
        extra = dict(base.extra)
        extra["n"] = n0
        extra["n_hasta"] = n1
        extra["senales"] = sorted({x for s in tocados for x in s.senales})
        extra["duda_glosario"] = any(docs[s.n].extra["duda_glosario"] for s in tocados)
        extra["texto_corregido"] = (
            None
            if n0 == n1
            else " ".join((docs[s.n].extra["texto_corregido"] or s.texto) for s in tocados)
        )
        if n0 == n1:
            extra["texto_corregido"] = base.extra["texto_corregido"]
        r = Resultado(
            fuente,
            TIPO_SEGMENTO,
            video,
            tocados[0].t0_ms,
            tocados[-1].t1_ms,
            " ".join(s.texto for s in tocados),
            indice.fotograma_en(video, tocados[0].t0_ms),
            extra,
        )
        if _filtra(
            Documento(fuente, TIPO_SEGMENTO, video, r.t0_ms, r.t1_ms, {}, "", extra), opciones
        ):
            salida.append(r)
    return salida


OPCIONES_POR_DEFECTO = Opciones()


def buscar(indice: Indice, texto: str, opciones: Opciones = OPCIONES_POR_DEFECTO) -> Respuesta:
    """AND de tokens de busqueda por documento; `frase` exige la secuencia (con `[...]`) por
    campo en los items y sobre toda la cruda en los segmentos; `prefijo` casa por inicio."""
    _comprobar_opciones(indice, opciones)
    if opciones.frase:
        try:
            trozos = _trozos(texto)
        except CitaError as exc:
            raise RetrievalError(str(exc)) from exc
        terminos: list[str] = []
    else:
        terminos = token_de_busqueda(texto)
        trozos = []
        if not terminos:
            raise RetrievalError("la consulta no tiene tokens")
    salida: list[Resultado] = []
    for doc in indice.documentos:
        if not _filtra(doc, opciones):
            continue
        if opciones.frase:
            if doc.tipo != TIPO_EVIDENCIA:
                continue  # los segmentos van por el flujo completo (pueden cruzar segmentos)
            if _casa_frase_item(doc, trozos):
                salida.append(_resultado(indice, doc))
        elif _casa_and(doc, terminos, opciones.prefijo):
            salida.append(_resultado(indice, doc))
    if opciones.frase and opciones.solo != "evidencia" and not opciones.tema:
        videos = [opciones.video] if opciones.video else list(indice.videos)
        for v in videos:
            salida += _frase_en_cruda(indice, v, trozos, opciones)
    salida.sort(key=_orden)
    if opciones.top is not None:
        salida = salida[: opciones.top]
    return Respuesta(salida, list(indice.avisos))


def _contradicciones_de(indice: Indice, ids: set[str], video: str, t_ms: int) -> list[Resultado]:
    salida: list[Resultado] = []
    for c in indice.contradicciones:
        implicados = [i["id"] for i in c["items"]]
        if not ids & set(implicados):
            continue
        t0 = t_ms
        salida.append(
            Resultado(
                f"contradiccion {c['tema']}",
                TIPO_CONTRADICCION,
                video,
                t0,
                t0,
                " frente a ".join(str(v) for v in c["valores"]),
                None,
                {"tema": c["tema"], "valores": list(c["valores"]), "items": implicados},
            )
        )
    return salida


def en_instante(indice: Indice, video: str, t_ms: int, margen_ms: int = 10_000) -> Respuesta:
    """Todo lo que ocurre en `t_ms` de `video` con margen: items (por t0), segmentos de la cruda
    activa (por n), el fotograma de referencia y las contradicciones de esos items."""
    if video not in indice.videos:
        raise RetrievalError(f"video desconocido {video!r} (fuentes.yaml: {list(indice.videos)})")
    if t_ms < 0:
        raise RetrievalError("el instante debe ser >= 0")
    if not 0 <= margen_ms <= MARGEN_MAX_MS:
        raise RetrievalError(f"el margen debe estar entre 0 y {MARGEN_MAX_MS // 1000} s")
    salida: list[Resultado] = []
    ids: set[str] = set()
    for doc in indice.documentos:
        if (
            doc.tipo == TIPO_EVIDENCIA
            and doc.video == video
            and doc.t0_ms - margen_ms <= t_ms <= doc.t1_ms + margen_ms
        ):
            salida.append(_resultado(indice, doc))
            ids.add(doc.fuente)
    segmentos: Sequence[Segmento] = indice.segmentos.get(video, [])
    docs = {
        d.extra["n"]: d for d in indice.documentos if d.tipo == TIPO_SEGMENTO and d.video == video
    }
    for s in texto_entre(list(segmentos), t_ms, t_ms, margen_ms):
        salida.append(_resultado(indice, docs[s.n]))
    foto = indice.fotograma_en(video, t_ms)
    if foto is not None:
        salida.append(
            Resultado(
                foto["referencia"],
                TIPO_FOTOGRAMA,
                video,
                t_ms // 1000 * 1000,
                t_ms // 1000 * 1000,
                "",
                foto,
                {},
            )
        )
    # En `at` el orden es por bloques (items, segmentos, fotograma) y dentro de cada bloque por
    # tiempo; las contradicciones cierran la lista (no tienen instante propio), por tema.
    salida.sort(key=lambda r: (_ORDEN_TIPO.get(r.tipo, 9), r.t0_ms, r.fuente))
    salida += sorted(_contradicciones_de(indice, ids, video, t_ms), key=lambda r: r.fuente)
    return Respuesta(salida, list(indice.avisos))
