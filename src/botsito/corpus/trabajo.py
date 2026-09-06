"""Carpetas de trabajo y guardias comunes a las extracciones del corpus (transcripcion F04,
fotogramas F05). Un manifiesto inmutable registra una carpeta bajo `data/`; la carpeta base
`<nombre>` se reutiliza solo si sigue perteneciendo a la misma huella (parametros + version de la
herramienta) y al mismo video; si no, se abre `<nombre>-<hash8>` para no pisar lo que otro
manifiesto sigue verificando. Lo decide tanto la marca local de la carpeta (`huella.txt`,
`video.sha256`, que no viajan en git) como los manifiestos ya registrados (que si viajan): en un
clon sin `data/` solo el manifiesto sabe de que huella salio `<nombre>`.

Regla de actividad: un video tiene exactamente una extraccion activa por tipo. Extraer a OTRA
carpeta exige `reemplaza_a` = la activa; repetir la misma carpeta es idempotente y no lleva
`reemplaza_a`.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from botsito.comun.documentos import hash_corto
from botsito.comun.yaml_estricto import YamlError, cargar_yaml
from botsito.corpus.transcripcion import escribir_atomico

FICHERO_HUELLA = "huella.txt"
FICHERO_VIDEO_CARPETA = "video.sha256"
SUFIJO_CARPETA = re.compile(r"^-[0-9a-f]{8}$")


def leer_marca(ruta: Path) -> str:
    try:
        return ruta.read_text(encoding="utf-8").strip()
    except OSError:
        return ""


def carpeta_para(
    cv: Path, nombre: str, huella: str, sha256_video: str, registrada_ajena: bool
) -> Path:
    """`<nombre>` la primera vez; `<nombre>-<hash8>` si la base pertenece a otra huella o a
    otro video (por marca local o por manifiesto). Deja las marcas en la carpeta elegida."""
    carpeta = cv / nombre
    marca = carpeta / FICHERO_HUELLA
    marca_video = carpeta / FICHERO_VIDEO_CARPETA
    ajena = registrada_ajena or (
        carpeta.is_dir()
        and (
            (marca.exists() and leer_marca(marca) != huella)
            or (marca_video.exists() and leer_marca(marca_video) != sha256_video)
        )
    )
    if ajena:
        carpeta = cv / f"{nombre}-{hash_corto(huella + sha256_video)}"
        marca = carpeta / FICHERO_HUELLA
        marca_video = carpeta / FICHERO_VIDEO_CARPETA
    carpeta.mkdir(parents=True, exist_ok=True)
    if not marca.exists():
        escribir_atomico(marca, huella + "\n")
    if not marca_video.exists():
        escribir_atomico(marca_video, sha256_video + "\n")
    return carpeta


def manifiestos_crudos(directorio: Path, error: type[Exception]) -> list[dict[str, Any]]:
    """Manifiestos tal cual (sin validar el esquema): lo justo para las guardias previas a la
    extraccion. Un YAML ilegible es `error`, nunca un traceback."""
    if not directorio.is_dir():
        return []
    docs: list[dict[str, Any]] = []
    for ruta in sorted(directorio.glob("*.yaml")):
        if ruta.name.startswith("_"):
            continue
        try:
            doc = cargar_yaml(ruta.read_text(encoding="utf-8"))
        except YamlError as exc:
            raise error(f"{ruta.name}: {exc}") from exc
        if isinstance(doc, dict):
            docs.append(doc)
    return docs


def comprobar_activa(
    docs: list[dict[str, Any]],
    campo_id: str,
    video_id: str,
    carpeta_rel: str,
    reemplaza_a: str | None,
    error: type[Exception],
    que: str,
) -> None:
    """Ver la regla de actividad en la cabecera. `docs` son los manifiestos crudos del tipo."""
    mios = [d for d in docs if d.get("video_id") == video_id]
    reemplazados = {d.get("reemplaza_a") for d in mios if d.get("reemplaza_a")}
    activas = [d for d in mios if d.get(campo_id) not in reemplazados]
    misma = [d for d in activas if d.get("carpeta") == carpeta_rel]
    if misma and reemplaza_a:
        raise error(
            f"{misma[0].get(campo_id)} ya es la {que} activa de {video_id} con estos "
            "parametros: no hay nada que reemplazar"
        )
    otras = [d for d in activas if d.get("carpeta") != carpeta_rel]
    if otras and reemplaza_a is None:
        raise error(
            f"{video_id} ya tiene la {que} activa {otras[0].get(campo_id)}; indica "
            "--reemplaza-a con ese id (exactamente una activa por video)"
        )
    if otras and reemplaza_a not in {d.get(campo_id) for d in otras}:
        raise error(
            f"--reemplaza-a {reemplaza_a}: la {que} activa de {video_id} es "
            f"{otras[0].get(campo_id)}"
        )


def comprobar_inmutabilidad(
    docs: list[dict[str, Any]],
    campo_id: str,
    campo_hash: str,
    carpeta_rel: str,
    hash_actual: str,
    error: type[Exception],
    que: str,
) -> None:
    """Si un manifiesto ya registra esta carpeta, el contenido de hoy debe tener su hash."""
    for doc in docs:
        if doc.get("carpeta") != carpeta_rel:
            continue
        if doc.get(campo_hash) != hash_actual:
            raise error(
                f"{doc.get(campo_id)} ya registra la carpeta {carpeta_rel} con otro contenido: "
                f"la {que} de un manifiesto es inmutable; revisa versiones y parametros antes de "
                "seguir"
            )


def reemplaza_a_previo(
    doc: object, reemplaza_a: str | None, nombre: str, error: type[Exception]
) -> None:
    """Un manifiesto que ya existe no se reescribe. Repetirlo sin `reemplaza_a` es idempotente;
    pedir otro `reemplaza_a` para el, no."""
    anterior = doc.get("reemplaza_a") if isinstance(doc, dict) else None
    if reemplaza_a is not None and anterior != reemplaza_a:
        raise error(
            f"{nombre} ya existe con reemplaza_a={anterior!r}; un manifiesto es inmutable y no "
            f"se puede cambiar a {reemplaza_a!r}"
        )
