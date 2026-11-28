"""Adaptador de faster-whisper (grupo de dependencias opcional `asr`; F04, ADR-0007).

Unico modulo que importa `faster_whisper`/`ctranslate2` (contrato de importacion). En Windows,
cuBLAS y cuDNN llegan como paquetes de pip y hay que anadir sus `bin/` al buscador de DLL antes
de cargar el modelo. Parametros fijos y anotados en el manifiesto: `temperature=0` (sin cascada),
`beam_size=5`, `condition_on_previous_text=False` (evita bucles de repeticion entre fragmentos),
`vad_filter=True` con parametros por defecto (faster-whisper devuelve los tiempos en el eje del
fragmento; desde el 2026-11-27 el VAD se configura por transcripcion, `ConfiguracionVad`, ADR-0007
enmienda de esa fecha), `initial_prompt` = vocabulario del glosario. Medido el 2026-09-06 (ADR-0007,
enmienda): con `condition_on_previous_text=False` el `initial_prompt` solo condiciona la PRIMERA
ventana de cada fragmento; `hotwords` condicionaria todas, pero sobre v5 alargo los segmentos
hasta 40 s (mas que la ventana de 30 s), perdio ~10 s de habla con un hecho clave y sesgo
"sell" -> "SL": descartado por fidelidad. faster-whisper trunca el prompt a 223 tokens sin
avisar, de ahi la guardia `LIMITE_PROMPT_TOKENS`. Determinismo prometido: misma maquina y
mismas versiones -> misma cruda; el informe lo verifica una vez.
"""

from __future__ import annotations

import importlib
import importlib.metadata
import importlib.util
import os
import platform
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from botsito.comun.documentos import sha256_hex
from botsito.corpus.transcripcion import MotorAsr, SegmentoRelativo, TranscripcionError

IDIOMA = "es"
BEAM = 5
TEMPERATURA = 0.0
# faster-whisper recorta el prompt a `max_length // 2 - 1` tokens (448 // 2 - 1) sin avisar:
# un vocabulario mas largo entraria a medias y el manifiesto mentiria sobre lo que vio el motor.
LIMITE_PROMPT_TOKENS = 223


def _anadir_dlls_cuda() -> list[str]:
    anadidos: list[str] = []
    for paquete in ("nvidia.cublas", "nvidia.cudnn"):
        spec = importlib.util.find_spec(paquete)
        if spec is None or not spec.submodule_search_locations:
            continue
        for base in spec.submodule_search_locations:
            carpeta = Path(base) / "bin"
            if carpeta.is_dir() and hasattr(os, "add_dll_directory"):
                os.add_dll_directory(str(carpeta))
                os.environ["PATH"] = str(carpeta) + os.pathsep + os.environ.get("PATH", "")
                anadidos.append(str(carpeta))
    return anadidos


def _version(paquete: str) -> str:
    try:
        return importlib.metadata.version(paquete)
    except importlib.metadata.PackageNotFoundError:
        return "?"


def _gpu() -> str:
    try:
        r = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,driver_version", "--format=csv,noheader"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=20,
        )
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip().splitlines()[0]
    except (OSError, subprocess.TimeoutExpired):
        pass
    return "?"


def comprobar_prompt(tokenizador: Any, prompt: str) -> int:
    """Tokens que ocupa el vocabulario tal como lo codifica faster-whisper (`" " + texto`,
    `add_special_tokens=False`: sin <|startoftranscript|> ni <|notimestamps|>). Error de
    dominio si el motor lo truncaria."""
    if not prompt:
        return 0
    n = len(tokenizador.encode(" " + prompt.strip(), add_special_tokens=False).ids)
    if n > LIMITE_PROMPT_TOKENS:
        raise TranscripcionError(
            f"el vocabulario del glosario ocupa {n} tokens y faster-whisper trunca el prompt a "
            f"{LIMITE_PROMPT_TOKENS}: acorta el vocabulario antes de transcribir"
        )
    return n


# Los parametros del VAD de Silero de faster-whisper 1.2.1 (`faster_whisper/vad.py`, `VadOptions`),
# por su nombre, LEIDOS en el paquete instalado (trabajo/vad-julio, fase 0.3). Sus valores por
# defecto NO se copian aqui: un parametro que no se da no se anota y lo pone el paquete
# (`vad_parameters=None` -> `VadOptions()`), y uno que se da se anota siempre, aunque valga lo mismo
# que el de defecto (los valores leidos, en docs/validation/VAD-JULIO.md, 0.3).
# `tests/unit/test_transcripcion_vad.py` compara esta lista con los campos de `VadOptions` donde el
# paquete esta (la CI no instala el grupo `asr`).
VAD_PARAMETROS = (
    "threshold",
    "neg_threshold",
    "min_speech_duration_ms",
    "max_speech_duration_s",
    "min_silence_duration_ms",
    "speech_pad_ms",
)
_VAD_ENTEROS = ("min_speech_duration_ms", "min_silence_duration_ms", "speech_pad_ms")


@dataclass(frozen=True, slots=True)
class ConfiguracionVad:
    """El VAD de una transcripcion (ADR-0007, enmienda 2026-11-27). `parametros` lleva SOLO los
    que se dan, ordenados por nombre: sin ninguno, la descripcion del motor y la huella son
    exactamente las de antes de poder configurarlo. Se construye con `desde`, que valida."""

    activo: bool = True
    parametros: tuple[tuple[str, float | int], ...] = ()

    @classmethod
    def desde(cls, activo: bool = True, **valores: float | int | None) -> ConfiguracionVad:
        """Valida y ordena; un `None` es un parametro que no se da."""
        desconocidos = sorted(set(valores) - set(VAD_PARAMETROS))
        if desconocidos:
            raise TranscripcionError(
                f"parametro de VAD desconocido: {', '.join(desconocidos)} (los de faster-whisper "
                f"son {', '.join(VAD_PARAMETROS)})"
            )
        dados = {k: v for k, v in valores.items() if v is not None}
        if not activo:
            if dados:
                raise TranscripcionError(
                    "sin VAD no hay parametros de VAD: quita --sin-vad o las opciones --vad-*"
                )
            return cls(activo=False)
        for k in _VAD_ENTEROS:
            if k in dados:
                v = dados[k]
                if isinstance(v, bool) or not isinstance(v, int) or v < 0:
                    raise TranscripcionError(f"{k} debe ser un entero >= 0 (ms); se dio {v!r}")
        for k in ("threshold", "neg_threshold"):
            if k in dados and not 0.0 < float(dados[k]) < 1.0:
                raise TranscripcionError(
                    f"{k} debe estar entre 0 y 1 (sin incluirlos); se dio {dados[k]!r}"
                )
        if (
            "threshold" in dados
            and "neg_threshold" in dados
            and not float(dados["neg_threshold"]) < float(dados["threshold"])
        ):
            raise TranscripcionError(
                f"neg_threshold ({dados['neg_threshold']!r}) debe ser menor que threshold "
                f"({dados['threshold']!r})"
            )
        if "max_speech_duration_s" in dados and not float(dados["max_speech_duration_s"]) > 0:
            raise TranscripcionError(
                f"max_speech_duration_s debe ser > 0 (s); se dio {dados['max_speech_duration_s']!r}"
            )
        return cls(activo=True, parametros=tuple(sorted(dados.items())))

    @property
    def por_defecto(self) -> bool:
        return self.activo and not self.parametros


def describir_vad(vad: ConfiguracionVad) -> dict[str, Any]:
    """La parte del VAD de la descripcion del motor (y de la huella), pura: no carga el modelo.
    Por defecto, `{"vad_filter": True}`, lo de siempre."""
    if not vad.activo:
        return {"vad_filter": False}
    salida: dict[str, Any] = {"vad_filter": True}
    if vad.parametros:
        salida["vad_parameters"] = dict(vad.parametros)
    return salida


def argumentos_vad(vad: ConfiguracionVad) -> dict[str, Any]:
    """Los argumentos de `WhisperModel.transcribe`; por defecto, `vad_parameters=None`, que el
    paquete convierte en `VadOptions()` (`transcribe.py`)."""
    return {
        "vad_filter": vad.activo,
        "vad_parameters": dict(vad.parametros) if vad.parametros else None,
    }


@dataclass(frozen=True, slots=True)
class ConfiguracionWhisper:
    modelo: str = "large-v3"
    dispositivo: str = "cuda"
    compute_type: str = "int8_float16"
    prompt_inicial: str = ""
    # Al final y con valor por defecto: `scripts/transcribir_sesion.py` construye esta clase por
    # posicion con los cuatro campos de arriba.
    vad: ConfiguracionVad = field(default_factory=ConfiguracionVad)

    @property
    def nombre(self) -> str:
        """Nombre de la transcripcion: modelo + compute (ejecuciones distintas no colisionan)."""
        return f"{self.modelo}-{self.compute_type}".replace("_", "-")


class MotorWhisper(MotorAsr):
    def __init__(self, configuracion: ConfiguracionWhisper | None = None) -> None:
        self.configuracion = configuracion or ConfiguracionWhisper()
        self._modelo: Any = None
        self._ruta_modelo: Path | None = None
        self._prompt_tokens: int | None = None

    def _comprobar_prompt(self, ruta_modelo: Path) -> int:
        """Antes de cargar los pesos en la GPU: el tokenizador del modelo basta."""
        tokenizers = importlib.import_module("tokenizers")
        tokenizador = tokenizers.Tokenizer.from_file(str(ruta_modelo / "tokenizer.json"))
        return comprobar_prompt(tokenizador, self.configuracion.prompt_inicial)

    @property
    def nombre(self) -> str:
        return self.configuracion.nombre

    def _cargar(self) -> Any:
        if self._modelo is None:
            _anadir_dlls_cuda()
            fw = importlib.import_module("faster_whisper")
            utils = importlib.import_module("faster_whisper.utils")
            self._ruta_modelo = Path(utils.download_model(self.configuracion.modelo))
            self._prompt_tokens = self._comprobar_prompt(self._ruta_modelo)
            self._modelo = fw.WhisperModel(
                str(self._ruta_modelo),
                device=self.configuracion.dispositivo,
                compute_type=self.configuracion.compute_type,
            )
        return self._modelo

    def describir(self) -> dict[str, Any]:
        self._cargar()
        assert self._ruta_modelo is not None
        pesos = self._ruta_modelo / "model.bin"
        return {
            "motor": "faster-whisper",
            "modelo": self.configuracion.modelo,
            "modelo_ruta": str(self._ruta_modelo),
            "modelo_sha256": sha256_hex(pesos.read_bytes()) if pesos.is_file() else "?",
            "dispositivo": self.configuracion.dispositivo,
            "compute_type": self.configuracion.compute_type,
            "faster_whisper": _version("faster-whisper"),
            "ctranslate2": _version("ctranslate2"),
            "nvidia_cublas_cu12": _version("nvidia-cublas-cu12"),
            "nvidia_cudnn_cu12": _version("nvidia-cudnn-cu12"),
            "gpu": _gpu(),
            "python": platform.python_version(),
            "idioma": IDIOMA,
            "beam_size": BEAM,
            "temperature": TEMPERATURA,
            "word_timestamps": True,
            **describir_vad(self.configuracion.vad),
            "condition_on_previous_text": False,
            "initial_prompt_sha256": sha256_hex(self.configuracion.prompt_inicial.encode("utf-8")),
            "initial_prompt_tokens": self._prompt_tokens,
            "hotwords": None,
        }

    def transcribir(self, wav: Path) -> list[SegmentoRelativo]:
        modelo = self._cargar()
        segmentos, _info = modelo.transcribe(
            str(wav),
            language=IDIOMA,
            beam_size=BEAM,
            temperature=TEMPERATURA,
            word_timestamps=True,
            **argumentos_vad(self.configuracion.vad),
            condition_on_previous_text=False,
            initial_prompt=self.configuracion.prompt_inicial or None,
        )
        salida: list[SegmentoRelativo] = []
        for s in segmentos:
            palabras = tuple(
                (float(w.start), float(w.end), str(w.word), float(w.probability))
                for w in (s.words or [])
            )
            salida.append(
                SegmentoRelativo(
                    float(s.start),
                    float(s.end),
                    str(s.text),
                    palabras,
                    float(s.no_speech_prob),
                    float(s.compression_ratio),
                    float(s.avg_logprob),
                )
            )
        return salida
