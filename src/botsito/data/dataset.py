"""Datasets congelados de velas M1 (F15, ADR-0005): ficheros por mes + manifiesto inmutable.

Disposicion bajo la carpeta de datos (`[rutas].data`, ignorada por git salvo `manifests/`):

    data/ohlc/<dataset_id>/<SIMBOLO>_M1_<AAAA-MM>.csv     (no versionado)
    data/manifests/<dataset_id>.yaml                       (versionado, INMUTABLE)

`dataset_id = <nombre>-<8 hex>`: el sufijo es el sha256 de los sha256 de los ficheros, en orden,
como los ids de evidencia. Bytes distintos son un dataset distinto; el manifiesto viejo no se
toca (`reemplaza_a` enlaza al nuevo con el anterior). El historial de git de `data/manifests/`
se vigila como el de la evidencia. `comprobar()` compara el disco con el manifiesto (tamanos y,
si se pide, hashes), como `corpus check`.

Esta capa no importa el registro ni el historial (son hermanos): la CLI les pasa lo que necesitan.
"""

from __future__ import annotations

import hashlib
import re
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import yaml

from botsito.data.agregacion import huecos
from botsito.data.dukascopy import (
    DECODIFICADOR_VERSION,
    ESCALA_VOLUMEN,
    FILTRO_PLANAS,
    HUSO_DATOS,
    PROVEEDOR,
    TIPO_PRECIO,
    DiaDescargado,
    descargar_dia,
)
from botsito.data.velas import a_datetime, escribir_csv, formato_ts, leer_fichero
from botsito.domain.velas import SerieVelas, Vela
from botsito.yaml_estricto import YamlError, cargar_yaml

SCHEMA_VERSION = 1
DIRECTORIO_MANIFIESTOS = "data/manifests"
CARPETA_OHLC = "ohlc"
_NOMBRE = re.compile(r"^[a-z0-9][a-z0-9-]{1,47}$", re.ASCII)
_ID = re.compile(r"^[a-z0-9][a-z0-9-]{1,47}-[0-9a-f]{8}$", re.ASCII)
_SIMBOLO = re.compile(r"^[A-Z0-9]{3,12}$", re.ASCII)
_SHA256 = re.compile(r"^[0-9a-f]{64}$", re.ASCII)
HUECO_RESENABLE_MIN = 60  # huecos menores se cuentan; mayores se listan (fines de semana, festivos)
CAMPOS_OBLIGATORIOS = (
    "schema_version",
    "dataset_id",
    "proveedor",
    "tipo_precio",
    "simbolo",
    "simbolo_proveedor",
    "escala",
    "escala_volumen",
    "huso_datos",
    "periodo_min",
    "filtro_planas",
    "decodificador_version",
    "desde",
    "hasta",
    "descargado_el",
    "ficheros",
    "dias",
    "huecos",
)
CAMPOS_OPCIONALES = ("reemplaza_a", "generado_por")


class DatasetError(ValueError):
    """El dataset o su manifiesto no cumplen el esquema o no coinciden con el disco."""


@dataclass(frozen=True, slots=True)
class Congelado:
    manifiesto: dict[str, Any]
    ruta_manifiesto: Path
    ficheros: tuple[Path, ...]


def _sha256(datos: bytes) -> str:
    return hashlib.sha256(datos).hexdigest()


def dias_entre(desde: date, hasta: date) -> list[date]:
    if hasta < desde:
        raise DatasetError(f"rango invalido: {desde} > {hasta}")
    return [desde + timedelta(days=i) for i in range((hasta - desde).days + 1)]


def validar_id(dataset_id: str) -> str:
    if not _ID.match(dataset_id):
        raise DatasetError(f"dataset_id {dataset_id!r} invalido (nombre-hash8)")
    return dataset_id


def ruta_manifiesto(repo: Path, dataset_id: str) -> Path:
    return repo / DIRECTORIO_MANIFIESTOS / f"{validar_id(dataset_id)}.yaml"


def id_desde_hashes(nombre: str, hashes: list[str]) -> str:
    sufijo = _sha256("\n".join(hashes).encode("ascii"))[:8]
    return f"{nombre}-{sufijo}"


def congelar(
    repo: Path,
    carpeta_datos: Path,
    nombre: str,
    simbolo: str,
    escala: int,
    desde: date,
    hasta: date,
    descarga: Callable[[str], bytes | None],
    hoy: date,
    reemplaza_a: str | None = None,
    generado_por: str | None = None,
    descargar: Callable[..., DiaDescargado] = descargar_dia,
) -> Congelado:
    """Descarga el rango, escribe un CSV por mes y el manifiesto. Nunca sobreescribe.

    `hasta` debe ser anterior a `hoy`: el dia en curso llegaria parcial y quedaria congelado.
    """
    if not _NOMBRE.match(nombre):
        raise DatasetError(f"nombre {nombre!r} invalido (minusculas, digitos y guiones, 2-48)")
    if not _SIMBOLO.match(simbolo):
        raise DatasetError(f"simbolo {simbolo!r} invalido (mayusculas y digitos)")
    if isinstance(escala, bool) or escala <= 0:
        raise DatasetError("escala debe ser un entero positivo (puntos por unidad)")
    if hasta >= hoy:
        raise DatasetError(
            f"hasta ({hasta}) debe ser anterior a hoy ({hoy}): el dia en curso es parcial"
        )
    if reemplaza_a is not None and not ruta_manifiesto(repo, reemplaza_a).exists():
        raise DatasetError(f"reemplaza_a {reemplaza_a!r} no existe")
    por_mes: dict[str, list[Vela]] = {}
    ausentes: list[str] = []
    sin_datos: list[str] = []
    registros = descartadas = presentes = dudosas = planas_laborables = 0
    for dia in dias_entre(desde, hasta):
        resultado = descargar(simbolo, dia, descarga)
        if not resultado.presente:
            ausentes.append(dia.isoformat())
            continue
        presentes += 1
        registros += resultado.registros
        descartadas += resultado.descartadas
        dudosas += resultado.volumen_cero_no_planas
        planas_laborables += resultado.descartadas_en_laborable
        if not resultado.velas:
            sin_datos.append(dia.isoformat())
            continue
        por_mes.setdefault(dia.strftime("%Y-%m"), []).extend(resultado.velas)
    todas: list[Vela] = [v for mes in sorted(por_mes) for v in por_mes[mes]]
    if not todas:
        raise DatasetError("el rango no contiene ninguna vela: no se congela un dataset vacio")
    contenidos: list[tuple[str, bytes, list[Vela]]] = []
    for mes in sorted(por_mes):
        nombre_fichero = f"{simbolo}_M1_{mes}.csv"
        contenidos.append(
            (nombre_fichero, escribir_csv(por_mes[mes]).encode("utf-8"), por_mes[mes])
        )
    dataset_id = id_desde_hashes(nombre, [_sha256(texto) for _, texto, _ in contenidos])
    manifiesto_ruta = ruta_manifiesto(repo, dataset_id)
    carpeta = carpeta_datos / CARPETA_OHLC / dataset_id
    if manifiesto_ruta.exists() or carpeta.exists():
        raise DatasetError(f"el dataset {dataset_id} ya existe con este mismo contenido")
    carpeta.mkdir(parents=True)
    ficheros: list[dict[str, Any]] = []
    rutas: list[Path] = []
    for nombre_fichero, texto, velas_mes in contenidos:
        ruta = carpeta / nombre_fichero
        ruta.write_bytes(texto)
        rutas.append(ruta)
        ficheros.append(
            {
                "ruta": f"{CARPETA_OHLC}/{dataset_id}/{nombre_fichero}",
                "bytes": len(texto),
                "sha256": _sha256(texto),
                "filas": len(velas_mes),
                "primera": formato_ts(velas_mes[0].inicio),
                "ultima": formato_ts(velas_mes[-1].inicio),
            }
        )
    todos_huecos = huecos(todas)
    manifiesto: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_id": dataset_id,
        "proveedor": PROVEEDOR,
        "tipo_precio": TIPO_PRECIO,
        "simbolo": simbolo,
        "simbolo_proveedor": simbolo,
        "escala": escala,
        "escala_volumen": ESCALA_VOLUMEN,
        "huso_datos": HUSO_DATOS,
        "periodo_min": 1,
        "filtro_planas": FILTRO_PLANAS,
        "decodificador_version": DECODIFICADOR_VERSION,
        "desde": desde.isoformat(),
        "hasta": hasta.isoformat(),
        "descargado_el": hoy.isoformat(),
        "ficheros": ficheros,
        "dias": {
            "presentes": presentes,
            "ausentes": ausentes,
            "sin_datos": sin_datos,
            "registros": registros,
            "descartadas_planas_sin_volumen": descartadas,
            "descartadas_en_laborable": planas_laborables,
            "volumen_cero_no_planas": dudosas,
            "velas": len(todas),
        },
        "huecos": {
            "menores_de_60_min": sum(1 for h in todos_huecos if h.minutos < HUECO_RESENABLE_MIN),
            "mayores": [
                {"desde": formato_ts(h.desde), "hasta": formato_ts(h.hasta), "minutos": h.minutos}
                for h in todos_huecos
                if h.minutos >= HUECO_RESENABLE_MIN
            ],
        },
    }
    if reemplaza_a:
        manifiesto["reemplaza_a"] = reemplaza_a
    if generado_por:
        manifiesto["generado_por"] = generado_por
    escribir_manifiesto(manifiesto, manifiesto_ruta)
    return Congelado(manifiesto, manifiesto_ruta, tuple(rutas))


def escribir_manifiesto(manifiesto: dict[str, Any], ruta: Path) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    texto = yaml.safe_dump(manifiesto, allow_unicode=True, sort_keys=True, width=100)
    ruta.write_text(
        "# GENERADO por `botsito data download`. INMUTABLE: no editar; un cambio es otro dataset.\n"
        + texto,
        encoding="utf-8",
        newline="\n",
    )


def cargar_manifiesto(ruta: Path) -> dict[str, Any]:
    if not ruta.exists():
        raise DatasetError(f"no existe {ruta}")
    try:
        doc = cargar_yaml(ruta.read_text(encoding="utf-8"))
    except YamlError as exc:
        raise DatasetError(f"{ruta.name}: {exc}") from exc
    if not isinstance(doc, dict):
        raise DatasetError(f"{ruta.name}: no es un mapa")
    return validar_manifiesto(doc, ruta.name)


def _texto(doc: dict[str, Any], campo: str, origen: str) -> str:
    v = doc.get(campo)
    if not isinstance(v, str) or not v.strip():
        raise DatasetError(f"{origen}: {campo} debe ser texto no vacio")
    return v


def _entero_positivo(doc: dict[str, Any], campo: str, origen: str) -> int:
    v = doc.get(campo)
    if isinstance(v, bool) or not isinstance(v, int) or v <= 0:
        raise DatasetError(f"{origen}: {campo} debe ser un entero positivo")
    return v


def validar_manifiesto(doc: dict[str, Any], origen: str) -> dict[str, Any]:
    faltan = [c for c in CAMPOS_OBLIGATORIOS if c not in doc]
    if faltan:
        raise DatasetError(f"{origen}: faltan campos {faltan}")
    desconocidos = sorted(set(doc) - set(CAMPOS_OBLIGATORIOS) - set(CAMPOS_OPCIONALES))
    if desconocidos:
        raise DatasetError(f"{origen}: campos desconocidos {desconocidos}")
    if doc["schema_version"] != SCHEMA_VERSION:
        raise DatasetError(f"{origen}: schema_version {doc['schema_version']!r} no soportada")
    dataset_id = _texto(doc, "dataset_id", origen)
    if not _ID.match(dataset_id):
        raise DatasetError(f"{origen}: dataset_id invalido")
    if origen != "manifiesto" and Path(origen).stem != dataset_id:
        raise DatasetError(f"{origen}: el fichero debe llamarse {dataset_id}.yaml")
    for campo in ("proveedor", "tipo_precio", "simbolo", "simbolo_proveedor", "huso_datos"):
        _texto(doc, campo, origen)
    if doc["huso_datos"] != HUSO_DATOS:
        raise DatasetError(f"{origen}: huso_datos debe ser {HUSO_DATOS}")
    for campo in ("desde", "hasta", "descargado_el"):
        try:
            date.fromisoformat(_texto(doc, campo, origen))
        except ValueError as exc:
            raise DatasetError(f"{origen}: {campo} no es una fecha AAAA-MM-DD") from exc
    if doc["hasta"] < doc["desde"]:
        raise DatasetError(f"{origen}: hasta anterior a desde")
    for campo in (
        "escala",
        "escala_volumen",
        "periodo_min",
        "filtro_planas",
        "decodificador_version",
    ):
        _entero_positivo(doc, campo, origen)
    ficheros = doc["ficheros"]
    if not isinstance(ficheros, list) or not ficheros:
        raise DatasetError(f"{origen}: ficheros debe ser una lista no vacia")
    rutas: set[str] = set()
    hashes: list[str] = []
    for f in ficheros:
        if not isinstance(f, dict):
            raise DatasetError(f"{origen}: entrada de fichero invalida")
        ruta = f.get("ruta")
        if (
            not isinstance(ruta, str)
            or not ruta
            or ruta in rutas
            or ".." in ruta
            or ruta[0] in "/\\"
        ):
            raise DatasetError(f"{origen}: ruta de fichero invalida o repetida {ruta!r}")
        rutas.add(ruta)
        if not isinstance(f.get("sha256"), str) or not _SHA256.match(f["sha256"]):
            raise DatasetError(f"{origen}: sha256 invalido en {ruta}")
        hashes.append(f["sha256"])
        for campo in ("bytes", "filas"):
            v = f.get(campo)
            if isinstance(v, bool) or not isinstance(v, int) or v < 0:
                raise DatasetError(f"{origen}: {campo} invalido en {ruta}")
    nombre = dataset_id.rsplit("-", 1)[0]
    if id_desde_hashes(nombre, hashes) != dataset_id:
        raise DatasetError(f"{origen}: el sufijo del dataset_id no coincide con los hashes")
    if not isinstance(doc["dias"], dict) or not isinstance(doc["huecos"], dict):
        raise DatasetError(f"{origen}: dias y huecos deben ser mapas")
    if "reemplaza_a" in doc and (
        not isinstance(doc["reemplaza_a"], str) or not _ID.match(doc["reemplaza_a"])
    ):
        raise DatasetError(f"{origen}: reemplaza_a debe ser un dataset_id")
    return doc


def comprobar(manifiesto: dict[str, Any], carpeta_datos: Path, hashes: bool) -> list[str]:
    """Problemas entre el manifiesto y el disco. Lista vacia = OK."""
    problemas: list[str] = []
    for f in manifiesto["ficheros"]:
        ruta = carpeta_datos / str(f["ruta"])
        if not ruta.is_file():
            problemas.append(f"falta en disco: {f['ruta']}")
            continue
        datos = ruta.read_bytes()
        if len(datos) != f["bytes"]:
            problemas.append(f"tamano distinto: {f['ruta']}")
        elif hashes and _sha256(datos) != f["sha256"]:
            problemas.append(f"hash distinto: {f['ruta']}")
    return problemas


def cargar_serie(
    manifiesto: dict[str, Any],
    carpeta_datos: Path,
    desde: date | None = None,
    hasta: date | None = None,
) -> SerieVelas:
    """M1 del dataset en orden, comprobando el hash de cada fichero antes de leerlo.

    Con `desde`/`hasta` (dias UTC inclusivos) solo se leen los ficheros mensuales necesarios y se
    devuelve la ventana: F10 y F14 cargan la ventana de un caso, no meses enteros.
    """
    velas: list[Vela] = []
    for f in manifiesto["ficheros"]:
        mes = str(f["ruta"]).rsplit("_", 1)[-1].removesuffix(".csv")
        if desde and mes < desde.strftime("%Y-%m") or hasta and mes > hasta.strftime("%Y-%m"):
            continue
        ruta = carpeta_datos / str(f["ruta"])
        if not ruta.is_file():
            raise DatasetError(f"falta en disco: {f['ruta']} (botsito data download)")
        if _sha256(ruta.read_bytes()) != f["sha256"]:
            raise DatasetError(f"{f['ruta']} no coincide con el manifiesto: dataset alterado")
        parte = leer_fichero(ruta)
        if len(parte) != f["filas"]:
            raise DatasetError(f"{f['ruta']}: {len(parte)} filas, el manifiesto dice {f['filas']}")
        if velas and parte and parte[0].inicio <= velas[-1].inicio:
            raise DatasetError(f"{f['ruta']}: ficheros desordenados en el manifiesto")
        velas.extend(parte)
    if desde or hasta:
        velas = [
            v
            for v in velas
            if (desde is None or a_datetime(v.inicio).date() >= desde)
            and (hasta is None or a_datetime(v.inicio).date() <= hasta)
        ]
    return SerieVelas(
        simbolo=str(manifiesto["simbolo"]),
        periodo_min=int(manifiesto["periodo_min"]),
        escala=int(manifiesto["escala"]),
        escala_volumen=int(manifiesto["escala_volumen"]),
        velas=tuple(velas),
    )


def manifiestos(repo: Path) -> list[Path]:
    carpeta = repo / DIRECTORIO_MANIFIESTOS
    if not carpeta.is_dir():
        return []
    salida: list[Path] = []
    for p in sorted(x for x in carpeta.iterdir() if x.is_file()):
        if p.name == "README.md" or p.name.startswith("_"):
            continue
        if p.suffix != ".yaml":
            raise DatasetError(f"fichero inesperado en {DIRECTORIO_MANIFIESTOS}: {p.name}")
        salida.append(p)
    return salida


def buscar_manifiesto(repo: Path, nombre_o_id: str) -> Path:
    """Acepta el id completo o el nombre sin sufijo (si hay uno solo con ese nombre)."""
    candidatos = [
        p
        for p in manifiestos(repo)
        if p.stem == nombre_o_id or p.stem.rsplit("-", 1)[0] == nombre_o_id
    ]
    if len(candidatos) == 1:
        return candidatos[0]
    if not candidatos:
        raise DatasetError(f"no hay manifiesto para {nombre_o_id!r} en {DIRECTORIO_MANIFIESTOS}")
    raise DatasetError(
        f"{nombre_o_id!r} es ambiguo: {[p.stem for p in candidatos]}; usa el dataset_id completo"
    )
