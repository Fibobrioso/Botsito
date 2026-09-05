"""Ajustes de entorno: donde esta cada cosa y en que entorno corremos. Nada de negocio.

Solo se admiten las secciones `[entorno]` y `[rutas]` con claves conocidas. Una clave que coincida
con un nombre del registro de parametros es un error: los valores de negocio tienen una sola puerta.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path

ENTORNOS = ("backtest", "tester", "demo", "real")  # `real` lo estrena F33 (pre-vuelo)
CLAVES_PERMITIDAS: dict[str, frozenset[str]] = {
    "entorno": frozenset({"nombre"}),
    "rutas": frozenset({"corpus", "data", "knowledge"}),
}


class AjustesError(ValueError):
    """El fichero de ajustes contiene algo que no le corresponde."""


@dataclass(frozen=True, slots=True)
class Ajustes:
    entorno: str
    corpus: Path
    data: Path
    knowledge: Path


def cargar_ajustes(ruta: Path, nombres_de_parametros: frozenset[str] = frozenset()) -> Ajustes:
    if not ruta.exists():
        raise AjustesError(f"no existe {ruta}")
    try:
        documento = tomllib.loads(ruta.read_text(encoding="utf-8"))
    except (tomllib.TOMLDecodeError, UnicodeDecodeError) as exc:
        raise AjustesError(f"{ruta.name}: TOML invalido ({exc})") from exc
    for seccion, contenido in documento.items():
        if seccion not in CLAVES_PERMITIDAS:
            raise AjustesError(f"seccion no permitida en ajustes: [{seccion}]")
        if not isinstance(contenido, dict):
            raise AjustesError(f"[{seccion}] debe ser una tabla")
        for clave in contenido:
            if clave in nombres_de_parametros:
                raise AjustesError(
                    f"[{seccion}].{clave} es un parametro del registro: "
                    "solo puede vivir en knowledge/spec/parametros.yaml"
                )
            if clave not in CLAVES_PERMITIDAS[seccion]:
                raise AjustesError(f"clave no permitida: [{seccion}].{clave}")
    entorno = documento.get("entorno", {}).get("nombre")
    if entorno not in ENTORNOS:
        raise AjustesError(f"[entorno].nombre debe ser uno de {ENTORNOS}, no {entorno!r}")
    rutas = documento.get("rutas", {})
    for clave in CLAVES_PERMITIDAS["rutas"]:
        if clave not in rutas:
            raise AjustesError(f"falta [rutas].{clave}")
    return Ajustes(
        entorno=str(entorno),
        corpus=Path(str(rutas["corpus"])),
        data=Path(str(rutas["data"])),
        knowledge=Path(str(rutas["knowledge"])),
    )
