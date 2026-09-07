"""Verificacion mecanica de citas (F07, ADR-0009).

Una cita de audio se localiza POR TOKENS dentro de los segmentos de la cruda que tocan la
ventana `[t0 - TOL, t1 + TOL]`, y su tiempo real se lee de las `palabras` de la cruda: la cita
queda atada al tiempo, no solo al texto. Una cita de pantalla se ata a una referencia
`fr-<id>/<t_ms>` del mismo video dentro del tramo.

Este modulo NO importa `botsito.corpus` (ADR-0006: `evidence` y `corpus` son capas hermanas e
independientes): recibe los segmentos por un protocolo estructural que los `Segmento` reales
cumplen; quien compone ambas capas es `validation/knowledge.py` o la CLI.
"""

from __future__ import annotations

import re
import unicodedata
from bisect import bisect_right
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from typing import Protocol

from botsito.comun import ids

# Constantes tecnicas de la verificacion (no son parametros de negocio).
TOLERANCIA_CITA_MS = 2000  # no-negocio: holgura entre la ventana declarada y las palabras
TOLERANCIA_FOTOGRAMA_MS = 1000  # no-negocio: holgura del fotograma respecto al tramo
MIN_TOKENS_CITA = 4  # no-negocio: una cita mas corta casa en cualquier sitio
MIN_TOKENS_TROZO = 3  # no-negocio: cada trozo entre comodines
MAX_COMODINES = 2  # no-negocio: comodines por cita
COMODIN = "[...]"

_ELIPSIS = re.compile(r"\.{2,}|…")
_SEPARADORES = re.compile(r"[-‐-―'’`]")
# Un numero con separadores interiores (`0.75`, `16,5`, `1:3`, `1.19537`) es UN token; el resto
# de tokens son secuencias de letras/digitos (`m15`, `breakeven`, `vale`).
_TOKEN = re.compile(r"\d+(?:[.,:]\d+)+|\w+")


class CitaError(ValueError):
    """La cita no se puede verificar: mal formada, no localizada o fuera de tiempo."""


class PalabraCitable(Protocol):
    @property
    def t0_ms(self) -> int: ...
    @property
    def t1_ms(self) -> int: ...
    @property
    def texto(self) -> str: ...


class SegmentoCitable(Protocol):
    @property
    def n(self) -> int: ...
    @property
    def t0_ms(self) -> int: ...
    @property
    def t1_ms(self) -> int: ...
    @property
    def texto(self) -> str: ...
    @property
    def senales(self) -> tuple[str, ...]: ...
    @property
    def palabras(self) -> tuple[PalabraCitable, ...]: ...


@dataclass(frozen=True, slots=True)
class Token:
    texto: str
    segmento: int
    t0_ms: int
    t1_ms: int
    senales: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Localizacion:
    t0_ms: int
    t1_ms: int
    segmentos: tuple[int, ...]
    coincidencias: int
    trozos: int
    senales: tuple[str, ...] = ()
    avisos: tuple[str, ...] = ()


def _limpiar(texto: str) -> str:
    """NFC, sin elipsis del ASR y con guiones/apostrofes como espacio, CONSERVANDO la longitud
    (cada caracter sustituido por un espacio) para poder alinear con las palabras."""
    nfc = unicodedata.normalize("NFC", texto)
    nfc = _ELIPSIS.sub(lambda m: " " * len(m.group()), nfc)
    return _SEPARADORES.sub(" ", nfc)


def tokens(texto: str) -> list[str]:
    """Tokens normalizados de un texto (cita o cruda)."""
    return [m.group().casefold() for m in _TOKEN.finditer(_limpiar(texto))]


def _sin_espacios(texto: str) -> str:
    return "".join(texto.split())


def tokens_de_segmento(s: SegmentoCitable) -> tuple[list[Token], str | None]:
    """Tokens del segmento con el tiempo de la palabra que los contiene. Si las palabras no
    reproducen el texto, todos los tokens llevan el tiempo del segmento (con aviso)."""
    limpio = _limpiar(s.texto)
    nfc = unicodedata.normalize("NFC", s.texto)
    palabras = list(s.palabras)
    aviso: str | None = None
    inicios: list[int] = []
    if palabras:
        acumulado = 0
        for p in palabras:
            inicios.append(acumulado)
            acumulado += len(_sin_espacios(unicodedata.normalize("NFC", p.texto)))
        if acumulado != len(_sin_espacios(nfc)):
            aviso = f"segmento {s.n}: las palabras no reproducen el texto; tiempos del segmento"
            palabras = []
    else:
        aviso = f"segmento {s.n}: sin palabras; tiempos del segmento"
    salida: list[Token] = []
    for m in _TOKEN.finditer(limpio):
        if palabras:
            offset = len(_sin_espacios(nfc[: m.start()]))
            k = max(bisect_right(inicios, offset) - 1, 0)
            t0, t1 = palabras[k].t0_ms, palabras[k].t1_ms
        else:
            t0, t1 = s.t0_ms, s.t1_ms
        salida.append(Token(m.group().casefold(), s.n, t0, t1, tuple(s.senales)))
    return salida, aviso


def trozos_de_cita(cita: str) -> list[list[str]]:
    """Trozos de tokens separados por el comodin `[...]`, con las reglas de forma."""
    if "[" in cita.replace(COMODIN, "") or "]" in cita.replace(COMODIN, ""):
        raise CitaError("la cita solo admite corchetes en el comodin [...]")
    partes = cita.split(COMODIN)
    if len(partes) - 1 > MAX_COMODINES:
        raise CitaError(f"la cita admite como maximo {MAX_COMODINES} comodines {COMODIN}")
    trozos = [tokens(p) for p in partes]
    if any(not t for t in trozos):
        raise CitaError("un trozo de la cita esta vacio (comodin al borde o duplicado)")
    total = sum(len(t) for t in trozos)
    if total < MIN_TOKENS_CITA:
        raise CitaError(f"la cita tiene {total} tokens; el minimo es {MIN_TOKENS_CITA}")
    if len(trozos) > 1 and any(len(t) < MIN_TOKENS_TROZO for t in trozos):
        raise CitaError(f"cada trozo entre comodines necesita {MIN_TOKENS_TROZO} tokens")
    return trozos


def _ventana(
    segmentos: Sequence[SegmentoCitable], t0_ms: int, t1_ms: int, tol_ms: int
) -> list[SegmentoCitable]:
    a, b = max(t0_ms - tol_ms, 0), t1_ms + tol_ms
    return [s for s in segmentos if s.t1_ms > a and s.t0_ms < b]


def _buscar(flujo: list[Token], trozo: list[str], desde: int) -> int | None:
    n = len(trozo)
    for i in range(desde, len(flujo) - n + 1):
        if all(flujo[i + k].texto == trozo[k] for k in range(n)):
            return i
    return None


def localizar_cita(
    segmentos: Sequence[SegmentoCitable],
    t0_ms: int,
    t1_ms: int,
    cita: str,
    tol_ms: int = TOLERANCIA_CITA_MS,
) -> Localizacion:
    """Localiza la cita (tokens, en orden, con comodines) dentro de la ventana y devuelve su
    tiempo real por palabras. Lanza `CitaError` si no se localiza o cae fuera de la ventana."""
    trozos = trozos_de_cita(cita)
    ventana = _ventana(segmentos, t0_ms, t1_ms, tol_ms)
    if not ventana:
        raise CitaError("ningun segmento de la cruda toca la ventana [t0, t1]")
    flujo: list[Token] = []
    avisos: list[str] = []
    for s in ventana:
        toks, aviso = tokens_de_segmento(s)
        flujo.extend(toks)
        if aviso:
            avisos.append(aviso)
    primero = trozos[0]
    inicios = [
        i
        for i in range(len(flujo) - len(primero) + 1)
        if all(flujo[i + k].texto == primero[k] for k in range(len(primero)))
    ]
    if not inicios:
        raise CitaError("la cita no se localiza en la cruda dentro de la ventana [t0, t1]")
    hallado: tuple[int, int] | None = None
    for inicio in inicios:
        fin = inicio + len(primero)
        ok = True
        for trozo in trozos[1:]:
            pos = _buscar(flujo, trozo, fin)
            if pos is None:
                ok = False
                break
            fin = pos + len(trozo)
        if ok:
            hallado = (inicio, fin)
            break
    if hallado is None:
        raise CitaError("los trozos de la cita no aparecen en ese orden dentro de la ventana")
    usados = flujo[hallado[0] : hallado[1]]
    inicio_ms = min(t.t0_ms for t in usados)
    fin_ms = max(t.t1_ms for t in usados)
    if inicio_ms < t0_ms - tol_ms or fin_ms > t1_ms + tol_ms:
        raise CitaError(
            f"la cita esta en {formato_ms(inicio_ms)}-{formato_ms(fin_ms)}: ajusta t0/t1"
        )
    senales = tuple(sorted({x for t in usados for x in t.senales}))
    return Localizacion(
        inicio_ms,
        fin_ms,
        tuple(sorted({t.segmento for t in usados})),
        len(inicios),
        len(trozos),
        senales,
        tuple(avisos),
    )


def formato_ms(ms: int) -> str:
    h, resto = divmod(ms, 3_600_000)
    m, resto = divmod(resto, 60_000)
    s, mil = divmod(resto, 1000)
    return f"{h}:{m:02d}:{s:02d}.{mil:03d}"


def video_de_referencia(referencia: str) -> str | None:
    """`fr-<video>-<hash8>/<t_ms>` -> `<video>`; None si no es una referencia de fotograma."""
    if not ids.es_id_de("referencia_fotograma", referencia):
        return None
    return referencia.split("-", 2)[1]


def t_ms_de_referencia(referencia: str) -> int:
    return int(referencia.rsplit("/", 1)[1])


def comprobar_referencias(
    video_id: str,
    t0_ms: int,
    t1_ms: int,
    modalidad: str,
    fotogramas: Sequence[str],
    referencias: set[str],
    tol_ms: int = TOLERANCIA_FOTOGRAMA_MS,
) -> list[str]:
    """Reglas de la cita de pantalla (brief F07, decision 4)."""
    problemas: list[str] = []
    if modalidad == "audio":
        if fotogramas:
            problemas.append("modalidad audio no admite fotogramas")
        return problemas
    de_video = [f for f in fotogramas if video_de_referencia(f) is not None]
    if not de_video:
        problemas.append(
            f"modalidad {modalidad} exige al menos una referencia fr-<id>/<t_ms> del video"
        )
    for f in fotogramas:
        if f not in referencias:
            problemas.append(f"referencia no conocida {f!r}")
            continue
        video = video_de_referencia(f)
        if video is None:
            continue  # material_adicional: acompanado por un fr-* (comprobado arriba)
        if video != video_id:
            problemas.append(f"referencia {f!r} es del video {video!r}, no de {video_id!r}")
        t = t_ms_de_referencia(f)
        if not (t0_ms - tol_ms <= t <= t1_ms + tol_ms):
            problemas.append(f"referencia {f!r} fuera del tramo [t0 - 1 s, t1 + 1 s]")
    return problemas


@dataclass(frozen=True, slots=True)
class ContextoEvidencia:
    """Lo que hace falta para verificar citas; lo compone `validation`/CLI, no `evidence`."""

    referencias: set[str] | None = None
    crudas: Callable[[str], Sequence[SegmentoCitable] | None] | None = None
    transcripciones: dict[str, str] = field(default_factory=dict)  # tid -> video_id
    activas: dict[str, str] = field(default_factory=dict)  # video_id -> tid
    reemplazadas: dict[str, str] = field(default_factory=dict)  # tid -> tid que la reemplaza
    dudas: Callable[[str], set[int]] | None = None  # tid -> segmentos con duda del glosario
    temas_raiz: frozenset[str] | None = None
    valores_cerrados: frozenset[str] = frozenset()
