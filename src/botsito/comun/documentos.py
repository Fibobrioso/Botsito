"""Documentos inmutables con id por hash (evidencia, feedback, manifiestos): helpers comunes.

Cada capa conserva su `contenido_canonico` (el orden de claves forma parte del id y no puede
cambiar sin invalidar lo ya escrito); lo que se comparte es todo lo demas: normalizacion de
texto, deteccion de vacios, hash corto, recorrido de directorios con README y `_*` exentos,
cadenas de `supersede` sin ciclos y filtrado de activos.
"""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from pathlib import Path
from typing import Any, Protocol

HASH_CORTO = 8


class Supersedible(Protocol):
    @property
    def id(self) -> str: ...

    @property
    def supersede(self) -> str | None: ...


def normalizar_texto(valor: object) -> str:
    return " ".join(str(valor).split())


def vacio(valor: object) -> bool:
    """None, texto en blanco o coleccion vacia: no cuenta como campo presente."""
    if valor is None:
        return True
    if isinstance(valor, str):
        return not normalizar_texto(valor)
    if isinstance(valor, dict | list | tuple):
        return len(valor) == 0
    return False


def hash_corto(texto: str) -> str:
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()[:HASH_CORTO]


def sha256_hex(datos: bytes) -> str:
    return hashlib.sha256(datos).hexdigest()


def ficheros_de(directorio: Path, error: type[Exception], que: str) -> list[Path]:
    """`*.yaml` bajo `directorio` (recursivo), exentos README.md y `_*`. Otro fichero es error."""
    if not directorio.is_dir():
        raise error(f"no existe el directorio de {que} {directorio}")
    salida: list[Path] = []
    for ruta in sorted(p for p in directorio.rglob("*") if p.is_file()):
        if ruta.name == "README.md" or ruta.name.startswith("_"):
            continue
        if ruta.suffix != ".yaml":
            raise error(f"fichero inesperado en {que}: {ruta.name} (solo *.yaml)")
        salida.append(ruta)
    return salida


def cargar_directorio[T](
    directorio: Path,
    cargar: Callable[[Path], T],
    error: type[Exception],
    que: str,
    id_de: Callable[[T], str],
) -> list[T]:
    items = [cargar(ruta) for ruta in ficheros_de(directorio, error, que)]
    ids = [id_de(i) for i in items]
    repetidos = sorted({i for i in ids if ids.count(i) > 1})
    if repetidos:
        raise error(f"ids repetidos: {repetidos}")
    return items


def ciclos_de_supersede(sucesor: dict[str, str | None]) -> list[str]:
    """Un ciclo A->B->A desactivaria ambos sin que nadie lo pidiera (un aviso por ciclo)."""
    problemas: list[str] = []
    for inicio in sorted(sucesor):
        vistos = [inicio]
        actual = sucesor.get(inicio)
        while actual is not None and actual in sucesor:
            if actual in vistos:
                if actual == inicio and inicio == min(vistos):
                    problemas.append(f"ciclo de supersede: {' -> '.join([*vistos, actual])}")
                break
            vistos.append(actual)
            actual = sucesor.get(actual)
    return problemas


def activos[T: Supersedible](items: list[T]) -> list[T]:
    """Items no superseded por otro."""
    superseded = {i.supersede for i in items if i.supersede}
    return [i for i in items if i.id not in superseded]


def sin_vacios(doc: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in doc.items() if not vacio(v)}
