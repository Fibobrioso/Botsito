"""Audio del corpus (F04, ADR-0007): un WAV por video, silencios y corte por MUESTRAS.

Hechos tecnicos del pipeline (no de negocio; se copian al manifiesto de cada transcripcion):
WAV PCM 16 bit, 16 kHz, mono, `-fflags +bitexact` (mismo video -> mismo WAV byte a byte);
silencio = tramo bajo `UMBRAL_SILENCIO_DB` durante al menos `SILENCIO_MINIMO_S`. Toda la
aritmetica de tiempos es en muestras enteras sobre ese unico WAV: los fragmentos se escriben con
`wave` (no con `ffmpeg -ss` sobre el MP4, que arrastra el priming del AAC), y el desfase
absoluto de un fragmento es `muestra_inicio * 1000 // 16000` milisegundos.

Corte: `cur = 0`; mientras queden mas de `MAX_S` segundos, se elige el centro del silencio mas
cercano a `cur + OBJETIVO_S` dentro de `[cur + MIN_S, cur + MAX_S]` (empate: el mas temprano);
sin silencio, corte forzado en `cur + OBJETIVO_S` y se cuenta. Sin solape: un corte en el centro
de un silencio no parte palabras; un corte forzado puede, y por eso el manifiesto lo reporta.
"""

from __future__ import annotations

import re
import subprocess
import wave
from dataclasses import dataclass
from pathlib import Path

MUESTRAS_S = 16000
CANALES = 1
OBJETIVO_S = 600.0
MIN_S = 420.0
MAX_S = 780.0
UMBRAL_SILENCIO_DB = -35.0
SILENCIO_MINIMO_S = 0.5  # no-negocio: duracion minima de un silencio para poder cortar
_SILENCIO_INICIO = re.compile(r"silence_start:\s*(-?\d+(?:\.\d+)?)")
_SILENCIO_FIN = re.compile(r"silence_end:\s*(-?\d+(?:\.\d+)?)")


class AudioError(RuntimeError):
    """ffmpeg fallo o el audio no cumple el formato esperado."""


@dataclass(frozen=True, slots=True)
class ParametrosCorte:
    objetivo_s: float = OBJETIVO_S
    min_s: float = MIN_S
    max_s: float = MAX_S
    umbral_db: float = UMBRAL_SILENCIO_DB
    silencio_minimo_s: float = SILENCIO_MINIMO_S

    def __post_init__(self) -> None:
        if not (0 < self.min_s <= self.objetivo_s <= self.max_s):
            raise AudioError("se exige 0 < min_s <= objetivo_s <= max_s")
        if self.silencio_minimo_s <= 0:
            raise AudioError("silencio_minimo_s debe ser positivo")

    def como_dict(self) -> dict[str, float]:
        return {
            "objetivo_s": self.objetivo_s,
            "min_s": self.min_s,
            "max_s": self.max_s,
            "umbral_db": self.umbral_db,
            "silencio_minimo_s": self.silencio_minimo_s,
            "muestras_s": MUESTRAS_S,
        }


@dataclass(frozen=True, slots=True)
class Silencio:
    inicio_m: int  # muestras
    fin_m: int

    @property
    def centro_m(self) -> int:
        return (self.inicio_m + self.fin_m) // 2


@dataclass(frozen=True, slots=True)
class Fragmento:
    indice: int
    inicio_m: int  # muestra absoluta del video
    fin_m: int
    ruta: Path

    @property
    def inicio_ms(self) -> int:
        return self.inicio_m * 1000 // MUESTRAS_S

    @property
    def fin_ms(self) -> int:
        return self.fin_m * 1000 // MUESTRAS_S


@dataclass(frozen=True, slots=True)
class Cortes:
    puntos_m: list[int]
    forzados_m: list[int]


def _ffmpeg(args: list[str]) -> str:
    resultado = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostdin", *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if resultado.returncode != 0:
        raise AudioError(f"ffmpeg fallo: {resultado.stderr.strip()[-400:]}")
    return resultado.stderr


def version_ffmpeg() -> str:
    salida = subprocess.run(
        ["ffmpeg", "-version"], capture_output=True, encoding="utf-8", errors="replace", check=False
    ).stdout
    m = re.search(r"ffmpeg version (\S+)", salida)
    return m.group(1) if m else "?"


def extraer_wav(video: Path, destino: Path) -> Path:
    """Pista de audio completa como WAV PCM 16 kHz mono, bit a bit reproducible (atomico)."""
    if not video.is_file():
        raise AudioError(f"no existe el video {video}")
    destino.parent.mkdir(parents=True, exist_ok=True)
    temporal = destino.with_name(destino.name + ".tmp")
    _ffmpeg(
        [
            "-v",
            "error",
            "-y",
            "-i",
            str(video),
            "-vn",
            "-ac",
            str(CANALES),
            "-ar",
            str(MUESTRAS_S),
            "-c:a",
            "pcm_s16le",
            "-fflags",
            "+bitexact",
            "-map_metadata",
            "-1",
            "-f",
            "wav",
            str(temporal),
        ]
    )
    temporal.replace(destino)
    return destino


def muestras_wav(ruta: Path) -> int:
    """Numero de muestras del WAV; un fichero ilegible o truncado es `AudioError`, no traceback."""
    try:
        with wave.open(str(ruta), "rb") as w:
            if (
                w.getframerate() != MUESTRAS_S
                or w.getnchannels() != CANALES
                or w.getsampwidth() != 2
            ):
                raise AudioError(f"{ruta.name}: se esperaba PCM 16 bit, {MUESTRAS_S} Hz, mono")
            return w.getnframes()
    except (wave.Error, EOFError, OSError) as exc:
        raise AudioError(f"{ruta.name}: WAV ilegible ({exc})") from exc


def duracion_wav_s(ruta: Path) -> float:
    return muestras_wav(ruta) / MUESTRAS_S


def detectar_silencios(wav: Path, umbral_db: float, minimo_s: float) -> list[Silencio]:
    """Silencios de `silencedetect` en muestras. Un `silence_start` sin fin (final del audio) se
    ignora: no sirve para cortar."""
    salida = _ffmpeg(
        [
            "-v",
            "info",
            "-i",
            str(wav),
            "-af",
            f"silencedetect=noise={umbral_db}dB:d={minimo_s}",
            "-f",
            "null",
            "-",
        ]
    )
    inicios = [float(x) for x in _SILENCIO_INICIO.findall(salida)]
    fines = [float(x) for x in _SILENCIO_FIN.findall(salida)]
    silencios = [
        Silencio(round(a * MUESTRAS_S), round(b * MUESTRAS_S))
        for a, b in zip(inicios, fines, strict=False)
        if b > a
    ]
    return sorted(silencios, key=lambda s: s.inicio_m)


def puntos_de_corte(n_muestras: int, silencios: list[Silencio], p: ParametrosCorte) -> Cortes:
    """Ver la regla en la cabecera. Invariantes: puntos estrictamente crecientes, el primero 0, el
    ultimo `n_muestras`, ningun fragmento mayor que `max_s`, todos menos el ultimo >= `min_s`."""
    if n_muestras <= 0:
        raise AudioError("audio vacio")
    obj, lo, hi = (round(x * MUESTRAS_S) for x in (p.objetivo_s, p.min_s, p.max_s))
    puntos, forzados = [0], []
    cur = 0
    while n_muestras - cur > hi:
        candidatos = [s.centro_m for s in silencios if cur + lo <= s.centro_m <= cur + hi]
        if candidatos:
            corte = min(candidatos, key=lambda m: (abs(m - (cur + obj)), m))
        else:
            corte = cur + obj
            forzados.append(corte)
        puntos.append(corte)
        cur = corte
    puntos.append(n_muestras)
    return Cortes(puntos, forzados)


def cortar_wav(wav: Path, puntos_m: list[int], carpeta: Path) -> list[Fragmento]:
    """Fragmentos contiguos por muestras exactas que cubren [0, n)."""
    carpeta.mkdir(parents=True, exist_ok=True)
    fragmentos: list[Fragmento] = []
    with wave.open(str(wav), "rb") as origen:
        parametros = origen.getparams()
        for i, (a, b) in enumerate(zip(puntos_m, puntos_m[1:], strict=False)):
            if b <= a:
                raise AudioError(f"fragmento {i} vacio ({a}-{b})")
            origen.setpos(a)
            datos = origen.readframes(b - a)
            ruta = carpeta / f"fragmento_{i:03d}.wav"
            temporal = ruta.with_name(ruta.name + ".tmp")
            with wave.open(str(temporal), "wb") as destino:
                destino.setparams(parametros)
                destino.writeframes(datos)
            temporal.replace(ruta)
            fragmentos.append(Fragmento(i, a, b, ruta))
    return fragmentos
