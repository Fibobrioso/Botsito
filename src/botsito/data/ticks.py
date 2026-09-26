"""Ticks de Dukascopy congelados (rama `trabajo/ticks-llenado`, ADR-0051): el mismo procedimiento y
la misma politica de almacenamiento que las M1 (`data/dataset.py`), por horas.

Hechos del proveedor: un fichero por hora y simbolo en
`{base}/{SIMBOLO}/{AAAA}/{MM-1}/{DD}/{HH}h_ticks.bi5` (mes en base 0), LZMA, 20 bytes por tick
`>IIIff` = (milisegundos desde el inicio de la hora, ASK, BID, volumen ASK, volumen BID); los
precios ya son enteros en la escala del simbolo, los volumenes float en millones. Una hora sin
mercado es 404 o un cuerpo vacio. Medido el 2026-09-26 sobre una hora de abril de 2026.

Disposicion bajo la carpeta de datos (`[rutas].data`, ignorada por git salvo `manifests/`):

    data/ticks/<dataset_id>/<SIMBOLO>_TICKS_<AAAA-MM-DD>.csv   (un fichero por dia, no versionado)
    data/manifests/ticks/<dataset_id>.yaml                     (versionado, INMUTABLE)
    data/raw/<SIMBOLO>/ticks/<AAAA-MM-DD>/<HH>.bi5            (cache cruda; `.404` si no existe)

EN STREAMING: se descarga hora a hora, se escribe el CSV de cada dia en cuanto acaba y no se
guarda en memoria mas que un dia. Una hora que falla tras los reintentos NO aborta la descarga:
queda en `horas.perdidas` del manifiesto y el modelo de llenado la cubre con el respaldo M1
(ADR-0051 §5). El manifiesto lleva el sha256 de cada CSV y el `dataset_id` cubre esos hashes, como
en las M1. Los manifiestos de ticks viven en su subcarpeta para que `data/dataset.manifiestos`,
que valida el esquema de las M1, no los confunda.
"""

from __future__ import annotations

import lzma
import math
import re
import struct
from collections.abc import Callable, Iterator, Sequence
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

import yaml

from botsito.comun import ids
from botsito.comun.documentos import ficheros_de, sha256_hex
from botsito.comun.yaml_estricto import YamlError, leer_yaml
from botsito.data.dukascopy import (
    ESCALA_VOLUMEN,
    HUSO_DATOS,
    PROVEEDOR,
    URL_BASE,
    Descarga,
    DescargaError,
    FormatoBi5Error,
)
from botsito.domain.ticks import MS_POR_MINUTO, MilisegundoUtc, Tick, TickInvalidoError
from botsito.domain.valores import Puntos

SCHEMA_TICKS = 1
DECODIFICADOR_TICKS_VERSION = 1
DIRECTORIO_MANIFIESTOS_TICKS = "data/manifests/ticks"
CARPETA_TICKS = "ticks"
MAX_INTENTOS_POR_TRAMO = 5  # el brief: como maximo 5 por tramo, con espera creciente
ESPERA_BASE_S = 15.0  # 15, 30, 45, 60 s: con 5 s el 503 del servidor no se recuperaba
CABECERA_CSV = "ts_utc,ask,bid,volumen_ask,volumen_bid"
_REGISTRO = struct.Struct(">IIIff")
_MS_POR_HORA = 3_600_000
_NOMBRE = re.compile(r"^(?=.{2,48}$)[a-z0-9]+(-[a-z0-9]+)*$", re.ASCII)
_SUFIJO_HEX = re.compile(r"^[0-9a-f]{8}$", re.ASCII)
_SIMBOLO = re.compile(r"^[A-Z0-9]{3,12}$", re.ASCII)
_SHA256 = re.compile(r"^[0-9a-f]{64}$", re.ASCII)
_TS = re.compile(r"^(\d{4}-\d{2}-\d{2})T(\d{2}):(\d{2}):(\d{2})\.(\d{3})Z$", re.ASCII)
_EPOCA = datetime(1970, 1, 1, tzinfo=UTC)
CAMPOS = (
    "schema_ticks",
    "dataset_id",
    "proveedor",
    "simbolo",
    "escala",
    "escala_volumen",
    "huso_datos",
    "decodificador_version",
    "desde",
    "hasta",
    "descargado_el",
    "ficheros",
    "horas",
    "ticks",
)
CAMPOS_OPCIONALES = ("generado_por",)


class TicksError(ValueError):
    """El dataset de ticks o su manifiesto no cumplen el esquema o no coinciden con el disco."""


# ------------------------------------------------------------------------------- proveedor


def url_hora(simbolo: str, dia: date, hora: int, base: str = URL_BASE) -> str:
    return (
        f"{base}/{simbolo}/{dia.year:04d}/{dia.month - 1:02d}/{dia.day:02d}/{hora:02d}h_ticks.bi5"
    )


def decodificar_ticks(cuerpo: bytes, dia: date, hora: int) -> list[Tick]:
    """Los ticks de una hora, en orden. Un cuerpo vacio es una hora sin mercado."""
    if not cuerpo:
        return []
    try:
        crudo = lzma.decompress(cuerpo)
    except lzma.LZMAError as exc:
        raise FormatoBi5Error(f"{dia} {hora:02d}h: no es LZMA ({exc})") from exc
    if len(crudo) % _REGISTRO.size:
        raise FormatoBi5Error(
            f"{dia} {hora:02d}h: {len(crudo)} bytes no es multiplo de {_REGISTRO.size}"
        )
    inicio = int(
        (datetime(dia.year, dia.month, dia.day, hora, tzinfo=UTC) - _EPOCA).total_seconds()
    )
    inicio_ms = inicio * 1000
    ticks: list[Tick] = []
    anterior = -1
    for ms, ask, bid, vol_ask, vol_bid in _REGISTRO.iter_unpack(crudo):
        if ms >= _MS_POR_HORA:
            raise FormatoBi5Error(f"{dia} {hora:02d}h: milisegundo fuera de la hora ({ms})")
        if ms < anterior:
            raise FormatoBi5Error(f"{dia} {hora:02d}h: ticks desordenados en {ms}")
        anterior = ms
        if not (math.isfinite(vol_ask) and math.isfinite(vol_bid)) or vol_ask < 0 or vol_bid < 0:
            raise FormatoBi5Error(f"{dia} {hora:02d}h ms {ms}: volumen invalido")
        try:
            ticks.append(
                Tick(
                    MilisegundoUtc(inicio_ms + ms),
                    Puntos(ask),
                    Puntos(bid),
                    round(vol_ask * ESCALA_VOLUMEN),
                    round(vol_bid * ESCALA_VOLUMEN),
                )
            )
        except TickInvalidoError as exc:
            raise FormatoBi5Error(f"{dia} {hora:02d}h ms {ms}: {exc}") from exc
    return ticks


def con_cache_horas(raw: Path, descarga: Descarga) -> Descarga:
    """Cache por hora del fichero crudo: `<raw>/<SIMBOLO>/ticks/<AAAA-MM-DD>/<HH>.bi5`."""

    def cacheada(url: str) -> bytes | None:
        partes = url.rstrip("/").split("/")
        simbolo, anio, mes0, dia, fichero = (
            partes[-5],
            partes[-4],
            partes[-3],
            partes[-2],
            partes[-1],
        )
        hora = fichero[:2]
        base = raw / simbolo / CARPETA_TICKS / f"{anio}-{int(mes0) + 1:02d}-{dia}" / hora
        cuerpo_f, marca_404 = base.with_suffix(".bi5"), base.with_suffix(".404")
        if cuerpo_f.exists():
            return cuerpo_f.read_bytes()
        if marca_404.exists():
            return None
        cuerpo = descarga(url)
        base.parent.mkdir(parents=True, exist_ok=True)
        if cuerpo is None:
            marca_404.write_bytes(b"")
        else:
            cuerpo_f.write_bytes(cuerpo)
        return cuerpo

    return cacheada


@dataclass(frozen=True, slots=True)
class HoraDescargada:
    dia: date
    hora: int
    ticks: tuple[Tick, ...]
    estado: str  # presente | ausente (404) | vacia | perdida (fallo tras los reintentos)


def descargar_hora(
    simbolo: str, dia: date, hora: int, descarga: Descarga, base: str = URL_BASE
) -> HoraDescargada:
    """Una hora. Un `DescargaError` (tras los reintentos de `descarga`) NO se propaga: la hora
    queda PERDIDA y la descarga sigue; el manifiesto la lista."""
    try:
        cuerpo = descarga(url_hora(simbolo, dia, hora, base))
    except DescargaError:
        return HoraDescargada(dia, hora, (), "perdida")
    if cuerpo is None:
        return HoraDescargada(dia, hora, (), "ausente")
    ticks = decodificar_ticks(cuerpo, dia, hora)
    return HoraDescargada(dia, hora, tuple(ticks), "presente" if ticks else "vacia")


# ---------------------------------------------------------------------------------- CSV


def formato_ts_ms(ms: int) -> str:
    return (_EPOCA + timedelta(milliseconds=ms)).strftime(
        "%Y-%m-%dT%H:%M:%S."
    ) + f"{ms % 1000:03d}Z"


def parse_ts_ms(texto: str) -> MilisegundoUtc:
    m = _TS.match(texto)
    if m is None:
        raise TicksError(f"ts_utc invalido {texto!r}")
    dia = date.fromisoformat(m.group(1))
    segundos = int(
        (
            datetime(
                dia.year,
                dia.month,
                dia.day,
                int(m.group(2)),
                int(m.group(3)),
                int(m.group(4)),
                tzinfo=UTC,
            )
            - _EPOCA
        ).total_seconds()
    )
    return MilisegundoUtc(segundos * 1000 + int(m.group(5)))


def escribir_csv_ticks(ticks: Sequence[Tick]) -> str:
    lineas = [CABECERA_CSV]
    lineas += [
        f"{formato_ts_ms(t.instante)},{t.ask},{t.bid},{t.volumen_ask},{t.volumen_bid}"
        for t in ticks
    ]
    return "\n".join(lineas) + "\n"


def leer_csv_ticks(texto: str) -> list[Tick]:
    lineas = texto.split("\n")
    if not lineas or lineas[0] != CABECERA_CSV:
        raise TicksError("CSV de ticks sin la cabecera esperada")
    if lineas[-1] != "":
        raise TicksError("CSV de ticks sin salto de linea final")
    salida: list[Tick] = []
    for n, linea in enumerate(lineas[1:-1], 2):
        partes = linea.split(",")
        if len(partes) != 5:
            raise TicksError(f"linea {n}: {len(partes)} campos, se esperaban 5")
        try:
            salida.append(
                Tick(
                    parse_ts_ms(partes[0]),
                    Puntos(int(partes[1])),
                    Puntos(int(partes[2])),
                    int(partes[3]),
                    int(partes[4]),
                )
            )
        except (ValueError, TickInvalidoError) as exc:
            raise TicksError(f"linea {n}: {exc}") from exc
        if len(salida) > 1 and salida[-1].instante < salida[-2].instante:
            raise TicksError(f"linea {n}: ticks desordenados")
    return salida


def leer_fichero_ticks(ruta: Path) -> list[Tick]:
    texto = ruta.read_bytes().decode("utf-8")
    if "\r" in texto:
        raise TicksError(f"{ruta.name}: contiene CR; el formato congelado es LF")
    return leer_csv_ticks(texto)


# ------------------------------------------------------------------------------ congelar


@dataclass(frozen=True, slots=True)
class CongeladoTicks:
    manifiesto: dict[str, Any]
    ruta_manifiesto: Path
    ficheros: tuple[Path, ...]


@dataclass
class _Recuento:
    presentes: int = 0
    ausentes: int = 0
    vacias: int = 0
    perdidas: list[str] = field(default_factory=list)
    ticks: int = 0
    cruzados: int = 0  # ASK < BID


def _dias(desde: date, hasta: date) -> Iterator[date]:
    if hasta < desde:
        raise TicksError(f"rango invalido: {desde} > {hasta}")
    d = desde
    while d <= hasta:
        yield d
        d += timedelta(days=1)


def ruta_manifiesto_ticks(repo: Path, dataset_id: str) -> Path:
    if not ids.DATASET.match(dataset_id):
        raise TicksError(f"dataset_id {dataset_id!r} invalido (nombre-hash8)")
    return repo / DIRECTORIO_MANIFIESTOS_TICKS / f"{dataset_id}.yaml"


def id_desde_hashes(nombre: str, hashes: Sequence[str]) -> str:
    return f"{nombre}-{sha256_hex(chr(10).join(hashes).encode('ascii'))[:8]}"


def congelar_ticks(
    repo: Path,
    carpeta_datos: Path,
    nombre: str,
    simbolo: str,
    escala: int,
    desde: date,
    hasta: date,
    descarga: Descarga,
    hoy: date,
    generado_por: str | None = None,
    avisar: Callable[[str], None] | None = None,
    descargar: Callable[..., HoraDescargada] = descargar_hora,
) -> CongeladoTicks:
    """Descarga el rango hora a hora, escribe un CSV por dia y el manifiesto. Nunca sobreescribe.

    Streaming: cada dia se escribe al terminar sus 24 horas y se suelta. Los ficheros van a una
    carpeta temporal `<dataset>.parcial` hasta conocer el id (que depende de los hashes) y se
    mueven al final; si la descarga se corta, lo crudo esta en la cache y se reanuda.
    """
    if not _NOMBRE.match(nombre) or _SUFIJO_HEX.match(nombre.rsplit("-", 1)[-1]):
        raise TicksError(f"nombre {nombre!r} invalido")
    if not _SIMBOLO.match(simbolo):
        raise TicksError(f"simbolo {simbolo!r} invalido")
    if isinstance(escala, bool) or escala <= 0:
        raise TicksError("escala debe ser un entero positivo")
    if hasta >= hoy:
        raise TicksError(f"hasta ({hasta}) debe ser anterior a hoy ({hoy})")
    parcial = carpeta_datos / CARPETA_TICKS / f"{nombre}.parcial"
    if parcial.exists():
        raise TicksError(f"queda una descarga parcial en {parcial}: borrala o terminala")
    parcial.mkdir(parents=True)
    recuento = _Recuento()
    ficheros: list[dict[str, Any]] = []
    rutas: list[Path] = []
    hashes: list[str] = []
    for dia in _dias(desde, hasta):
        del_dia: list[Tick] = []
        for hora in range(24):
            h = descargar(simbolo, dia, hora, descarga)
            if h.estado == "presente":
                recuento.presentes += 1
                del_dia.extend(h.ticks)
            elif h.estado == "ausente":
                recuento.ausentes += 1
            elif h.estado == "vacia":
                recuento.vacias += 1
            else:
                recuento.perdidas.append(f"{dia.isoformat()}T{hora:02d}Z")
                if avisar:
                    avisar(f"PERDIDA: {dia} {hora:02d}h tras {MAX_INTENTOS_POR_TRAMO} intentos")
        if not del_dia:
            continue
        recuento.ticks += len(del_dia)
        recuento.cruzados += sum(1 for t in del_dia if t.ask < t.bid)
        nombre_fichero = f"{simbolo}_TICKS_{dia.isoformat()}.csv"
        texto = escribir_csv_ticks(del_dia).encode("utf-8")
        ruta = parcial / nombre_fichero
        ruta.write_bytes(texto)
        rutas.append(ruta)
        sha = sha256_hex(texto)
        hashes.append(sha)
        ficheros.append(
            {
                "ruta": nombre_fichero,  # se completa con la carpeta del dataset al final
                "bytes": len(texto),
                "sha256": sha,
                "filas": len(del_dia),
                "primera": formato_ts_ms(del_dia[0].instante),
                "ultima": formato_ts_ms(del_dia[-1].instante),
            }
        )
        if avisar:
            avisar(f"{dia}: {len(del_dia)} ticks")
        del del_dia
    if not ficheros:
        parcial.rmdir()
        raise TicksError("el rango no contiene ningun tick: no se congela un dataset vacio")
    dataset_id = id_desde_hashes(nombre, hashes)
    ruta_manifiesto = ruta_manifiesto_ticks(repo, dataset_id)
    carpeta = carpeta_datos / CARPETA_TICKS / dataset_id
    if ruta_manifiesto.exists() or carpeta.exists():
        for r in rutas:
            r.unlink()
        parcial.rmdir()
        raise TicksError(f"el dataset {dataset_id} ya existe con este mismo contenido")
    parcial.rename(carpeta)
    rutas = [carpeta / r.name for r in rutas]
    for f in ficheros:
        f["ruta"] = f"{CARPETA_TICKS}/{dataset_id}/{f['ruta']}"
    manifiesto: dict[str, Any] = {
        "schema_ticks": SCHEMA_TICKS,
        "dataset_id": dataset_id,
        "proveedor": PROVEEDOR,
        "simbolo": simbolo,
        "escala": escala,
        "escala_volumen": ESCALA_VOLUMEN,
        "huso_datos": HUSO_DATOS,
        "decodificador_version": DECODIFICADOR_TICKS_VERSION,
        "desde": desde.isoformat(),
        "hasta": hasta.isoformat(),
        "descargado_el": hoy.isoformat(),
        "ficheros": ficheros,
        "horas": {
            "presentes": recuento.presentes,
            "ausentes_404": recuento.ausentes,
            "vacias": recuento.vacias,
            "perdidas": recuento.perdidas,
        },
        "ticks": {"total": recuento.ticks, "cruzados_ask_menor_que_bid": recuento.cruzados},
    }
    if generado_por:
        manifiesto["generado_por"] = generado_por
    escribir_manifiesto_ticks(manifiesto, ruta_manifiesto)
    return CongeladoTicks(manifiesto, ruta_manifiesto, tuple(rutas))


def escribir_manifiesto_ticks(manifiesto: dict[str, Any], ruta: Path) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    texto = yaml.safe_dump(manifiesto, allow_unicode=True, sort_keys=True, width=100)
    ruta.write_text(
        "# GENERADO por `botsito data download-ticks`. INMUTABLE: no editar; un cambio es otro "
        "dataset.\n" + texto,
        encoding="utf-8",
        newline="\n",
    )


# -------------------------------------------------------------------------------- cargar


def _texto(doc: dict[str, Any], campo: str, origen: str) -> str:
    v = doc.get(campo)
    if not isinstance(v, str) or not v:
        raise TicksError(f"{origen}: {campo} debe ser texto no vacio")
    return v


def validar_manifiesto_ticks(doc: dict[str, Any], origen: str) -> dict[str, Any]:
    faltan = [c for c in CAMPOS if c not in doc]
    if faltan:
        raise TicksError(f"{origen}: faltan campos {faltan}")
    desconocidos = sorted(set(doc) - set(CAMPOS) - set(CAMPOS_OPCIONALES))
    if desconocidos:
        raise TicksError(f"{origen}: campos desconocidos {desconocidos}")
    if doc["schema_ticks"] != SCHEMA_TICKS:
        raise TicksError(f"{origen}: schema_ticks {doc['schema_ticks']!r} no soportado")
    dataset_id = _texto(doc, "dataset_id", origen)
    if not ids.DATASET.match(dataset_id):
        raise TicksError(f"{origen}: dataset_id invalido")
    if origen != "manifiesto" and Path(origen).stem != dataset_id:
        raise TicksError(f"{origen}: el fichero debe llamarse {dataset_id}.yaml")
    fijos = {"proveedor": PROVEEDOR, "huso_datos": HUSO_DATOS, "escala_volumen": ESCALA_VOLUMEN}
    for campo, valor in fijos.items():
        if doc[campo] != valor:
            raise TicksError(f"{origen}: {campo} debe ser {valor!r}")
    if not _SIMBOLO.match(_texto(doc, "simbolo", origen)):
        raise TicksError(f"{origen}: simbolo invalido")
    for campo in ("escala", "decodificador_version"):
        v = doc[campo]
        if isinstance(v, bool) or not isinstance(v, int) or v <= 0:
            raise TicksError(f"{origen}: {campo} debe ser un entero positivo")
    fechas: dict[str, date] = {}
    for campo in ("desde", "hasta", "descargado_el"):
        try:
            fechas[campo] = date.fromisoformat(_texto(doc, campo, origen))
        except ValueError as exc:
            raise TicksError(f"{origen}: {campo} no es una fecha") from exc
    if fechas["hasta"] < fechas["desde"] or fechas["descargado_el"] <= fechas["hasta"]:
        raise TicksError(f"{origen}: fechas incoherentes")
    ficheros = doc["ficheros"]
    if not isinstance(ficheros, list) or not ficheros:
        raise TicksError(f"{origen}: ficheros debe ser una lista no vacia")
    hashes: list[str] = []
    rutas: set[str] = set()
    for f in ficheros:
        if not isinstance(f, dict):
            raise TicksError(f"{origen}: entrada de fichero invalida")
        ruta = f.get("ruta")
        if (
            not isinstance(ruta, str)
            or not ruta
            or ruta in rutas
            or ".." in ruta
            or ruta[0] in "/\\"
        ):
            raise TicksError(f"{origen}: ruta invalida o repetida {ruta!r}")
        rutas.add(ruta)
        if not isinstance(f.get("sha256"), str) or not _SHA256.match(f["sha256"]):
            raise TicksError(f"{origen}: sha256 invalido en {ruta}")
        hashes.append(f["sha256"])
        for campo in ("bytes", "filas"):
            v = f.get(campo)
            if isinstance(v, bool) or not isinstance(v, int) or v < 1:
                raise TicksError(f"{origen}: {campo} invalido en {ruta}")
        primera, ultima = parse_ts_ms(str(f.get("primera"))), parse_ts_ms(str(f.get("ultima")))
        if primera > ultima:
            raise TicksError(f"{origen}: primera/ultima invertidas en {ruta}")
    nombre = dataset_id.rsplit("-", 1)[0]
    if id_desde_hashes(nombre, hashes) != dataset_id:
        raise TicksError(f"{origen}: el sufijo del dataset_id no coincide con los hashes")
    if not isinstance(doc["horas"], dict) or not isinstance(doc["ticks"], dict):
        raise TicksError(f"{origen}: horas y ticks deben ser mapas")
    return doc


def cargar_manifiesto_ticks(ruta: Path) -> dict[str, Any]:
    if not ruta.exists():
        raise TicksError(f"no existe {ruta}")
    try:
        doc = leer_yaml(ruta)
    except YamlError as exc:
        raise TicksError(f"{ruta.name}: {exc}") from exc
    if not isinstance(doc, dict):
        raise TicksError(f"{ruta.name}: se esperaba un mapa")
    return validar_manifiesto_ticks(doc, str(ruta))


def manifiestos_ticks(repo: Path) -> list[Path]:
    carpeta = repo / DIRECTORIO_MANIFIESTOS_TICKS
    if not carpeta.is_dir():
        return []
    return [
        p for p in ficheros_de(carpeta, TicksError, "manifiestos de ticks") if p.parent == carpeta
    ]


def buscar_manifiesto_ticks(repo: Path, nombre_o_id: str) -> Path:
    candidatos = [
        p
        for p in manifiestos_ticks(repo)
        if p.stem == nombre_o_id or p.stem.rsplit("-", 1)[0] == nombre_o_id
    ]
    if not candidatos:
        raise TicksError(f"no hay manifiesto de ticks para {nombre_o_id!r}")
    if len(candidatos) > 1:
        raise TicksError(f"{nombre_o_id!r} es ambiguo: {[c.stem for c in candidatos]}")
    return candidatos[0]


def comprobar_ticks(manifiesto: dict[str, Any], carpeta_datos: Path, hashes: bool) -> list[str]:
    problemas: list[str] = []
    for f in manifiesto["ficheros"]:
        ruta = carpeta_datos / str(f["ruta"])
        if not ruta.is_file():
            problemas.append(f"falta en disco: {f['ruta']}")
            continue
        datos = ruta.read_bytes()
        if len(datos) != f["bytes"]:
            problemas.append(f"tamano distinto: {f['ruta']}")
        elif hashes and sha256_hex(datos) != f["sha256"]:
            problemas.append(f"hash distinto: {f['ruta']}")
    return problemas


@dataclass(frozen=True)
class SerieTicks:
    simbolo: str
    escala: int
    origen: str
    ticks: tuple[Tick, ...]
    horas_perdidas: tuple[str, ...]  # `AAAA-MM-DDTHHZ`: sin ticks por fallo, no por mercado cerrado


def cargar_ticks(
    manifiesto: dict[str, Any],
    carpeta_datos: Path,
    desde_ms: int | None = None,
    hasta_ms: int | None = None,
) -> SerieTicks:
    """Los ticks de `[desde_ms, hasta_ms)`, leyendo solo los ficheros de los dias necesarios y
    comprobando su hash. Sin rango, todo el dataset (pesado: un mes son millones de ticks)."""
    if desde_ms is not None and hasta_ms is not None and hasta_ms < desde_ms:
        raise TicksError(f"ventana invalida: {desde_ms} > {hasta_ms}")
    dia_desde = (_EPOCA + timedelta(milliseconds=desde_ms)).date() if desde_ms is not None else None
    dia_hasta = (
        (_EPOCA + timedelta(milliseconds=hasta_ms - 1)).date() if hasta_ms is not None else None
    )
    ticks: list[Tick] = []
    for f in manifiesto["ficheros"]:
        dia = date.fromisoformat(str(f["ruta"]).rsplit("_", 1)[-1].removesuffix(".csv"))
        if (dia_desde and dia < dia_desde) or (dia_hasta and dia > dia_hasta):
            continue
        ruta = carpeta_datos / str(f["ruta"])
        if not ruta.is_file():
            raise TicksError(f"falta en disco: {f['ruta']} (botsito data download-ticks)")
        datos = ruta.read_bytes()
        if sha256_hex(datos) != f["sha256"]:
            raise TicksError(f"{f['ruta']} no coincide con el manifiesto: dataset alterado")
        parte = leer_csv_ticks(datos.decode("utf-8"))
        if len(parte) != f["filas"]:
            raise TicksError(f"{f['ruta']}: {len(parte)} filas, el manifiesto dice {f['filas']}")
        ticks.extend(parte)
    if desde_ms is not None or hasta_ms is not None:
        ticks = [
            t
            for t in ticks
            if (desde_ms is None or t.instante >= desde_ms)
            and (hasta_ms is None or t.instante < hasta_ms)
        ]
    return SerieTicks(
        simbolo=str(manifiesto["simbolo"]),
        escala=int(manifiesto["escala"]),
        origen=str(manifiesto["dataset_id"]),
        ticks=tuple(ticks),
        horas_perdidas=tuple(str(h) for h in manifiesto["horas"].get("perdidas", [])),
    )


def minutos_con_ticks(ticks: Sequence[Tick]) -> frozenset[int]:
    return frozenset(t.instante // MS_POR_MINUTO for t in ticks)


__all__ = [
    "CABECERA_CSV",
    "DIRECTORIO_MANIFIESTOS_TICKS",
    "MAX_INTENTOS_POR_TRAMO",
    "CongeladoTicks",
    "HoraDescargada",
    "SerieTicks",
    "TicksError",
    "buscar_manifiesto_ticks",
    "cargar_manifiesto_ticks",
    "cargar_ticks",
    "comprobar_ticks",
    "con_cache_horas",
    "congelar_ticks",
    "decodificar_ticks",
    "descargar_hora",
    "escribir_csv_ticks",
    "formato_ts_ms",
    "leer_csv_ticks",
    "leer_fichero_ticks",
    "manifiestos_ticks",
    "minutos_con_ticks",
    "parse_ts_ms",
    "url_hora",
    "validar_manifiesto_ticks",
]
