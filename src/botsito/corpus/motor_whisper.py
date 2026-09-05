"""Adaptador de faster-whisper (grupo de dependencias opcional `asr`; F04, ADR-0007).

Unico modulo que importa `faster_whisper`/`ctranslate2` (contrato de importacion). En Windows,
cuBLAS y cuDNN llegan como paquetes de pip y hay que anadir sus `bin/` al buscador de DLL antes
de cargar el modelo. Parametros fijos y anotados en el manifiesto: `temperature=0` (sin cascada),
`beam_size=5`, `condition_on_previous_text=False` (evita bucles de repeticion entre fragmentos),
`vad_filter=True` con parametros por defecto (faster-whisper devuelve los tiempos en el eje del
fragmento), `initial_prompt` = vocabulario del glosario. Determinismo prometido: misma maquina y
mismas versiones -> misma cruda; el informe lo verifica una vez.
"""

from __future__ import annotations

import importlib
import importlib.metadata
import importlib.util
import os
import platform
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from botsito.comun.documentos import sha256_hex
from botsito.corpus.transcripcion import MotorAsr, SegmentoRelativo

IDIOMA = "es"
BEAM = 5
TEMPERATURA = 0.0


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


@dataclass(frozen=True, slots=True)
class ConfiguracionWhisper:
    modelo: str = "large-v3"
    dispositivo: str = "cuda"
    compute_type: str = "int8_float16"
    prompt_inicial: str = ""

    @property
    def nombre(self) -> str:
        """Nombre de la transcripcion: modelo + compute (ejecuciones distintas no colisionan)."""
        return f"{self.modelo}-{self.compute_type}".replace("_", "-")


class MotorWhisper(MotorAsr):
    def __init__(self, configuracion: ConfiguracionWhisper | None = None) -> None:
        self.configuracion = configuracion or ConfiguracionWhisper()
        self._modelo: Any = None
        self._ruta_modelo: Path | None = None

    @property
    def nombre(self) -> str:
        return self.configuracion.nombre

    def _cargar(self) -> Any:
        if self._modelo is None:
            _anadir_dlls_cuda()
            fw = importlib.import_module("faster_whisper")
            utils = importlib.import_module("faster_whisper.utils")
            self._ruta_modelo = Path(utils.download_model(self.configuracion.modelo))
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
            "vad_filter": True,
            "condition_on_previous_text": False,
            "initial_prompt_sha256": sha256_hex(self.configuracion.prompt_inicial.encode("utf-8")),
        }

    def transcribir(self, wav: Path) -> list[SegmentoRelativo]:
        modelo = self._cargar()
        segmentos, _info = modelo.transcribe(
            str(wav),
            language=IDIOMA,
            beam_size=BEAM,
            temperature=TEMPERATURA,
            word_timestamps=True,
            vad_filter=True,
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
