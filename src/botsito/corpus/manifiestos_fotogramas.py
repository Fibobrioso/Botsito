"""Manifiestos INMUTABLES de fotogramas (F05, ADR-0008): carga, esquema, activos, comprobacion.

Un manifiesto por extraccion en `knowledge/corpus/fotogramas/<id>.yaml` (versionado; el
historial de git lo vigila como a la evidencia). `reemplaza_a` enlaza una re-extraccion con la
anterior; hay exactamente una activa por video. `comprobar` recomputa contra `data/`: el
`index.jsonl` debe tener el sha256 del manifiesto y lo que el manifiesto afirma (recuentos,
ultimo pts, huecos, extra) se recalcula desde el indice; los ficheros extra y una muestra
determinista de regulares se verifican por hash. `referencias_conocidas` es lo que F07 puede
citar: `fr-<id>/<t_ms>` de TODOS los manifiestos (activos o reemplazados: un item que cito uno
reemplazado sigue siendo valido) mas las rutas del corpus con papel `material_adicional`; lo
heredado de Bot v2 queda fuera.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from botsito.comun import ids
from botsito.comun.documentos import activos as _activos
from botsito.comun.documentos import cargar_directorio, ciclos_de_supersede, sha256_hex
from botsito.comun.yaml_estricto import YamlError, cargar_yaml
from botsito.corpus.fotogramas import (
    CARPETA_DATOS,
    DIRECTORIO_MANIFIESTOS,
    FICHERO_INDICE,
    NOMBRE,
    SCHEMA_VERSION,
    Fotograma,
    FotogramasError,
    Obligatorio,
    desde_jsonl,
    huecos,
    referencia,
)
from botsito.corpus.transcripcion import formato_ms

_SUFIJO_CARPETA = re.compile(r"^-[0-9a-f]{8}$")
MUESTRA_REGULARES = 20  # no-negocio: fotogramas regulares verificados por hash en `check`

CAMPOS_OBLIGATORIOS = (
    "schema_version",
    "fotogramas_id",
    "video_id",
    "fichero_video",
    "sha256_video",
    "duracion_video_s",
    "resolucion",
    "ffmpeg",
    "parametros",
    "carpeta",
    "n_fotogramas",
    "n_regulares",
    "ultimo_pts_ms",
    "hueco_fotogramas_ms",
    "huecos",
    "extra",
    "sha256_index",
    "generado_el",
)
CAMPOS_OPCIONALES = ("reemplaza_a",)
PAPEL_CITABLE = "material_adicional"


class ManifiestoFotogramasError(ValueError):
    """El manifiesto no cumple su esquema o no coincide con el disco."""


@dataclass(frozen=True, slots=True)
class Fotogramas:
    id: str
    video_id: str
    carpeta: str
    sha256_index: str
    n_fotogramas: int
    ultimo_pts_ms: int
    extra_ms: tuple[int, ...]
    supersede: str | None  # reemplaza_a (mismo nombre que evidencia/feedback para `activos`)
    doc: dict[str, Any]

    def referencias(self) -> set[str]:
        """`fr-<id>/<t_ms>` de cada regular (un segundo entero hasta el ultimo pts) y extra."""
        regulares = range(0, self.ultimo_pts_ms // 1000 * 1000 + 1, 1000)
        return {referencia(self.id, t) for t in regulares} | {
            referencia(self.id, t) for t in self.extra_ms
        }


def cargar_manifiesto(ruta: Path) -> Fotogramas:
    try:
        doc = cargar_yaml(ruta.read_text(encoding="utf-8"))
    except YamlError as exc:
        raise ManifiestoFotogramasError(f"{ruta.name}: {exc}") from exc
    if not isinstance(doc, dict):
        raise ManifiestoFotogramasError(f"{ruta.name}: no es un mapa")
    return validar(doc, ruta.name)


def _entero(v: object) -> bool:
    return isinstance(v, int) and not isinstance(v, bool) and v >= 0


def _hex(v: object) -> bool:
    return isinstance(v, str) and len(v) == 64 and all(c in "0123456789abcdef" for c in v)


def validar(doc: dict[str, Any], origen: str) -> Fotogramas:
    faltan = [c for c in CAMPOS_OBLIGATORIOS if c not in doc]
    if faltan:
        raise ManifiestoFotogramasError(f"{origen}: faltan campos {faltan}")
    ajenos = sorted(set(doc) - set(CAMPOS_OBLIGATORIOS) - set(CAMPOS_OPCIONALES))
    if ajenos:
        raise ManifiestoFotogramasError(f"{origen}: campos desconocidos {ajenos}")
    if doc["schema_version"] != SCHEMA_VERSION:
        raise ManifiestoFotogramasError(f"{origen}: schema_version no soportada")
    fid = doc["fotogramas_id"]
    if not ids.es_id_de("fotogramas", fid):
        raise ManifiestoFotogramasError(f"{origen}: fotogramas_id invalido {fid!r}")
    if origen != "manifiesto" and Path(origen).stem != fid:
        raise ManifiestoFotogramasError(f"{origen}: el fichero debe llamarse {fid}.yaml")
    for c in ("video_id", "fichero_video", "carpeta", "ffmpeg", "generado_el"):
        if not isinstance(doc[c], str) or not doc[c].strip():
            raise ManifiestoFotogramasError(f"{origen}: {c} debe ser texto no vacio")
    for c in ("sha256_video", "sha256_index"):
        if not _hex(doc[c]):
            raise ManifiestoFotogramasError(f"{origen}: {c} invalido")
    if fid != f"fr-{doc['video_id']}-{doc['sha256_index'][:8]}":
        raise ManifiestoFotogramasError(
            f"{origen}: el id debe ser fr-{doc['video_id']}-<8 primeros de sha256_index>"
        )
    esperada = f"{CARPETA_DATOS}/{doc['video_id']}/{NOMBRE}"
    carpeta = str(doc["carpeta"])
    sufijo = carpeta[len(esperada) :] if carpeta.startswith(esperada) else None
    if sufijo is None or (sufijo and not _SUFIJO_CARPETA.match(sufijo)):
        raise ManifiestoFotogramasError(
            f"{origen}: carpeta {carpeta!r} debe ser {esperada!r} (o con sufijo -<huella8>)"
        )
    for c in ("n_fotogramas", "n_regulares", "ultimo_pts_ms", "hueco_fotogramas_ms"):
        if not _entero(doc[c]):
            raise ManifiestoFotogramasError(f"{origen}: {c} debe ser entero >= 0")
    if doc["n_fotogramas"] < 1 or doc["n_regulares"] < 1:
        raise ManifiestoFotogramasError(f"{origen}: una extraccion sin fotogramas no se registra")
    d = doc["duracion_video_s"]
    if isinstance(d, bool) or not isinstance(d, int | float) or d <= 0:
        raise ManifiestoFotogramasError(f"{origen}: duracion_video_s debe ser un numero > 0")
    if doc["ultimo_pts_ms"] > d * 1000 + 1000:
        raise ManifiestoFotogramasError(f"{origen}: ultimo_pts_ms supera la duracion del video")
    res = doc["resolucion"]
    if (
        not isinstance(res, dict)
        or set(res) != {"ancho", "alto"}
        or not all(_entero(res[k]) and res[k] > 0 for k in res)
    ):
        raise ManifiestoFotogramasError(f"{origen}: resolucion debe tener ancho y alto > 0")
    if not isinstance(doc["parametros"], dict) or not isinstance(
        doc["parametros"].get("seleccion"), str
    ):
        raise ManifiestoFotogramasError(f"{origen}: parametros.seleccion ausente")
    for c in ("huecos", "extra"):
        if not isinstance(doc[c], list):
            raise ManifiestoFotogramasError(f"{origen}: {c} debe ser una lista")
    for h in doc["huecos"]:
        bien = (
            isinstance(h, dict)
            and set(h) == {"desde_ms", "hasta_ms", "ms"}
            and all(_entero(h[k]) for k in h)
            and h["desde_ms"] < h["hasta_ms"]
            and h["ms"] == h["hasta_ms"] - h["desde_ms"]
        )
        if not bien:
            raise ManifiestoFotogramasError(f"{origen}: hueco invalido {h!r}")
    extra_ms: list[int] = []
    for e in doc["extra"]:
        bien = (
            isinstance(e, dict)
            and set(e) == {"t_ms", "pts_ms", "sha256"}
            and _entero(e["t_ms"])
            and _entero(e["pts_ms"])
            and e["pts_ms"] >= e["t_ms"]
            and e["t_ms"] % 1000 != 0
            and _hex(e["sha256"])
        )
        if not bien:
            raise ManifiestoFotogramasError(f"{origen}: extra invalido {e!r}")
        extra_ms.append(int(e["t_ms"]))
    if len(set(extra_ms)) != len(extra_ms):
        raise ManifiestoFotogramasError(f"{origen}: extra repetido")
    if doc["n_fotogramas"] != doc["n_regulares"] + len(extra_ms):
        raise ManifiestoFotogramasError(f"{origen}: n_fotogramas != n_regulares + extra")
    if "reemplaza_a" in doc and not ids.es_id_de("fotogramas", doc["reemplaza_a"]):
        raise ManifiestoFotogramasError(f"{origen}: reemplaza_a debe ser un fotogramas_id")
    return Fotogramas(
        fid,
        str(doc["video_id"]),
        carpeta,
        str(doc["sha256_index"]),
        int(doc["n_fotogramas"]),
        int(doc["ultimo_pts_ms"]),
        tuple(sorted(extra_ms)),
        doc.get("reemplaza_a"),
        doc,
    )


def cargar_todos(repo: Path) -> list[Fotogramas]:
    carpeta = repo / DIRECTORIO_MANIFIESTOS
    if not carpeta.is_dir():
        return []
    items = cargar_directorio(
        carpeta,
        cargar_manifiesto,
        ManifiestoFotogramasError,
        DIRECTORIO_MANIFIESTOS,
        lambda t: t.id,
    )
    conocidos = {t.id: t for t in items}
    for t in items:
        if t.supersede and t.supersede not in conocidos:
            raise ManifiestoFotogramasError(f"{t.id}: reemplaza_a {t.supersede} no existe")
        if t.supersede == t.id:
            raise ManifiestoFotogramasError(f"{t.id}: no puede reemplazarse a si mismo")
        if t.supersede and conocidos[t.supersede].video_id != t.video_id:
            raise ManifiestoFotogramasError(
                f"{t.id}: reemplaza_a {t.supersede} es de otro video "
                f"({conocidos[t.supersede].video_id})"
            )
    for problema in ciclos_de_supersede({t.id: t.supersede for t in items}):
        raise ManifiestoFotogramasError(problema)
    vivos = activos(items)
    por_video: dict[str, list[str]] = {}
    for t in vivos:
        por_video.setdefault(t.video_id, []).append(t.id)
    for video_id, lista in sorted(por_video.items()):
        if len(lista) > 1:
            raise ManifiestoFotogramasError(
                f"{video_id} tiene {len(lista)} extracciones activas {lista}: exactamente una "
                "por video (marca reemplaza_a)"
            )
    return items


def activos(items: list[Fotogramas]) -> list[Fotogramas]:
    return _activos(items)


def activa_de(items: list[Fotogramas], video_id: str) -> Fotogramas:
    vivas = [t for t in activos(items) if t.video_id == video_id]
    if not vivas:
        raise ManifiestoFotogramasError(f"no hay extraccion de fotogramas activa para {video_id}")
    return vivas[0]


def carpeta_de(carpeta_datos: Path, t: Fotogramas) -> Path:
    return carpeta_datos / Path(t.carpeta)


def _muestra(fotogramas: list[Fotograma], n: int) -> list[Fotograma]:
    """`n` regulares repartidos de forma determinista (mismo indice -> misma muestra)."""
    regulares = [f for f in fotogramas if f.origen == "regular"]
    if len(regulares) <= n:
        return regulares
    paso = len(regulares) / n
    return [regulares[int(i * paso)] for i in range(n)]


def comprobar(
    items: list[Fotogramas], carpeta_datos: Path, muestra: int = MUESTRA_REGULARES
) -> tuple[list[str], list[str]]:
    """(errores, avisos). Carpeta ausente = aviso (los datos no viajan en git); indice alterado,
    recuentos que no cuadran, fichero ausente o con otro tamano, hash distinto = error."""
    errores: list[str] = []
    avisos: list[str] = []
    for t in items:
        carpeta = carpeta_de(carpeta_datos, t)
        indice = carpeta / FICHERO_INDICE
        if not indice.is_file():
            avisos.append(f"{t.id}: {FICHERO_INDICE} no esta en esta maquina ({carpeta})")
            continue
        datos = indice.read_bytes()
        if sha256_hex(datos) != t.sha256_index:
            errores.append(f"{t.id}: {FICHERO_INDICE} alterado (sha256 distinto del manifiesto)")
            continue
        try:
            fotogramas = desde_jsonl(datos.decode("utf-8"))
        except (FotogramasError, UnicodeDecodeError) as exc:
            errores.append(f"{t.id}: {FICHERO_INDICE} no se puede leer ({exc})")
            continue
        errores += [f"{t.id}: {e}" for e in _recomputar(t.doc, fotogramas)]
        for f in fotogramas:
            ruta = carpeta / f.fichero
            if not ruta.is_file():
                errores.append(f"{t.id}: falta {f.fichero}")
            elif ruta.stat().st_size != f.bytes:
                errores.append(f"{t.id}: {f.fichero} tiene otro tamano")
        por_hash = [f for f in fotogramas if f.origen == "obligatorio"] + _muestra(
            fotogramas, muestra
        )
        for f in por_hash:
            ruta = carpeta / f.fichero
            if ruta.is_file() and sha256_hex(ruta.read_bytes()) != f.sha256:
                errores.append(f"{t.id}: {f.fichero} alterado (sha256 distinto del indice)")
    return errores, avisos


def _recomputar(doc: dict[str, Any], fotogramas: list[Fotograma]) -> list[str]:
    """Lo que el manifiesto afirma sobre el indice se recalcula desde el indice."""
    fallos: list[str] = []
    if len(fotogramas) != doc["n_fotogramas"]:
        fallos.append(f"{len(fotogramas)} fotogramas, el manifiesto dice {doc['n_fotogramas']}")
    regulares = sum(1 for f in fotogramas if f.origen == "regular")
    if regulares != doc["n_regulares"]:
        fallos.append(f"{regulares} regulares, el manifiesto dice {doc['n_regulares']}")
    ultimo = max(f.pts_ms for f in fotogramas)
    if ultimo != doc["ultimo_pts_ms"]:
        fallos.append(f"ultimo pts {ultimo}, el manifiesto dice {doc['ultimo_pts_ms']}")
    esperados = huecos(fotogramas, int(doc["hueco_fotogramas_ms"]))
    if esperados != doc["huecos"]:
        fallos.append(f"huecos {esperados}, el manifiesto dice {doc['huecos']}")
    extra = [
        {"t_ms": f.t_ms, "pts_ms": f.pts_ms, "sha256": f.sha256}
        for f in fotogramas
        if f.origen == "obligatorio"
    ]
    if extra != doc["extra"]:
        fallos.append("extra no coincide con los obligatorios del indice")
    return fallos


def comprobar_obligatorios(items: list[Fotogramas], obligatorios: list[Obligatorio]) -> list[str]:
    """Cada obligatorio existe en la extraccion activa de su video (regular o extra)."""
    fallos: list[str] = []
    vivos = {t.video_id: t for t in activos(items)}
    for o in obligatorios:
        t = vivos.get(o.video_id)
        if t is None:
            fallos.append(f"obligatorio {o.video_id} {formato_ms(o.t_ms)}: sin extraccion activa")
            continue
        if referencia(t.id, o.t_ms) not in t.referencias():
            fallos.append(
                f"obligatorio {o.video_id} {formato_ms(o.t_ms)}: no esta en {t.id} "
                "(re-extrae con `corpus frames extract`)"
            )
    return fallos


def referencias_conocidas(
    items: list[Fotogramas], manifiesto_corpus: dict[str, Any] | None
) -> set[str]:
    """Lo que un item de evidencia puede poner en `fotogramas` (F07): referencias `fr-*/t_ms`
    de todos los manifiestos y rutas del corpus con papel `material_adicional`. Lo heredado de
    Bot v2 (`heredado_v2`) no se cita."""
    salida: set[str] = set()
    for t in items:
        salida |= t.referencias()
    for f in (manifiesto_corpus or {}).get("ficheros") or []:
        if isinstance(f, dict) and f.get("papel") == PAPEL_CITABLE:
            salida.add(str(f.get("ruta")))
    return salida
