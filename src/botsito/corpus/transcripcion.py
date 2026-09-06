"""Segmentos con tiempos absolutos en milisegundos enteros y fusion de fragmentos (F04).

El motor devuelve segmentos RELATIVOS al fragmento (segundos, float); `fusionar` los convierte a
milisegundos absolutos con `t_ms = inicio_ms_del_fragmento + round(r * 1000)`, recorta lo que
cruce el final del fragmento, descarta lo que empiece despues, exige monotonia y `t1_ms <= fin
del WAV`. Cada segmento lleva las senales de calidad del ASR y un campo `senales` derivado
(`repeticion`, `baja_prob`, `compresion`, `no_habla`) para que F07 desconfie donde toca. La cruda
es JSONL, una linea por segmento con indice `n` (id estable), claves ordenadas, INMUTABLE.
"""

from __future__ import annotations

import json
import re
import unicodedata
from collections.abc import Callable, Iterable
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Protocol

from botsito.comun.documentos import sha256_hex
from botsito.corpus.audio import Fragmento

HUECO_TRANSCRIPCION_S = 30.0  # tramos sin segmento >= esto se listan (silencio o alucinacion)
# Umbrales de Whisper para marcar segmentos sospechosos (hechos tecnicos del motor).
COMPRESION_MAX = 2.4
LOGPROB_MIN = -1.0
NO_HABLA_MAX = 0.6
# Whisper devuelve a veces segmentos consecutivos que se pisan unos milisegundos: se recorta el
# segundo y se cuenta. Un solape mayor es un motor que va hacia atras y se rechaza.
SOLAPE_MAX_MS = 500
SENALES = ("repeticion", "baja_prob", "compresion", "no_habla")


class TranscripcionError(ValueError):
    """Un segmento o una transcripcion no cumple sus invariantes."""


@dataclass(frozen=True, slots=True)
class Palabra:
    t0_ms: int
    t1_ms: int
    texto: str
    probabilidad: float


@dataclass(frozen=True, slots=True)
class SegmentoRelativo:
    """Lo que devuelve el motor: segundos desde el inicio del fragmento."""

    t0_s: float
    t1_s: float
    texto: str
    palabras: tuple[tuple[float, float, str, float], ...] = ()
    no_speech_prob: float = 0.0
    compression_ratio: float = 0.0
    avg_logprob: float = 0.0


@dataclass(frozen=True, slots=True)
class Segmento:
    n: int
    t0_ms: int
    t1_ms: int
    texto: str
    palabras: tuple[Palabra, ...] = ()
    no_speech_prob: float = 0.0
    compression_ratio: float = 0.0
    avg_logprob: float = 0.0
    senales: tuple[str, ...] = field(default=())

    def __post_init__(self) -> None:
        for v in (self.n, self.t0_ms, self.t1_ms):
            if isinstance(v, bool) or not isinstance(v, int):
                raise TranscripcionError("n, t0_ms y t1_ms deben ser enteros")
        if not (self.n >= 0 and self.t0_ms >= 0 and self.t1_ms > self.t0_ms):
            raise TranscripcionError(
                f"segmento {self.n} con tiempos invalidos {self.t0_ms}-{self.t1_ms}"
            )
        if not self.texto.strip():
            raise TranscripcionError(f"segmento {self.n} vacio")
        for p in self.palabras:
            dentro = self.t0_ms <= p.t0_ms <= p.t1_ms <= self.t1_ms
            if not dentro or not 0 <= p.probabilidad <= 1:
                raise TranscripcionError(f"segmento {self.n}: palabra {p.texto!r} fuera de rango")
        if any(s not in SENALES for s in self.senales):
            raise TranscripcionError(f"segmento {self.n}: senal desconocida {self.senales}")


class MotorAsr(Protocol):
    @property
    def nombre(self) -> str: ...

    def describir(self) -> dict[str, Any]: ...

    def transcribir(self, wav: Path) -> list[SegmentoRelativo]: ...


class MotorFalso:
    """Segmentos deterministas por fragmento: uno por cada 5 s de audio, o lo que diga
    `generar`. Sirve para tests y para la CLI sin modelo."""

    def __init__(self, generar: Callable[[Path], list[SegmentoRelativo]] | None = None) -> None:
        self._generar = generar

    @property
    def nombre(self) -> str:
        return "falso"

    def describir(self) -> dict[str, Any]:
        return {"motor": "falso", "modelo": "falso"}

    def transcribir(self, wav: Path) -> list[SegmentoRelativo]:
        if self._generar is not None:
            return self._generar(wav)
        from botsito.corpus.audio import duracion_wav_s

        d = duracion_wav_s(wav)
        salida: list[SegmentoRelativo] = []
        t = 0.0
        while t < d:
            fin = min(t + 5.0, d)
            salida.append(
                SegmentoRelativo(t, fin, f"texto falso {int(t)}-{int(fin)} de {wav.name}")
            )
            t = fin
        return salida


def normalizar_para_comparar(texto: str) -> str:
    return " ".join(unicodedata.normalize("NFC", texto).casefold().split())


def _senales(s: SegmentoRelativo, anterior_texto: str | None) -> tuple[str, ...]:
    out: list[str] = []
    if anterior_texto is not None and normalizar_para_comparar(s.texto) == anterior_texto:
        out.append("repeticion")
    if s.avg_logprob < LOGPROB_MIN:
        out.append("baja_prob")
    if s.compression_ratio > COMPRESION_MAX:
        out.append("compresion")
    if s.no_speech_prob > NO_HABLA_MAX:
        out.append("no_habla")
    return tuple(out)


@dataclass(frozen=True, slots=True)
class Fusion:
    segmentos: list[Segmento]
    recortados: int
    descartados: int


def fusionar(
    por_fragmento: Iterable[tuple[Fragmento, list[SegmentoRelativo]]], fin_wav_ms: int
) -> Fusion:
    salida: list[Segmento] = []
    recortados = descartados = 0
    anterior: str | None = None
    for fragmento, relativos in por_fragmento:
        base = fragmento.inicio_ms
        for r in sorted(relativos, key=lambda x: x.t0_s):
            t0 = base + round(r.t0_s * 1000)
            t1 = base + round(r.t1_s * 1000)
            if t0 >= fragmento.fin_ms:
                descartados += 1
                continue
            if t1 > fragmento.fin_ms:
                # 1 ms de mas es redondeo (fin del fragmento por floor, motor por round), no
                # un recorte real.
                if t1 - fragmento.fin_ms > 1:
                    recortados += 1
                t1 = fragmento.fin_ms
            if t1 <= t0:
                descartados += 1
                continue
            if t1 > fin_wav_ms:
                raise TranscripcionError(f"segmento {t0}-{t1} supera el fin del audio {fin_wav_ms}")
            if salida and t0 < salida[-1].t1_ms:
                if salida[-1].t1_ms - t0 > SOLAPE_MAX_MS:
                    raise TranscripcionError(
                        f"segmentos solapados: {salida[-1].t1_ms} > {t0} "
                        f"(fragmento {fragmento.indice})"
                    )
                t0 = salida[-1].t1_ms
                recortados += 1
                if t1 <= t0:
                    descartados += 1
                    continue
            candidatas = [_palabra(base, a, b, w, prob, t0, t1) for a, b, w, prob in r.palabras]
            palabras = tuple(p for p in candidatas if p is not None)
            texto = " ".join(unicodedata.normalize("NFC", r.texto).split())
            if not texto:
                descartados += 1
                continue
            salida.append(
                Segmento(
                    len(salida),
                    t0,
                    t1,
                    texto,
                    palabras,
                    r.no_speech_prob,
                    r.compression_ratio,
                    r.avg_logprob,
                    _senales(r, anterior),
                )
            )
            anterior = normalizar_para_comparar(texto)
    return Fusion(salida, recortados, descartados)


def _palabra(
    base: int, a: float, b: float, w: str, prob: float, t0: int, t1: int
) -> Palabra | None:
    """Palabra recortada al segmento; `fin < inicio` (lo devuelve el motor a veces) se iguala."""
    if not w.strip() or base + round(a * 1000) >= t1:
        return None
    pa = min(max(base + round(a * 1000), t0), t1)
    pb = min(max(base + round(b * 1000), pa), t1)
    return Palabra(pa, pb, " ".join(w.split()), min(max(prob, 0.0), 1.0))


def huecos(
    segmentos: list[Segmento], fin_ms: int, minimo_s: float = HUECO_TRANSCRIPCION_S
) -> list[dict[str, int]]:
    """Tramos sin segmento >= `minimo_s`, incluidos el inicial y el final."""
    puntos = [0] + [t for s in segmentos for t in (s.t0_ms, s.t1_ms)] + [fin_ms]
    minimo_ms = round(minimo_s * 1000)
    return [
        {"desde_ms": a, "hasta_ms": b, "ms": b - a}
        for a, b in zip(puntos[0::2], puntos[1::2], strict=False)
        if b - a >= minimo_ms
    ]


def a_jsonl(segmentos: list[Segmento]) -> str:
    lineas = []
    for s in segmentos:
        d: dict[str, Any] = asdict(s)
        d["palabras"] = [asdict(p) for p in s.palabras]
        d["senales"] = list(s.senales)
        lineas.append(json.dumps(d, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return "\n".join(lineas) + ("\n" if lineas else "")


def desde_jsonl(texto: str) -> list[Segmento]:
    salida: list[Segmento] = []
    for num, linea in enumerate(texto.splitlines(), start=1):
        if not linea.strip():
            raise TranscripcionError(f"linea {num} vacia")
        try:
            d = json.loads(linea)
            palabras = tuple(
                Palabra(int(p["t0_ms"]), int(p["t1_ms"]), str(p["texto"]), float(p["probabilidad"]))
                for p in d.get("palabras", [])
            )
            s = Segmento(
                int(d["n"]),
                int(d["t0_ms"]),
                int(d["t1_ms"]),
                str(d["texto"]),
                palabras,
                float(d.get("no_speech_prob", 0.0)),
                float(d.get("compression_ratio", 0.0)),
                float(d.get("avg_logprob", 0.0)),
                tuple(str(x) for x in d.get("senales", [])),
            )
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            raise TranscripcionError(f"linea {num}: {exc}") from exc
        if s.n != num - 1:
            raise TranscripcionError(f"linea {num}: indice n={s.n} fuera de orden")
        if salida and s.t0_ms < salida[-1].t1_ms:
            raise TranscripcionError(f"linea {num}: segmentos desordenados o solapados")
        salida.append(s)
    return salida


def escribir_atomico(ruta: Path, texto: str) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    # Prefijo `_`: un temporal huerfano en knowledge/corpus/transcripciones/ queda exento del
    # listado de manifiestos (documentos.ficheros_de) en vez de invalidar el repo.
    temporal = ruta.with_name("_" + ruta.name + ".tmp")
    temporal.write_text(texto, encoding="utf-8", newline="\n")
    temporal.replace(ruta)


def transcribir_fragmentos(
    fragmentos: list[Fragmento],
    motor: MotorAsr,
    carpeta: Path,
    huella_parametros: str,
    progreso: Callable[[Fragmento, int], None] | None = None,
) -> list[tuple[Fragmento, list[SegmentoRelativo]]]:
    """Cada fragmento se guarda en `parciales/fragmento_NNN.json` con el sha256 de su WAV y la
    huella de los parametros: se reutiliza solo si ambos coinciden (reanudacion segura)."""
    salida: list[tuple[Fragmento, list[SegmentoRelativo]]] = []
    carpeta.mkdir(parents=True, exist_ok=True)
    for f in fragmentos:
        parcial = carpeta / f"fragmento_{f.indice:03d}.json"
        huella_wav = sha256_hex(f.ruta.read_bytes())
        relativos = _leer_parcial(parcial, huella_wav, huella_parametros)
        if relativos is None:
            relativos = motor.transcribir(f.ruta)
            escribir_atomico(
                parcial,
                json.dumps(
                    {
                        "indice": f.indice,
                        "sha256_wav": huella_wav,
                        "huella_parametros": huella_parametros,
                        "segmentos": [asdict(r) for r in relativos],
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                ),
            )
        if progreso:
            progreso(f, len(relativos))
        salida.append((f, relativos))
    return salida


def _leer_parcial(
    parcial: Path, huella_wav: str, huella_parametros: str
) -> list[SegmentoRelativo] | None:
    """None si no existe, es de otro WAV, de otros parametros o esta corrupto: se retranscribe
    (un parcial es cache, no verdad)."""
    if not parcial.exists():
        return None
    try:
        d = json.loads(parcial.read_text(encoding="utf-8"))
        if d.get("sha256_wav") != huella_wav or d.get("huella_parametros") != huella_parametros:
            return None
        return [
            SegmentoRelativo(
                float(x["t0_s"]),
                float(x["t1_s"]),
                str(x["texto"]),
                tuple((float(q[0]), float(q[1]), str(q[2]), float(q[3])) for q in x["palabras"]),
                float(x["no_speech_prob"]),
                float(x["compression_ratio"]),
                float(x["avg_logprob"]),
            )
            for x in d["segmentos"]
        ]
    except (OSError, ValueError, KeyError, TypeError, AttributeError, IndexError):
        return None


def formato_ms(ms: int) -> str:
    s, mil = divmod(ms, 1000)
    h, resto = divmod(s, 3600)
    m, seg = divmod(resto, 60)
    return f"{h}:{m:02d}:{seg:02d}.{mil:03d}"


_TIEMPO = re.compile(r"(\d+):([0-5]\d):([0-5]\d)(?:\.(\d{1,3}))?", re.ASCII)


def parse_ms(texto: str) -> int:
    """`h:mm:ss[.mmm]` -> milisegundos (mismo formato estricto que la evidencia, F06): sin
    signo, sin espacios ni separadores raros, como mucho tres decimales."""
    m = _TIEMPO.fullmatch(texto.strip())
    if m is None:
        raise TranscripcionError(f"tiempo invalido {texto!r} (h:mm:ss[.mmm])")
    h, mi, seg = int(m.group(1)), int(m.group(2)), int(m.group(3))
    mil = int((m.group(4) + "000")[:3]) if m.group(4) else 0
    return ((h * 60 + mi) * 60 + seg) * 1000 + mil


def texto_entre(
    segmentos: list[Segmento], t0_ms: int, t1_ms: int, margen_ms: int = 0
) -> list[Segmento]:
    """Segmentos que tocan [t0 - margen, t1 + margen]: lo que F07 cita literalmente."""
    a, b = max(t0_ms - margen_ms, 0), t1_ms + margen_ms
    if a == b:  # cita de un instante: tambien el segmento que empieza o acaba justo ahi
        return [s for s in segmentos if s.t0_ms <= a <= s.t1_ms]
    return [s for s in segmentos if s.t1_ms > a and s.t0_ms < b]


def a_texto_legible(segmentos: list[Segmento]) -> str:
    return "".join(
        f"[{formato_ms(s.t0_ms)}] {s.texto}"
        + (f"   <{','.join(s.senales)}>" if s.senales else "")
        + "\n"
        for s in segmentos
    )
