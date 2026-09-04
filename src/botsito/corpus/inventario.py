"""Inventario del corpus (F03): manifiesto determinista con hash, papel y metadatos de video.

Entradas: `knowledge/corpus/fuentes.yaml` (lo que DEBE haber) y la carpeta `corpus/` (lo que HAY).
Salida: `knowledge/corpus/manifest.yaml`. Sin fechas de generacion, para que regenerar no
produzca diff si el disco no cambio. Los huecos de cobertura se calculan sobre los `index.txt`
de fotogramas heredados: un tramo sin fotograma mayor que el umbral es un tramo que nadie vio.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from botsito.yaml_estricto import YamlError, cargar_yaml

PAPELES_CARPETA = ("heredado_v2", "material_adicional")
VERSION_MANIFIESTO = 1
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_LINEA_INDICE = re.compile(r"^(\S+)\s+(\d+:\d{2}:\d{2})\s+([\d.]+)\s*$")


class InventarioError(ValueError):
    """El corpus en disco no coincide con las fuentes esperadas, o un fichero es invalido."""


@dataclass(frozen=True, slots=True)
class FuenteVideo:
    video_id: str
    fichero: str
    drive_id: str
    bytes: int
    fecha_grabacion: str
    naturaleza: str


@dataclass(frozen=True, slots=True)
class CarpetaFuente:
    ruta: str
    papel: str
    descripcion: str


@dataclass(frozen=True, slots=True)
class Fuentes:
    raiz: str
    videos: tuple[FuenteVideo, ...]
    carpetas: tuple[CarpetaFuente, ...]
    umbral_hueco_segundos: int


@dataclass(frozen=True, slots=True)
class InfoVideo:
    duracion_s: float
    ancho: int
    alto: int
    fps: str
    audio: bool


def cargar_fuentes(ruta: Path) -> Fuentes:
    if not ruta.exists():
        raise InventarioError(f"no existe {ruta}")
    try:
        doc = cargar_yaml(ruta.read_text(encoding="utf-8")) or {}
    except YamlError as exc:
        raise InventarioError(f"{ruta}: {exc}") from exc
    try:
        videos = tuple(
            FuenteVideo(
                video_id=str(v["video_id"]),
                fichero=str(v["fichero"]),
                drive_id=str(v["drive_id"]),
                bytes=_entero(v["bytes"], "bytes"),
                fecha_grabacion=str(v["fecha_grabacion"]),
                naturaleza=str(v["naturaleza"]).strip(),
            )
            for v in doc["videos"]
        )
        carpetas = tuple(
            CarpetaFuente(str(c["ruta"]), str(c["papel"]), str(c["descripcion"]).strip())
            for c in doc.get("carpetas", [])
        )
        fuentes = Fuentes(
            raiz=str(doc["raiz"]),
            videos=videos,
            carpetas=carpetas,
            umbral_hueco_segundos=_entero(doc.get("umbral_hueco_segundos", 180), "umbral"),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise InventarioError(f"{ruta}: esquema invalido ({exc})") from exc
    ids = [v.video_id for v in fuentes.videos]
    if len(ids) != len(set(ids)):
        raise InventarioError("video_id duplicado en fuentes")
    for c in fuentes.carpetas:
        if c.papel not in PAPELES_CARPETA:
            raise InventarioError(f"papel desconocido {c.papel!r} para {c.ruta}")
    if fuentes.umbral_hueco_segundos <= 0:
        raise InventarioError("umbral_hueco_segundos debe ser positivo")
    return fuentes


def _entero(valor: object, campo: str) -> int:
    """Un entero de verdad: `1.5` no se trunca y `true` no vale 1."""
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise ValueError(f"{campo} debe ser un entero, no {valor!r}")
    return valor


def sha256_fichero(ruta: Path, bloque: int = 8 * 1024 * 1024) -> str:
    h = hashlib.sha256()
    with ruta.open("rb") as f:
        while True:
            trozo = f.read(bloque)
            if not trozo:
                break
            h.update(trozo)
    return h.hexdigest()


def ffprobe_disponible() -> str | None:
    return shutil.which("ffprobe")


def ffprobe_version() -> str:
    exe = ffprobe_disponible()
    if exe is None:
        raise InventarioError("ffprobe no esta en PATH")
    resultado = subprocess.run(
        [exe, "-version"], capture_output=True, encoding="utf-8", errors="replace", check=False
    )
    if resultado.returncode != 0:
        raise InventarioError(f"ffprobe -version fallo: {resultado.stderr.strip()[:80]}")
    salida = resultado.stdout
    m = re.search(r"ffprobe version (\d+(?:\.\d+)*)", salida)
    if m is None:
        raise InventarioError(f"no se pudo leer la version de ffprobe: {salida[:80]!r}")
    return m.group(1)


def ffprobe_info(ruta: Path) -> InfoVideo:
    exe = ffprobe_disponible()
    if exe is None:
        raise InventarioError("ffprobe no esta en PATH")
    args = [
        exe,
        "-v",
        "error",
        "-show_entries",
        "format=duration:stream=codec_type,width,height,r_frame_rate",
        "-of",
        "json",
        str(ruta),
    ]
    resultado = subprocess.run(
        args, capture_output=True, encoding="utf-8", errors="replace", check=False
    )
    if resultado.returncode != 0:
        raise InventarioError(f"ffprobe fallo sobre {ruta.name}: {resultado.stderr.strip()}")
    try:
        doc = json.loads(resultado.stdout)
    except json.JSONDecodeError as exc:
        raise InventarioError(f"{ruta.name}: ffprobe no devolvio JSON ({exc})") from exc
    video = next((s for s in doc.get("streams", []) if s.get("codec_type") == "video"), None)
    if video is None:
        raise InventarioError(f"{ruta.name}: sin pista de video")
    audio = any(s.get("codec_type") == "audio" for s in doc.get("streams", []))
    try:
        duracion = float(doc["format"]["duration"])
    except (KeyError, TypeError, ValueError) as exc:
        raise InventarioError(f"{ruta.name}: ffprobe no devolvio una duracion numerica") from exc
    return InfoVideo(
        duracion_s=duracion,
        ancho=int(video["width"]),
        alto=int(video["height"]),
        fps=str(video.get("r_frame_rate", "")),
        audio=audio,
    )


def clasificar(relativa: str, fuentes: Fuentes) -> str:
    """Papel de un fichero por su ruta relativa a la raiz del corpus."""
    if relativa in {v.fichero for v in fuentes.videos}:
        return "video_original"
    for c in sorted(fuentes.carpetas, key=lambda c: -len(c.ruta)):
        if relativa == c.ruta or relativa.startswith(c.ruta + "/"):
            return c.papel
    return "sin_clasificar"


def huecos_en_indice(
    texto: str, umbral_s: int, duracion_s: float | None = None
) -> list[dict[str, float]]:
    """Tramos sin fotograma mayores que el umbral, a partir de un index.txt heredado.

    Cada linea: `nombre h:mm:ss segundos`. Se considera tambien el tramo inicial (desde 0) y, si
    se conoce la duracion del video, el tramo final.
    """
    marcas: list[float] = []
    for linea in texto.splitlines():
        m = _LINEA_INDICE.match(linea.strip())
        if m:
            try:
                marcas.append(float(m.group(3)))
            except ValueError:
                continue  # linea corrupta del indice heredado: se ignora, no se inventa
    marcas.sort()
    puntos = [0.0, *marcas]
    if duracion_s is not None:
        puntos.append(duracion_s)
    huecos: list[dict[str, float]] = []
    for a, b in zip(puntos, puntos[1:], strict=False):
        if b - a > umbral_s:
            huecos.append(
                {"desde_s": round(a, 1), "hasta_s": round(b, 1), "segundos": round(b - a, 1)}
            )
    return huecos


def _video_id_de_ruta(relativa: str, fuentes: Fuentes) -> str | None:
    for parte in Path(relativa).parts:
        for v in fuentes.videos:
            if parte == v.video_id:
                return v.video_id
    return None


def inventariar(raiz_repo: Path, fuentes: Fuentes, hashear: bool = True) -> dict[str, Any]:
    raiz = raiz_repo / fuentes.raiz
    if not raiz.is_dir():
        raise InventarioError(f"no existe la raiz del corpus: {raiz}")
    videos: list[dict[str, Any]] = []
    duraciones: dict[str, float] = {}
    for fuente in fuentes.videos:
        ruta = raiz / fuente.fichero
        if not ruta.is_file():
            raise InventarioError(f"falta el video {fuente.video_id}: {fuente.fichero}")
        tam = ruta.stat().st_size
        if tam != fuente.bytes:
            raise InventarioError(
                f"{fuente.video_id}: {tam} bytes en disco, {fuente.bytes} esperados (Drive)"
            )
        info = ffprobe_info(ruta)
        duraciones[fuente.video_id] = info.duracion_s
        videos.append(
            {
                "video_id": fuente.video_id,
                "fichero": fuente.fichero,
                "drive_id": fuente.drive_id,
                "fecha_grabacion": fuente.fecha_grabacion,
                "bytes": tam,
                "sha256": sha256_fichero(ruta) if hashear else None,
                "duracion_s": round(info.duracion_s, 3),
                "ancho": info.ancho,
                "alto": info.alto,
                "fps": info.fps,
                "audio": info.audio,
            }
        )
    ficheros: list[dict[str, Any]] = []
    indices: list[dict[str, Any]] = []
    videos_set = {v.fichero for v in fuentes.videos}
    # Orden por la cadena POSIX de la ruta: Path compara sin distinguir mayusculas en Windows y
    # con ellas en Linux, y el manifiesto debe ser identico en ambos.
    candidatos = sorted((p.relative_to(raiz).as_posix(), p) for p in raiz.rglob("*") if p.is_file())
    for relativa, ruta in candidatos:
        if relativa in videos_set:
            continue
        papel = clasificar(relativa, fuentes)
        ficheros.append(
            {
                "ruta": relativa,
                "papel": papel,
                "bytes": ruta.stat().st_size,
                "sha256": sha256_fichero(ruta) if hashear else None,
            }
        )
        if papel == "heredado_v2" and ruta.name == "index.txt":
            vid = _video_id_de_ruta(relativa, fuentes)
            texto = ruta.read_text(encoding="utf-8", errors="replace")
            n = sum(1 for linea in texto.splitlines() if _LINEA_INDICE.match(linea.strip()))
            indices.append(
                {
                    "ruta": relativa,
                    "video_id": vid,
                    "fotogramas": n,
                    "huecos": huecos_en_indice(
                        texto, fuentes.umbral_hueco_segundos, duraciones.get(vid or "")
                    ),
                }
            )
    resumen: dict[str, dict[str, int]] = {}
    for f in ficheros:
        r = resumen.setdefault(str(f["papel"]), {"ficheros": 0, "bytes": 0})
        r["ficheros"] += 1
        r["bytes"] += int(f["bytes"])
    resumen["video_original"] = {
        "ficheros": len(videos),
        "bytes": sum(int(v["bytes"]) for v in videos),
    }
    return {
        "version": VERSION_MANIFIESTO,
        "raiz": fuentes.raiz,
        "ffprobe": ffprobe_version(),
        "umbral_hueco_segundos": fuentes.umbral_hueco_segundos,
        "videos": videos,
        "ficheros": ficheros,
        "indices_heredados": indices,
        "resumen": dict(sorted(resumen.items())),
    }


def escribir_manifiesto(manifiesto: dict[str, Any], ruta: Path) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    texto = yaml.safe_dump(manifiesto, allow_unicode=True, sort_keys=True, width=100)
    ruta.write_text(
        "# GENERADO por `botsito corpus inventory`. No editar a mano. Ver fuentes.yaml.\n" + texto,
        encoding="utf-8",
        newline="\n",
    )


def cargar_manifiesto(ruta: Path) -> dict[str, Any]:
    if not ruta.exists():
        raise InventarioError(f"no existe {ruta}")
    try:
        doc = cargar_yaml(ruta.read_text(encoding="utf-8"))
    except YamlError as exc:
        raise InventarioError(f"{ruta}: {exc}") from exc
    if not isinstance(doc, dict):
        raise InventarioError(f"{ruta}: no es un mapa")
    return doc


def validar_manifiesto(manifiesto: dict[str, Any], fuentes: Fuentes) -> list[str]:
    """Problemas de esquema y de coherencia con las fuentes. Lista vacia = OK."""
    problemas: list[str] = []
    if manifiesto.get("version") != VERSION_MANIFIESTO:
        problemas.append(f"version {manifiesto.get('version')!r}, esperada {VERSION_MANIFIESTO}")
    if manifiesto.get("raiz") != fuentes.raiz:
        problemas.append("la raiz del manifiesto no coincide con fuentes.yaml")
    for clave in ("videos", "ficheros"):
        lista = manifiesto.get(clave)
        if lista is not None and (
            not isinstance(lista, list) or not all(isinstance(x, dict) for x in lista)
        ):
            problemas.append(f"'{clave}' debe ser una lista de mapas")
            return problemas
    videos = {v.get("video_id"): v for v in manifiesto.get("videos") or []}
    for fuente in fuentes.videos:
        v = videos.get(fuente.video_id)
        if v is None:
            problemas.append(f"falta {fuente.video_id} en el manifiesto")
            continue
        if v.get("bytes") != fuente.bytes:
            problemas.append(f"{fuente.video_id}: bytes {v.get('bytes')} != {fuente.bytes}")
        for campo in ("sha256", "duracion_s", "ancho", "alto"):
            if not v.get(campo):
                problemas.append(f"{fuente.video_id}: falta {campo}")
        d = v.get("duracion_s")
        if d is not None and (isinstance(d, bool) or not isinstance(d, int | float)):
            problemas.append(f"{fuente.video_id}: duracion_s debe ser numerica, no {d!r}")
        if v.get("audio") is not True:
            problemas.append(f"{fuente.video_id}: sin pista de audio")
    rutas_vistas: set[str] = set()
    for f in manifiesto.get("ficheros") or []:
        ruta = str(f.get("ruta", ""))
        if not ruta or ruta in rutas_vistas:
            problemas.append(f"fichero sin ruta o duplicado: {ruta!r}")
        rutas_vistas.add(ruta)
        if f.get("papel") == "sin_clasificar":
            problemas.append(f"fichero sin clasificar: {ruta}")
        elif f.get("papel") not in PAPELES_CARPETA:
            problemas.append(f"papel invalido {f.get('papel')!r}: {ruta}")
        b = f.get("bytes")
        if isinstance(b, bool) or not isinstance(b, int) or b < 0:
            problemas.append(f"bytes invalidos: {ruta}")
        h = f.get("sha256")
        if h is not None and not _SHA256.match(str(h)):
            problemas.append(f"sha256 invalido: {ruta}")
    rutas = [str(f.get("ruta", "")) for f in manifiesto.get("ficheros") or []]
    if rutas != sorted(rutas):
        problemas.append("los ficheros no estan en orden POSIX (manifiesto no determinista)")
    return problemas


def comprobar_contra_disco(
    manifiesto: dict[str, Any], raiz_repo: Path, hashes: bool = False
) -> list[str]:
    raiz = raiz_repo / str(manifiesto["raiz"])
    problemas: list[str] = []
    entradas = [(v["fichero"], v) for v in manifiesto.get("videos") or []]
    entradas += [(f["ruta"], f) for f in manifiesto.get("ficheros") or []]
    for relativa, e in entradas:
        ruta = raiz / relativa
        if not ruta.is_file():
            problemas.append(f"falta en disco: {relativa}")
            continue
        if ruta.stat().st_size != e["bytes"]:
            problemas.append(f"tamano distinto: {relativa}")
        elif hashes and e.get("sha256") and sha256_fichero(ruta) != e["sha256"]:
            problemas.append(f"hash distinto: {relativa}")
    conocidas = {relativa for relativa, _ in entradas}
    if raiz.is_dir():
        for p in raiz.rglob("*"):
            if p.is_file() and p.relative_to(raiz).as_posix() not in conocidas:
                problemas.append(f"no inventariado: {p.relative_to(raiz).as_posix()}")
    return sorted(problemas)
