"""El reparto dev-visto (ADR-0042): material YA VISTO entra por un reparto sin sorteo y sin holdout.

El kit sortea dias CIEGOS; el camino de fidelidad (ADR-0036) sortea material etiquetado de un mes
visto y reserva la mayor parte. Ninguno sirve para lo que abril y agosto son: material de
DESARROLLO que el trader ya vio y que ya se leyo entero (`HOLDOUT-EXPOSICIONES.md`). Reservar dias
de un libro leido entero no protege nada, asi que aqui no hay sorteo, ni semilla, ni holdout:
TODOS los dias laborables de los tramos del mes son `dev`.

**SOLO ENTRA LO QUE CUMPLE LAS TRES CONDICIONES**, comprobadas antes de escribir y otra vez en
`dias_ingeribles` y en `knowledge validate`:

  1. el mes esta en `vistos.yaml` (el trader lo vio: no es ciego);
  2. su libro esta declarado en `libros.yaml` Y su lectura COMPLETA esta declarada en
     `HOLDOUT-EXPOSICIONES.md` -comprobado por el nombre del fichero del libro-;
  3. `cobertura_material` le da al mes un tramo con el `material_sha256` de ese libro.

**MISMO REGIMEN DE FICHERO QUE LOS OTROS REPARTOS.** `particiones.yaml` se recompone byte a byte
desde `cobertura_material` -si la cobertura cambia, el reparto deja de reproducirse y hay que
reconstruirlo a la vista- y va anclado por el sha de su blob en `anclas.yaml`. Los repartos del kit
y de fidelidad no se tocan, y la puerta aplica `casos_ocultos` (ADR-0041) tambien aqui: un dia
oculto no se ingiere aunque este en este reparto.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from botsito.cases.holdout import DIRECTORIO_VISTO
from botsito.cases.paquete import (
    FICHERO_ANCLAS,
    KitError,
    _dump,
    cargar_anclas,
    cargar_config,
    escribir_anclas,
    problemas_de_ancla,
)
from botsito.cases.ventanas import id_caso
from botsito.comun.historial import blob_en_arbol
from botsito.comun.yaml_estricto import YamlError, leer_yaml
from botsito.corpus.libros import LibrosError, cargar_libros

FICHERO_CONFIG_KIT = "knowledge/cases/kit/config.yaml"
FICHERO_VISTOS = "knowledge/cases/kit/vistos.yaml"
FICHERO_EXPOSICIONES = "docs/validation/HOLDOUT-EXPOSICIONES.md"
PARTICION = "dev"
# El id del artefacto ES el mes: un mes, un libro, un reparto.
MES = re.compile(r"^\d{4}-\d{2}$", re.ASCII)
COMANDO = "casos visto --mes"


class VistoError(ValueError):
    """El material no cumple las condiciones del reparto dev-visto, o su reparto no es el que es."""


def meses_vistos(repo: Path) -> set[str]:
    try:
        doc = leer_yaml(repo / FICHERO_VISTOS)
    except (OSError, YamlError) as exc:
        raise VistoError(f"{FICHERO_VISTOS}: {exc}") from exc
    entradas = doc.get("meses") if isinstance(doc, dict) else None
    return {str(e.get("mes")) for e in entradas or [] if isinstance(e, dict)}


def requisitos(repo: Path, mes: str) -> list[str]:
    """Por que `mes` NO puede entrar por dev-visto. Lista vacia: puede."""
    if not MES.match(mes):
        return [f"{mes!r} no es un mes AAAA-MM"]
    problemas: list[str] = []
    try:
        vistos = meses_vistos(repo)
    except VistoError as exc:
        return [str(exc)]
    if mes not in vistos:
        problemas.append(
            f"{mes} no esta en {FICHERO_VISTOS}: un mes que el trader no ha visto es ciego y va "
            f"por el kit, no por dev-visto (ADR-0042)"
        )
    try:
        config = cargar_config(repo / FICHERO_CONFIG_KIT)
    except (KitError, OSError) as exc:
        return [*problemas, str(exc)]
    shas = sorted(s for s, m in config.materiales.items() if m == mes)
    if not config.cobertura.get(mes) or len(shas) != 1:
        problemas.append(
            f"{mes}: cobertura_material no le da un tramo con UN `material_sha256`: sin el libro "
            f"del mes declarado no se sabe que material entra"
        )
        return problemas
    try:
        libros = cargar_libros(repo)
    except LibrosError as exc:
        return [*problemas, str(exc)]
    sha = shas[0]
    if sha not in libros:
        problemas.append(f"{mes}: el libro {sha[:12]}... no esta declarado en libros.yaml")
        return problemas
    fichero = Path(_fichero_del_libro(repo, sha)).name
    try:
        exposiciones = (repo / FICHERO_EXPOSICIONES).read_text(encoding="utf-8")
    except OSError:
        exposiciones = ""
    if not fichero or fichero not in exposiciones:
        problemas.append(
            f"{mes}: la lectura completa de su libro no esta declarada en {FICHERO_EXPOSICIONES} "
            f"(no nombra el fichero): dev-visto es para material ya leido entero (ADR-0042)"
        )
    return problemas


def _fichero_del_libro(repo: Path, sha: str) -> str:
    try:
        doc = leer_yaml(repo / "knowledge" / "corpus" / "libros.yaml")
    except (OSError, YamlError):
        return ""
    entrada = (doc.get("libros") or {}).get(sha) if isinstance(doc, dict) else None
    return str(entrada.get("fichero", "")) if isinstance(entrada, dict) else ""


def _laborables(tramos: tuple[tuple[str, str], ...]) -> list[date]:
    dias: list[date] = []
    for desde, hasta in tramos:
        d, fin = date.fromisoformat(desde), date.fromisoformat(hasta)
        while d <= fin:
            if d.weekday() < 5:
                dias.append(d)
            d += timedelta(days=1)
    return dias


def construir(repo: Path, mes: str) -> str:
    """El `particiones.yaml` del mes, como TEXTO. Lanza si el mes no cumple las condiciones."""
    problemas = requisitos(repo, mes)
    if problemas:
        raise VistoError("; ".join(problemas))
    config = cargar_config(repo / FICHERO_CONFIG_KIT)
    (sha,) = [s for s, m in config.materiales.items() if m == mes]
    dias = _laborables(config.cobertura[mes])
    doc: dict[str, Any] = {
        "artefacto": mes,
        "material_sha256": sha,
        "cupos": {PARTICION: len(dias)},
        "asignacion": {id_caso(config.simbolo, d): PARTICION for d in dias},
    }
    return _dump(doc)


def escribir(repo: Path, mes: str, texto: str) -> Path:
    """Escribe el reparto y lo ANCLA en el mismo paso. No sobreescribe."""
    ruta = repo / DIRECTORIO_VISTO / mes / "particiones.yaml"
    if ruta.exists():
        raise VistoError(f"{ruta.relative_to(repo).as_posix()} ya existe: no se sobreescribe")
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(texto, encoding="utf-8", newline="\n")
    anclas = cargar_anclas(repo, DIRECTORIO_VISTO, MES)
    blob = blob_en_arbol(repo, f"{DIRECTORIO_VISTO}/{mes}/particiones.yaml")
    if blob is None:
        raise VistoError("git no puede calcular el blob del reparto: no se ancla")
    anclas[mes] = {"particiones.yaml": blob}
    escribir_anclas(repo, anclas, DIRECTORIO_VISTO)
    return ruta


def artefactos(repo: Path) -> list[str]:
    base = repo / DIRECTORIO_VISTO
    if not base.is_dir():
        return []
    return sorted(p.parent.name for p in base.glob("*/particiones.yaml"))


def asignacion(repo: Path, mes: str) -> Mapping[str, str]:
    doc = leer_yaml(repo / DIRECTORIO_VISTO / mes / "particiones.yaml")
    crudo = doc.get("asignacion") if isinstance(doc, dict) else None
    return crudo if isinstance(crudo, dict) else {}


def problemas(repo: Path) -> list[str]:
    """Para `knowledge validate` y para `dias_ingeribles`: condiciones, reproduccion y ancla.

    SIN `data/`: el reparto sale entero de `cobertura_material`, asi que se comprueba siempre.
    """
    lista = artefactos(repo)
    if not lista:
        return []
    salida: list[str] = []
    try:
        anclas = cargar_anclas(repo, DIRECTORIO_VISTO, MES)
    except KitError as exc:
        salida.append(str(exc))
        anclas = {}
    for mes in lista:
        if not MES.match(mes):
            salida.append(f"{DIRECTORIO_VISTO}/{mes}: el artefacto se llama como su mes, AAAA-MM")
            continue
        ruta = repo / DIRECTORIO_VISTO / mes / "particiones.yaml"
        try:
            esperado = construir(repo, mes)
        except (VistoError, KitError) as exc:
            salida.append(f"{mes}: {exc}")
            continue
        if ruta.read_text(encoding="utf-8") != esperado:
            salida.append(
                f"{mes}/particiones.yaml: difiere de lo que se genera hoy desde "
                f"cobertura_material. Si la cobertura cambio, se reconstruye a la vista con "
                f"`botsito {COMANDO} {mes}` y se re-ancla (ADR-0042)"
            )
        salida += problemas_de_ancla(repo, mes, anclas, DIRECTORIO_VISTO, COMANDO)
    return salida


__all__ = [
    "COMANDO",
    "DIRECTORIO_VISTO",
    "FICHERO_ANCLAS",
    "PARTICION",
    "VistoError",
    "artefactos",
    "asignacion",
    "construir",
    "escribir",
    "meses_vistos",
    "problemas",
    "requisitos",
]
