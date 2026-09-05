"""Orquestacion de la transcripcion de un video (F04, ADR-0007), reanudable y determinista.

Disposicion bajo la carpeta de datos (`[rutas].data`, ignorada por git):

    data/transcripciones/<video_id>/audio.wav                       (un WAV por video)
    data/transcripciones/<video_id>/<nombre>/fragmentos/*.wav         (corte por muestras)
    data/transcripciones/<video_id>/<nombre>/parciales/*.json         (estado de reanudacion)
    data/transcripciones/<video_id>/<nombre>/cruda.jsonl              (INMUTABLE, hash)
    data/transcripciones/<video_id>/<nombre>/{corregida,correcciones}.jsonl, cruda.txt

y el manifiesto INMUTABLE, versionado, en `knowledge/corpus/transcripciones/<transcripcion_id>.yaml`
con `transcripcion_id = tr-<video_id>-<nombre>-<hash8 del sha256 de cruda.jsonl>`. `<nombre>` es
el del motor (modelo + compute) y `reemplaza_a` enlaza retranscripciones.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from botsito.comun.documentos import hash_corto, sha256_hex
from botsito.corpus.audio import (
    MUESTRAS_S,
    AudioError,
    ParametrosCorte,
    cortar_wav,
    detectar_silencios,
    extraer_wav,
    muestras_wav,
    puntos_de_corte,
    version_ffmpeg,
)
from botsito.corpus.glosario import Glosario, aplicar, correcciones_jsonl
from botsito.corpus.transcripcion import (
    HUECO_TRANSCRIPCION_S,
    MotorAsr,
    Segmento,
    TranscripcionError,
    a_jsonl,
    a_texto_legible,
    desde_jsonl,
    escribir_atomico,
    fusionar,
    huecos,
    transcribir_fragmentos,
)

CARPETA_DATOS = "transcripciones"
DIRECTORIO_MANIFIESTOS = "knowledge/corpus/transcripciones"
FICHERO_CRUDA = "cruda.jsonl"
FICHERO_CORREGIDA = "corregida.jsonl"
FICHERO_CORRECCIONES = "correcciones.jsonl"
FICHERO_LEGIBLE = "cruda.txt"
SCHEMA_VERSION = 1
TOLERANCIA_DURACION_S = 1.0  # WAV frente a la duracion del manifiesto del corpus (como F06)


@dataclass(frozen=True, slots=True)
class Resultado:
    transcripcion_id: str
    carpeta: Path
    cruda: Path
    manifiesto: Path
    segmentos: list[Segmento]


def carpeta_video(carpeta_datos: Path, video_id: str) -> Path:
    return carpeta_datos / CARPETA_DATOS / video_id


def id_transcripcion(video_id: str, nombre: str, sha256_cruda: str) -> str:
    return f"tr-{video_id}-{nombre}-{sha256_cruda[:8]}"


def transcribir_video(
    repo: Path,
    carpeta_datos: Path,
    raiz_corpus: Path,
    video_id: str,
    fichero_video: str,
    sha256_video: str,
    duracion_video_s: float,
    motor: MotorAsr,
    glosario: Glosario,
    parametros: ParametrosCorte | None = None,
    progreso: Any = None,
    comprobar_hash_video: bool = True,
    reemplaza_a: str | None = None,
) -> Resultado:
    parametros = parametros or ParametrosCorte()
    video = raiz_corpus / fichero_video
    if not video.is_file():
        raise AudioError(f"no existe el video {video}")
    if comprobar_hash_video and sha256_hex(video.read_bytes()) != sha256_video:
        raise AudioError(f"{fichero_video}: el sha256 no coincide con el manifiesto del corpus")
    cv = carpeta_video(carpeta_datos, video_id)
    carpeta = cv / motor.nombre
    carpeta.mkdir(parents=True, exist_ok=True)
    wav = cv / "audio.wav"
    if not wav.exists():
        extraer_wav(video, wav)
    n_muestras = muestras_wav(wav)
    duracion_wav_s = n_muestras / MUESTRAS_S
    if abs(duracion_wav_s - duracion_video_s) > TOLERANCIA_DURACION_S:
        raise AudioError(
            f"{video_id}: el WAV dura {duracion_wav_s:.3f} s y el manifiesto dice "
            f"{duracion_video_s:.3f} s"
        )
    fin_ms = n_muestras * 1000 // MUESTRAS_S
    descripcion_motor = motor.describir()
    huella = hash_corto(
        json.dumps({"corte": parametros.como_dict(), "motor": descripcion_motor}, sort_keys=True)
    )
    silencios = detectar_silencios(wav, parametros.umbral_db, parametros.silencio_minimo_s)
    cortes = puntos_de_corte(n_muestras, silencios, parametros)
    fragmentos = cortar_wav(wav, cortes.puntos_m, carpeta / "fragmentos")
    por_fragmento = transcribir_fragmentos(
        fragmentos, motor, carpeta / "parciales", huella, progreso
    )
    fusion = fusionar(por_fragmento, fin_ms)
    if not fusion.segmentos:
        raise TranscripcionError(f"{video_id}: la transcripcion no produjo ningun segmento")
    texto_cruda = a_jsonl(fusion.segmentos)
    sha_cruda = sha256_hex(texto_cruda.encode("utf-8"))
    tid = id_transcripcion(video_id, motor.nombre, sha_cruda)
    cruda = carpeta / FICHERO_CRUDA
    if cruda.exists() and sha256_hex(cruda.read_bytes()) != sha_cruda:
        raise TranscripcionError(
            f"{cruda} ya existe con otro contenido: una cruda es inmutable (borra la carpeta "
            "para retranscribir o usa otro nombre de motor)"
        )
    escribir_atomico(cruda, texto_cruda)
    escribir_atomico(carpeta / FICHERO_LEGIBLE, a_texto_legible(fusion.segmentos))
    corregir(carpeta, fusion.segmentos, glosario, tid)
    manifiesto: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "transcripcion_id": tid,
        "video_id": video_id,
        "fichero_video": fichero_video,
        "sha256_video": sha256_video,
        "sha256_wav": sha256_hex(wav.read_bytes()),
        "duracion_video_s": round(duracion_video_s, 3),
        "duracion_wav_s": round(duracion_wav_s, 3),
        "muestras": n_muestras,
        "carpeta": f"{CARPETA_DATOS}/{video_id}/{motor.nombre}",
        "motor": descripcion_motor,
        "ffmpeg": version_ffmpeg(),
        "corte": parametros.como_dict(),
        "silencios_detectados": len(silencios),
        "fragmentos": [
            {"indice": f.indice, "inicio_m": f.inicio_m, "fin_m": f.fin_m} for f in fragmentos
        ],
        "cortes_forzados_m": cortes.forzados_m,
        "segmentos": len(fusion.segmentos),
        "recortados": fusion.recortados,
        "descartados": fusion.descartados,
        "ms_con_habla": sum(s.t1_ms - s.t0_ms for s in fusion.segmentos),
        "senales": {
            nombre: sum(1 for s in fusion.segmentos if nombre in s.senales)
            for nombre in ("repeticion", "baja_prob", "compresion", "no_habla")
        },
        "hueco_transcripcion_s": HUECO_TRANSCRIPCION_S,
        "huecos": huecos(fusion.segmentos, fin_ms),
        "sha256_cruda": sha_cruda,
        "glosario_sha256_inicial": glosario.sha256,
        "generado_el": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    if reemplaza_a:
        manifiesto["reemplaza_a"] = reemplaza_a
    ruta_manifiesto = repo / DIRECTORIO_MANIFIESTOS / f"{tid}.yaml"
    if not ruta_manifiesto.exists():
        ruta_manifiesto.parent.mkdir(parents=True, exist_ok=True)
        ruta_manifiesto.write_text(
            "# GENERADO por `botsito corpus transcribe`. INMUTABLE: no editar; una retranscripcion "
            "es otro manifiesto con reemplaza_a.\n"
            + yaml.safe_dump(manifiesto, allow_unicode=True, sort_keys=True, width=100),
            encoding="utf-8",
            newline="\n",
        )
    return Resultado(tid, carpeta, cruda, ruta_manifiesto, fusion.segmentos)


def corregir(carpeta: Path, cruda: list[Segmento], glosario: Glosario, tid: str) -> int:
    """Escribe corregida.jsonl (= cruda + glosario) y correcciones.jsonl. Regenerable."""
    corregida, registro, dudas = aplicar(cruda, glosario, tid)
    escribir_atomico(carpeta / FICHERO_CORREGIDA, a_jsonl(corregida))
    escribir_atomico(carpeta / FICHERO_CORRECCIONES, correcciones_jsonl(glosario, registro, dudas))
    return len(registro)


def cargar_cruda(carpeta: Path) -> list[Segmento]:
    return desde_jsonl((carpeta / FICHERO_CRUDA).read_text(encoding="utf-8"))


def cargar_corregida(carpeta: Path) -> list[Segmento]:
    return desde_jsonl((carpeta / FICHERO_CORREGIDA).read_text(encoding="utf-8"))
