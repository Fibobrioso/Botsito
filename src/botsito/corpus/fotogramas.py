"""Fotogramas del corpus (F05, ADR-0008): cobertura completa a 1 fps, sin perdida, indexada.

Hechos tecnicos (no de negocio; se copian al manifiesto de cada extraccion):

- Regla unica de seleccion, para regulares y obligatorios: "primer fotograma fuente con
  `t >= instante`". Los regulares salen en una pasada con el filtro `select`
  (`SELECCION`) y `-fps_mode passthrough`, que conserva el `pts` original del fotograma
  elegido; `fps=1` NO sirve (elige el fotograma en `n + 0,47 s` y reescribe el `pts`).
  Los obligatorios con fraccion de segundo salen con `-ss <t> -copyts` (sin `-copyts` el
  `pts` sale 0). Un obligatorio en segundo entero ES el regular: misma imagen, mismo hash.
- `pts_ms` real se lee de `showinfo` (colocado DESPUES de `select`); `t_ms` nominal es
  `pts_ms // 1000 * 1000` para un regular y el instante pedido para un obligatorio. ffmpeg
  escribe una secuencia `%06d.png` y aqui se renombra a `<t_ms>.png` con el `pts` parseado.
- PNG (sin perdida) con `-fflags +bitexact -flags +bitexact`: mismo video, misma build de
  ffmpeg -> mismo fichero byte a byte. El hash depende del decodificador H.264 de la build.
- `huecos` se calcula sobre `pts` consecutivos: `select` no fabrica fotogramas, un salto de
  la fuente se ve. El umbral es una constante tecnica.

Disposicion bajo la carpeta de datos (`[rutas].data`, ignorada por git):

    data/fotogramas/<video_id>/<nombre>/<t_ms>.png      (regulares y extra)
    data/fotogramas/<video_id>/<nombre>/index.jsonl     (una linea por fotograma; su sha256
                                                         forma el id del manifiesto)

y el manifiesto INMUTABLE, versionado, en `knowledge/corpus/fotogramas/<fotogramas_id>.yaml`
con `fotogramas_id = fr-<video_id>-<hash8 del sha256 de index.jsonl>`.
"""

from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from botsito.comun import ids
from botsito.comun.documentos import hash_corto, sha256_hex
from botsito.comun.yaml_estricto import YamlError, cargar_yaml
from botsito.corpus.audio import version_ffmpeg
from botsito.corpus.inventario import sha256_fichero
from botsito.corpus.transcripcion import escribir_atomico, formato_ms, parse_ms

CARPETA_DATOS = "fotogramas"
DIRECTORIO_MANIFIESTOS = "knowledge/corpus/fotogramas"
FICHERO_OBLIGATORIOS = "knowledge/corpus/fotogramas_obligatorios.yaml"
FICHERO_INDICE = "index.jsonl"
FICHERO_HUELLA = "huella.txt"
FICHERO_VIDEO_CARPETA = "video.sha256"
SCHEMA_VERSION = 1
FPS = 1
FORMATO = "png"
NOMBRE = f"{FORMATO}-{FPS}fps"
HUECO_FOTOGRAMAS_MS = 2000  # no-negocio: umbral tecnico de hueco entre fotogramas (tabla A)
SELECCION = "isnan(prev_selected_t)+gte(floor(t),floor(prev_selected_t)+1)"
ORIGENES = ("regular", "obligatorio")
_SHOWINFO = re.compile(
    r"\[Parsed_showinfo_\d+ @ [^\]]+\] n:\s*(\d+) pts:\s*-?\d+ pts_time:\s*(-?\d+(?:\.\d+)?)"
    r".*? s:(\d+)x(\d+)"
)
_HEX = re.compile(r"^[0-9a-f]{64}$")


class FotogramasError(RuntimeError):
    """ffmpeg fallo, el indice es incoherente o un instante pedido no existe."""


@dataclass(frozen=True, slots=True)
class Fotograma:
    n: int
    t_ms: int  # nominal: segundo entero (regular) o instante pedido (obligatorio)
    pts_ms: int  # marca real del fotograma fuente elegido
    fichero: str
    sha256: str
    bytes: int
    origen: str

    def __post_init__(self) -> None:
        if self.n < 0 or self.t_ms < 0 or self.pts_ms < 0 or self.bytes <= 0:
            raise FotogramasError(f"fotograma {self.n}: valores negativos o fichero vacio")
        if self.pts_ms < self.t_ms:
            raise FotogramasError(f"fotograma {self.n}: pts {self.pts_ms} anterior a t {self.t_ms}")
        if not _HEX.match(self.sha256):
            raise FotogramasError(f"fotograma {self.n}: sha256 invalido")
        if self.origen not in ORIGENES:
            raise FotogramasError(f"fotograma {self.n}: origen desconocido {self.origen!r}")
        if self.fichero != nombre_fichero(self.t_ms):
            raise FotogramasError(
                f"fotograma {self.n}: fichero debe ser {nombre_fichero(self.t_ms)}"
            )


@dataclass(frozen=True, slots=True)
class Obligatorio:
    video_id: str
    t_ms: int
    motivo: str
    marca_heredada: str | None


@dataclass(frozen=True, slots=True)
class Resultado:
    fotogramas_id: str
    carpeta: Path
    indice: Path
    manifiesto: Path
    fotogramas: list[Fotograma]


def nombre_fichero(t_ms: int) -> str:
    return f"{t_ms:09d}.{FORMATO}"


def nominal_de(pts_ms: int) -> int:
    return pts_ms // 1000 * 1000


def referencia(fotogramas_id: str, t_ms: int) -> str:
    return f"{fotogramas_id}/{t_ms}"


def id_fotogramas(video_id: str, sha256_index: str) -> str:
    return f"fr-{video_id}-{sha256_index[:8]}"


# --- ffmpeg -------------------------------------------------------------------------------


def _ffmpeg(args: list[str]) -> str:
    try:
        resultado = subprocess.run(
            ["ffmpeg", "-hide_banner", "-nostdin", *args],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except FileNotFoundError as exc:
        raise FotogramasError("ffmpeg no esta en PATH") from exc
    if resultado.returncode != 0:
        raise FotogramasError(f"ffmpeg fallo: {resultado.stderr.strip()[-400:]}")
    return resultado.stderr


def parsear_showinfo(salida: str) -> tuple[list[int], tuple[int, int] | None]:
    """(pts_ms por fotograma emitido, en orden; resolucion). Lineas ajenas se ignoran."""
    pts: list[tuple[int, int]] = []
    resolucion: tuple[int, int] | None = None
    for m in _SHOWINFO.finditer(salida):
        pts.append((int(m.group(1)), round(float(m.group(2)) * 1000)))
        resolucion = (int(m.group(3)), int(m.group(4)))
    pts.sort()
    if [n for n, _ in pts] != list(range(len(pts))):
        raise FotogramasError("showinfo: numeracion de fotogramas no consecutiva")
    return [p for _, p in pts], resolucion


_BITEXACT = ["-fflags", "+bitexact", "-flags", "+bitexact"]


def extraer_regulares(video: Path, destino: Path) -> tuple[list[Fotograma], tuple[int, int]]:
    """Una pasada: un fotograma por segundo del video, con su `pts` real. Fotogramas previos en
    `destino` se borran (la pasada es determinista y se rehace entera)."""
    if not video.is_file():
        raise FotogramasError(f"no existe el video {video}")
    destino.mkdir(parents=True, exist_ok=True)
    for viejo in destino.glob(f"*.{FORMATO}"):
        viejo.unlink()
    temporal = destino / "_tmp"
    temporal.mkdir(exist_ok=True)
    for viejo in temporal.glob("*"):
        viejo.unlink()
    salida = _ffmpeg(
        [
            "-v",
            "info",
            "-y",
            "-i",
            str(video),
            "-vf",
            f"select='{SELECCION}',showinfo",
            "-fps_mode",
            "passthrough",
            *_BITEXACT,
            "-f",
            "image2",
            str(temporal / f"%06d.{FORMATO}"),
        ]
    )
    pts, resolucion = parsear_showinfo(salida)
    ficheros = sorted(temporal.glob(f"*.{FORMATO}"))
    if len(ficheros) != len(pts) or not pts or resolucion is None:
        raise FotogramasError(
            f"{video.name}: ffmpeg escribio {len(ficheros)} fotogramas y showinfo informo "
            f"de {len(pts)}"
        )
    fotogramas: list[Fotograma] = []
    vistos: set[int] = set()
    for n, (fichero, p) in enumerate(zip(ficheros, pts, strict=True)):
        t_ms = nominal_de(p)
        if t_ms in vistos:
            raise FotogramasError(f"{video.name}: dos fotogramas para el segundo {t_ms // 1000}")
        vistos.add(t_ms)
        final = destino / nombre_fichero(t_ms)
        fichero.replace(final)
        datos = final.read_bytes()
        fotogramas.append(
            Fotograma(n, t_ms, p, final.name, sha256_hex(datos), len(datos), "regular")
        )
    temporal.rmdir()
    return fotogramas, resolucion


def extraer_instante(video: Path, t_ms: int, destino: Path) -> tuple[int, bytes]:
    """(pts_ms real, bytes PNG) del primer fotograma con `t >= t_ms`, misma regla que la pasada."""
    if not video.is_file():
        raise FotogramasError(f"no existe el video {video}")
    destino.mkdir(parents=True, exist_ok=True)
    temporal = destino / f"_instante_{t_ms}.{FORMATO}"
    salida = _ffmpeg(
        [
            "-v",
            "info",
            "-y",
            "-ss",
            f"{t_ms / 1000:.3f}",
            "-copyts",
            "-i",
            str(video),
            "-frames:v",
            "1",
            "-vf",
            "showinfo",
            *_BITEXACT,
            str(temporal),
        ]
    )
    # showinfo puede informar de mas de un fotograma (el grafo de filtros va por delante del
    # `-frames:v 1` del codificador); el escrito es el primero.
    pts, _ = parsear_showinfo(salida)
    if not pts or not temporal.is_file():
        temporal.unlink(missing_ok=True)
        raise FotogramasError(
            f"{video.name}: no hay fotograma en {formato_ms(t_ms)} (fin del video)"
        )
    datos = temporal.read_bytes()
    temporal.unlink()
    if pts[0] < t_ms:
        raise FotogramasError(
            f"{video.name}: ffmpeg devolvio pts {pts[0]} ms para el instante {t_ms} ms"
        )
    return pts[0], datos


# --- indice -------------------------------------------------------------------------------


def a_jsonl(fotogramas: list[Fotograma]) -> str:
    lineas = []
    for f in fotogramas:
        doc = {
            "n": f.n,
            "t_ms": f.t_ms,
            "pts_ms": f.pts_ms,
            "fichero": f.fichero,
            "sha256": f.sha256,
            "bytes": f.bytes,
            "origen": f.origen,
        }
        lineas.append(json.dumps(doc, ensure_ascii=False, sort_keys=True))
    return "\n".join(lineas) + ("\n" if lineas else "")


def desde_jsonl(texto: str) -> list[Fotograma]:
    fotogramas: list[Fotograma] = []
    for i, linea in enumerate(texto.splitlines()):
        if not linea.strip():
            continue
        try:
            doc = json.loads(linea)
        except json.JSONDecodeError as exc:
            raise FotogramasError(f"indice linea {i + 1}: JSON invalido") from exc
        claves = {"n", "t_ms", "pts_ms", "fichero", "sha256", "bytes", "origen"}
        if not isinstance(doc, dict) or set(doc) != claves:
            raise FotogramasError(f"indice linea {i + 1}: claves {sorted(doc)!r}")
        for k in ("n", "t_ms", "pts_ms", "bytes"):
            if isinstance(doc[k], bool) or not isinstance(doc[k], int):
                raise FotogramasError(f"indice linea {i + 1}: {k} debe ser entero")
        if not isinstance(doc["fichero"], str) or not isinstance(doc["sha256"], str):
            raise FotogramasError(f"indice linea {i + 1}: fichero y sha256 deben ser texto")
        fotogramas.append(
            Fotograma(
                doc["n"],
                doc["t_ms"],
                doc["pts_ms"],
                doc["fichero"],
                doc["sha256"],
                doc["bytes"],
                str(doc["origen"]),
            )
        )
    validar_indice(fotogramas)
    return fotogramas


def validar_indice(fotogramas: list[Fotograma]) -> None:
    """`n` consecutivos desde 0, `t_ms` unicos y crecientes, `pts` crecientes, regulares en
    segundos enteros, los extra con fraccion."""
    if not fotogramas:
        raise FotogramasError("indice vacio")
    if [f.n for f in fotogramas] != list(range(len(fotogramas))):
        raise FotogramasError("indice: n no consecutivos desde 0")
    for a, b in zip(fotogramas, fotogramas[1:], strict=False):
        if b.t_ms <= a.t_ms or b.pts_ms < a.pts_ms:
            raise FotogramasError(f"indice: fotograma {b.n} no es posterior al {a.n}")
    for f in fotogramas:
        if f.origen == "regular" and f.t_ms % 1000 != 0:
            raise FotogramasError(f"indice: regular {f.n} fuera de un segundo entero")
        if f.origen == "obligatorio" and f.t_ms % 1000 == 0:
            raise FotogramasError(
                f"indice: obligatorio {f.n} en segundo entero (deberia ser el regular)"
            )


def huecos(
    fotogramas: list[Fotograma], umbral_ms: int = HUECO_FOTOGRAMAS_MS
) -> list[dict[str, int]]:
    """Tramos sin fotograma mayores que `umbral_ms` sobre los `pts` reales (desde 0)."""
    puntos = [0, *sorted(f.pts_ms for f in fotogramas)]
    salida: list[dict[str, int]] = []
    for a, b in zip(puntos, puntos[1:], strict=False):
        if b - a > umbral_ms:
            salida.append({"desde_ms": a, "hasta_ms": b, "ms": b - a})
    return salida


def plan_instantes(obligatorios_ms: list[int], fin_ms: int) -> list[int]:
    """Instantes obligatorios que necesitan extraccion propia (fraccion de segundo). Un instante
    en segundo entero ya es un regular. En o despues del fin del video, o repetido: error (si el
    video acaba antes del ultimo fotograma esperado, `extraer_instante` lo dira)."""
    vistos: set[int] = set()
    extra: list[int] = []
    for t in obligatorios_ms:
        if t < 0 or t >= fin_ms:
            raise FotogramasError(
                f"instante {formato_ms(t)} fuera del video (dura {formato_ms(fin_ms)})"
            )
        if t in vistos:
            raise FotogramasError(f"instante {formato_ms(t)} repetido")
        vistos.add(t)
        if t % 1000 != 0:
            extra.append(t)
    return sorted(extra)


def mas_cercanos(fotogramas: list[Fotograma], t_ms: int, n: int = 1) -> list[Fotograma]:
    """Los `n` fotogramas con `pts` mas cercano a `t_ms` (empate: el anterior), en orden de pts."""
    if n < 1:
        raise FotogramasError("n debe ser >= 1")
    if not fotogramas:
        raise FotogramasError("indice vacio")
    if t_ms < 0 or t_ms > fotogramas[-1].pts_ms + 1000:
        raise FotogramasError(f"{formato_ms(t_ms)} esta fuera del video")
    elegidos = sorted(fotogramas, key=lambda f: (abs(f.pts_ms - t_ms), f.pts_ms))[:n]
    return sorted(elegidos, key=lambda f: f.pts_ms)


# --- obligatorios -------------------------------------------------------------------------


def cargar_obligatorios(ruta: Path) -> list[Obligatorio]:
    """`knowledge/corpus/fotogramas_obligatorios.yaml`: lista escrita a mano de instantes que
    deben existir con precision de fotograma (motivo obligatorio)."""
    if not ruta.is_file():
        return []
    try:
        doc = cargar_yaml(ruta.read_text(encoding="utf-8"))
    except YamlError as exc:
        raise FotogramasError(f"{ruta.name}: {exc}") from exc
    if (
        not isinstance(doc, dict)
        or set(doc) != {"fotogramas"}
        or not isinstance(doc["fotogramas"], list)
    ):
        raise FotogramasError(f"{ruta.name}: se espera un mapa con la lista 'fotogramas'")
    salida: list[Obligatorio] = []
    vistos: set[tuple[str, int]] = set()
    for i, o in enumerate(doc["fotogramas"]):
        if not isinstance(o, dict) or not {"video_id", "t", "motivo"} <= set(o):
            raise FotogramasError(f"{ruta.name}: entrada {i}: faltan video_id, t o motivo")
        ajenos = set(o) - {"video_id", "t", "motivo", "marca_heredada"}
        if ajenos:
            raise FotogramasError(f"{ruta.name}: entrada {i}: campos desconocidos {sorted(ajenos)}")
        try:
            t_ms = parse_ms(str(o["t"]))
        except ValueError as exc:
            raise FotogramasError(f"{ruta.name}: entrada {i}: {exc}") from exc
        video_id = str(o["video_id"])
        if not str(o["motivo"]).strip():
            raise FotogramasError(f"{ruta.name}: entrada {i}: motivo vacio")
        if (video_id, t_ms) in vistos:
            raise FotogramasError(f"{ruta.name}: {video_id} {o['t']} repetido")
        vistos.add((video_id, t_ms))
        marca = o.get("marca_heredada")
        salida.append(Obligatorio(video_id, t_ms, str(o["motivo"]), str(marca) if marca else None))
    return salida


# --- orquestacion ---------------------------------------------------------------------------


def carpeta_video(carpeta_datos: Path, video_id: str) -> Path:
    return carpeta_datos / CARPETA_DATOS / video_id


def _leer(ruta: Path) -> str:
    try:
        return ruta.read_text(encoding="utf-8").strip()
    except OSError:
        return ""


def _carpeta_para(cv: Path, huella: str, sha256_video: str) -> Path:
    """`<nombre>` la primera vez; si esa carpeta pertenece a otra huella (otra build de ffmpeg,
    otra regla) o a otro video, `<nombre>-<hash8>`: una re-extraccion no pisa la anterior (su
    manifiesto es inmutable y sigue apuntando a su carpeta)."""
    carpeta = cv / NOMBRE
    marca = carpeta / FICHERO_HUELLA
    marca_video = carpeta / FICHERO_VIDEO_CARPETA
    ajena = carpeta.is_dir() and (
        (marca.exists() and _leer(marca) != huella)
        or (marca_video.exists() and _leer(marca_video) != sha256_video)
    )
    if ajena:
        carpeta = cv / f"{NOMBRE}-{hash_corto(huella + sha256_video)}"
        marca = carpeta / FICHERO_HUELLA
        marca_video = carpeta / FICHERO_VIDEO_CARPETA
    carpeta.mkdir(parents=True, exist_ok=True)
    if not marca.exists():
        escribir_atomico(marca, huella + "\n")
    if not marca_video.exists():
        escribir_atomico(marca_video, sha256_video + "\n")
    return carpeta


def parametros() -> dict[str, Any]:
    return {"fps": FPS, "formato": FORMATO, "seleccion": SELECCION, "bitexact": True}


def huella_de(ffmpeg: str, extra_ms: list[int]) -> str:
    """Huella de una carpeta de trabajo: build de ffmpeg, parametros e instantes extra."""
    return hash_corto(
        json.dumps({"ffmpeg": ffmpeg, "extra_ms": extra_ms, **parametros()}, sort_keys=True)
    )


def _indice_utilizable(
    carpeta: Path, obligatorios_ms: list[int], fin_ms: int
) -> list[Fotograma] | None:
    """Indice ya escrito cuyos ficheros siguen en disco (por tamano) y que cubre los obligatorios.
    Si falta algo, None: se rehace la pasada (determinista)."""
    indice = carpeta / FICHERO_INDICE
    if not indice.is_file():
        return None
    try:
        fotogramas = desde_jsonl(indice.read_text(encoding="utf-8"))
    except FotogramasError:
        return None
    for f in fotogramas:
        ruta = carpeta / f.fichero
        if not ruta.is_file() or ruta.stat().st_size != f.bytes:
            return None
    presentes = {f.t_ms for f in fotogramas}
    try:
        extra = plan_instantes(obligatorios_ms, fin_ms)
    except FotogramasError:
        return None
    if any(t not in presentes for t in extra):
        return None
    return fotogramas


def extraer_video(
    repo: Path,
    carpeta_datos: Path,
    raiz_corpus: Path,
    video_id: str,
    fichero_video: str,
    sha256_video: str,
    duracion_video_s: float,
    obligatorios_ms: list[int],
    reemplaza_a: str | None = None,
    comprobar_hash_video: bool = True,
    progreso: Any = None,
) -> Resultado:
    """Cobertura completa a 1 fps mas los obligatorios con fraccion; indice y manifiesto."""
    video = raiz_corpus / fichero_video
    if not video.is_file():
        raise FotogramasError(f"no existe el video {video}")
    if comprobar_hash_video and sha256_fichero(video) != sha256_video:
        raise FotogramasError(
            f"{fichero_video}: el sha256 no coincide con el manifiesto del corpus"
        )
    ffmpeg = version_ffmpeg()
    fin_ms = round(duracion_video_s * 1000)
    extra_ms = plan_instantes(obligatorios_ms, fin_ms)
    # La huella lleva los instantes extra: otro conjunto de obligatorios es otra carpeta (la
    # anterior sigue siendo verificable por su manifiesto inmutable).
    huella = huella_de(ffmpeg, extra_ms)
    cv = carpeta_video(carpeta_datos, video_id)
    carpeta = _carpeta_para(cv, huella, sha256_video)
    carpeta_rel = f"{CARPETA_DATOS}/{video_id}/{carpeta.name}"
    _comprobar_activa(repo, video_id, carpeta_rel, reemplaza_a)
    previo = _indice_utilizable(carpeta, obligatorios_ms, fin_ms)
    if previo is not None:
        fotogramas = previo
        resolucion = _resolucion_de(carpeta / fotogramas[0].fichero)
        if progreso:
            progreso(
                f"{video_id}: indice ya completo ({len(fotogramas)} fotogramas), no se decodifica"
            )
    else:
        if progreso:
            progreso(f"{video_id}: decodificando {fichero_video} ({duracion_video_s:.0f} s)")
        regulares, resolucion = extraer_regulares(video, carpeta)
        fotogramas = list(regulares)
        for t in extra_ms:
            pts, datos = extraer_instante(video, t, carpeta)
            final = carpeta / nombre_fichero(t)
            final.write_bytes(datos)
            fotogramas.append(
                Fotograma(0, t, pts, final.name, sha256_hex(datos), len(datos), "obligatorio")
            )
        fotogramas.sort(key=lambda f: f.t_ms)
        fotogramas = [
            Fotograma(i, f.t_ms, f.pts_ms, f.fichero, f.sha256, f.bytes, f.origen)
            for i, f in enumerate(fotogramas)
        ]
        validar_indice(fotogramas)
        escribir_atomico(carpeta / FICHERO_INDICE, a_jsonl(fotogramas))
    texto_indice = (carpeta / FICHERO_INDICE).read_bytes()
    sha_index = sha256_hex(texto_indice)
    fid = id_fotogramas(video_id, sha_index)
    _comprobar_inmutabilidad(repo, carpeta_rel, sha_index)
    ultimo_pts = max(f.pts_ms for f in fotogramas)
    manifiesto: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "fotogramas_id": fid,
        "video_id": video_id,
        "fichero_video": fichero_video,
        "sha256_video": sha256_video,
        "duracion_video_s": round(duracion_video_s, 3),
        "resolucion": {"ancho": resolucion[0], "alto": resolucion[1]},
        "ffmpeg": ffmpeg,
        "parametros": parametros(),
        "carpeta": carpeta_rel,
        "n_fotogramas": len(fotogramas),
        "n_regulares": sum(1 for f in fotogramas if f.origen == "regular"),
        "ultimo_pts_ms": ultimo_pts,
        "hueco_fotogramas_ms": HUECO_FOTOGRAMAS_MS,
        "huecos": huecos(fotogramas),
        "extra": [
            {"t_ms": f.t_ms, "pts_ms": f.pts_ms, "sha256": f.sha256}
            for f in fotogramas
            if f.origen == "obligatorio"
        ],
        "sha256_index": sha_index,
        "generado_el": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    if reemplaza_a:
        manifiesto["reemplaza_a"] = reemplaza_a
    ruta_manifiesto = repo / DIRECTORIO_MANIFIESTOS / f"{fid}.yaml"
    if ruta_manifiesto.exists():
        previo_doc = yaml.safe_load(ruta_manifiesto.read_text(encoding="utf-8"))
        anterior = previo_doc.get("reemplaza_a") if isinstance(previo_doc, dict) else None
        if anterior != reemplaza_a:
            raise FotogramasError(
                f"{ruta_manifiesto.name} ya existe con reemplaza_a={anterior!r}; un manifiesto es "
                f"inmutable y no se puede cambiar a {reemplaza_a!r}"
            )
    else:
        escribir_atomico(
            ruta_manifiesto,
            "# GENERADO por `botsito corpus frames extract`. INMUTABLE: no editar; una "
            "re-extraccion es otro manifiesto con reemplaza_a.\n"
            + yaml.safe_dump(manifiesto, allow_unicode=True, sort_keys=True, width=100),
        )
    return Resultado(fid, carpeta, carpeta / FICHERO_INDICE, ruta_manifiesto, fotogramas)


def _manifiestos_crudos(repo: Path) -> list[dict[str, Any]]:
    """Manifiestos tal cual (sin validar): lo justo para las guardias previas a la extraccion.
    (Este modulo no puede importar `manifiestos_fotogramas`, que lo importa a el.)"""
    directorio = repo / DIRECTORIO_MANIFIESTOS
    if not directorio.is_dir():
        return []
    docs: list[dict[str, Any]] = []
    for ruta in sorted(directorio.glob("*.yaml")):
        if ruta.name.startswith("_"):
            continue
        doc = yaml.safe_load(ruta.read_text(encoding="utf-8"))
        if isinstance(doc, dict):
            docs.append(doc)
    return docs


def _comprobar_activa(repo: Path, video_id: str, carpeta_rel: str, reemplaza_a: str | None) -> None:
    """Un video tiene exactamente una extraccion activa: extraer a OTRA carpeta (otros
    obligatorios, otra build) exige `reemplaza_a` = la activa; repetir la misma carpeta es una
    ejecucion idempotente y no lleva `reemplaza_a`."""
    docs = [d for d in _manifiestos_crudos(repo) if d.get("video_id") == video_id]
    reemplazados = {d.get("reemplaza_a") for d in docs if d.get("reemplaza_a")}
    activas = [d for d in docs if d.get("fotogramas_id") not in reemplazados]
    misma = [d for d in activas if d.get("carpeta") == carpeta_rel]
    if misma and reemplaza_a:
        raise FotogramasError(
            f"{misma[0].get('fotogramas_id')} ya es la extraccion activa de {video_id} con estos "
            "parametros: no hay nada que reemplazar"
        )
    otras = [d for d in activas if d.get("carpeta") != carpeta_rel]
    if otras and reemplaza_a is None:
        raise FotogramasError(
            f"{video_id} ya tiene la extraccion activa {otras[0].get('fotogramas_id')}; "
            "indica --reemplaza-a con ese id (exactamente una activa por video)"
        )
    if otras and reemplaza_a not in {d.get("fotogramas_id") for d in otras}:
        raise FotogramasError(
            f"--reemplaza-a {reemplaza_a}: la extraccion activa de {video_id} es "
            f"{otras[0].get('fotogramas_id')}"
        )


def _comprobar_inmutabilidad(repo: Path, carpeta_rel: str, sha_index: str) -> None:
    """Si ya hay un manifiesto para esta carpeta, el indice de hoy debe ser el suyo."""
    for doc in _manifiestos_crudos(repo):
        if doc.get("carpeta") != carpeta_rel:
            continue
        if doc.get("sha256_index") != sha_index:
            raise FotogramasError(
                f"{doc.get('fotogramas_id')} ya registra la carpeta {carpeta_rel} con otro "
                "index.jsonl: los fotogramas de un manifiesto son inmutables; revisa la build de "
                "ffmpeg antes de seguir"
            )


def _resolucion_de(png: Path) -> tuple[int, int]:
    """Ancho y alto del IHDR de un PNG (sin decodificar)."""
    with png.open("rb") as f:
        cabecera = f.read(24)
    if len(cabecera) < 24 or cabecera[:8] != b"\x89PNG\r\n\x1a\n" or cabecera[12:16] != b"IHDR":
        raise FotogramasError(f"{png.name}: no es un PNG")
    return int.from_bytes(cabecera[16:20], "big"), int.from_bytes(cabecera[20:24], "big")


def cargar_indice(carpeta: Path) -> list[Fotograma]:
    return desde_jsonl((carpeta / FICHERO_INDICE).read_text(encoding="utf-8"))


def es_referencia(texto: object) -> bool:
    return ids.es_id_de("referencia_fotograma", texto)
