"""Proveedor Dukascopy (F15, ADR-0005): velas M1 BID por dia, formato bi5.

Hechos del proveedor (no son parametros de negocio): un fichero por dia y simbolo en
`{base}/{SIMBOLO}/{AAAA}/{MM-1}/{DD}/BID_candles_min_1.bi5` (el mes va en base 0), comprimido con
LZMA, 24 bytes por vela `>iiiiif` = (segundos desde 00:00 UTC, abierta, cierre, minima, maxima,
volumen). Los precios ya son enteros en la escala del simbolo. El servidor entrega siempre los
1440 minutos: cuando el mercado esta cerrado rellena con velas planas de volumen cero, que aqui
se descartan y se cuentan (MT5 tampoco construye una vela sin ticks). Exige `User-Agent`.

La funcion de red se inyecta: los tests nunca tocan la red. `con_cache` envuelve cualquier
descarga con una cache por dia del fichero crudo (`<raw>/<SIMBOLO>/<AAAA-MM-DD>.bi5`; un 404 se
recuerda como `.404`): con un servidor que tarda hasta un minuto por dia, un fallo a mitad de
mes no obliga a repetir lo ya descargado.
"""

from __future__ import annotations

import lzma
import math
import struct
import time
import urllib.error
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path

from botsito.data.velas import a_minuto
from botsito.domain.valores import Puntos
from botsito.domain.velas import MINUTOS_POR_DIA, MinutoUtc, Vela, VelaInvalidaError

PROVEEDOR = "dukascopy"
TIPO_PRECIO = "BID"
HUSO_DATOS = "UTC"
# El volumen llega como float32 (millones de moneda base); se congela como entero en milesimas.
ESCALA_VOLUMEN = 1000
# Version de la regla de descarte y del decodificador: un cambio obliga a un dataset nuevo.
FILTRO_PLANAS = 1
DECODIFICADOR_VERSION = 1
URL_BASE = "https://datafeed.dukascopy.com/datafeed"
_REGISTRO = struct.Struct(">iiiiif")
_USER_AGENT = "Mozilla/5.0 (botsito; datos historicos)"

Descarga = Callable[[str], bytes | None]
"""Devuelve el cuerpo de la URL, None si el recurso no existe (404), o lanza `DescargaError`."""


class DescargaError(RuntimeError):
    """La red o el servidor fallaron tras los reintentos."""


class FormatoBi5Error(ValueError):
    """El fichero no tiene el formato esperado."""


@dataclass(frozen=True, slots=True)
class DiaDescargado:
    dia: date
    velas: tuple[Vela, ...]
    registros: int
    descartadas: int  # velas planas de volumen cero (sin ticks)
    presente: bool  # False si el proveedor no tiene fichero para ese dia (404)
    volumen_cero_no_planas: int = 0  # conservadas: precio se movio sin volumen (dato dudoso)
    descartadas_dentro_de_sesion: int = 0  # planas entre la primera y la ultima activa del dia


def url_dia(simbolo: str, dia: date, base: str = URL_BASE) -> str:
    return (
        f"{base}/{simbolo}/{dia.year:04d}/{dia.month - 1:02d}/{dia.day:02d}/BID_candles_min_1.bi5"
    )


def descarga_http(url: str, intentos: int = 6, espera_s: float = 5.0) -> bytes | None:
    """Descarga real con reintentos y espera creciente (5, 10, ... 30 s: el servidor devuelve
    503 cuando se satura). 404 -> None (dia sin fichero)."""
    ultimo: Exception | None = None
    for intento in range(intentos):
        try:
            peticion = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
            with urllib.request.urlopen(peticion, timeout=60) as respuesta:  # noqa: S310
                return bytes(respuesta.read())
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return None
            ultimo = exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            ultimo = exc
        if intento + 1 < intentos:
            time.sleep(espera_s * (intento + 1))
    raise DescargaError(f"{url}: {ultimo}")


def con_cache(raw: Path, descarga: Descarga) -> Descarga:
    """Descarga con memoria en disco por URL de dia (reanudacion de descargas largas)."""

    def cacheada(url: str) -> bytes | None:
        partes = url.rstrip("/").split("/")
        # .../{SIMBOLO}/{AAAA}/{MM-1}/{DD}/BID_candles_min_1.bi5
        simbolo, anio, mes0, dia = partes[-5], partes[-4], partes[-3], partes[-2]
        base = raw / simbolo / f"{anio}-{int(mes0) + 1:02d}-{dia}"
        fichero, marca_404 = base.with_suffix(".bi5"), base.with_suffix(".404")
        if fichero.exists():
            return fichero.read_bytes()
        if marca_404.exists():
            return None
        cuerpo = descarga(url)
        base.parent.mkdir(parents=True, exist_ok=True)
        if cuerpo is None:
            marca_404.write_bytes(b"")
        else:
            fichero.write_bytes(cuerpo)
        return cuerpo

    return cacheada


def decodificar_bi5(cuerpo: bytes, dia: date) -> tuple[list[Vela], int]:
    """Velas del dia (con las planas incluidas) y numero de registros."""
    if not cuerpo:
        return [], 0
    # Descompresion acotada: un cuerpo de pocos KB no puede expandirse a cientos de MB.
    maximo = MINUTOS_POR_DIA * _REGISTRO.size
    try:
        descompresor = lzma.LZMADecompressor()
        crudo = descompresor.decompress(cuerpo, max_length=maximo + 1)
    except lzma.LZMAError as exc:
        raise FormatoBi5Error(f"{dia}: no es LZMA ({exc})") from exc
    if len(crudo) > maximo or not descompresor.eof:
        raise FormatoBi5Error(f"{dia}: mas de {MINUTOS_POR_DIA} registros o fichero truncado")
    if len(crudo) % _REGISTRO.size:
        raise FormatoBi5Error(f"{dia}: {len(crudo)} bytes no es multiplo de {_REGISTRO.size}")
    inicio_dia = a_minuto(datetime(dia.year, dia.month, dia.day, tzinfo=UTC))
    velas: list[Vela] = []
    anterior = -1
    for segundos, abierta, cierre, minima, maxima, volumen in _REGISTRO.iter_unpack(crudo):
        if segundos % 60 or not 0 <= segundos < MINUTOS_POR_DIA * 60:
            raise FormatoBi5Error(f"{dia}: marca de tiempo invalida {segundos}")
        minuto = segundos // 60
        if minuto <= anterior:
            raise FormatoBi5Error(
                f"{dia}: registros desordenados o duplicados en el minuto {minuto}"
            )
        anterior = minuto
        if not math.isfinite(volumen) or volumen < 0:
            raise FormatoBi5Error(f"{dia} minuto {minuto}: volumen invalido {volumen!r}")
        try:
            velas.append(
                Vela(
                    inicio=MinutoUtc(inicio_dia + minuto),
                    abierta=Puntos(abierta),
                    maxima=Puntos(maxima),
                    minima=Puntos(minima),
                    cierre=Puntos(cierre),
                    volumen=round(volumen * ESCALA_VOLUMEN),
                )
            )
        except VelaInvalidaError as exc:
            raise FormatoBi5Error(f"{dia} minuto {minuto}: {exc}") from exc
    return velas, len(velas)


def es_plana_sin_volumen(v: Vela) -> bool:
    return v.volumen == 0 and v.abierta == v.maxima == v.minima == v.cierre


def descargar_dia(
    simbolo: str, dia: date, descarga: Descarga, base: str = URL_BASE
) -> DiaDescargado:
    cuerpo = descarga(url_dia(simbolo, dia, base))
    if cuerpo is None:
        return DiaDescargado(dia, (), 0, 0, presente=False)
    velas, registros = decodificar_bi5(cuerpo, dia)
    activas = tuple(v for v in velas if not es_plana_sin_volumen(v))
    descartadas = registros - len(activas)
    dudosas = sum(1 for v in activas if v.volumen == 0)
    # "Dentro de sesion": planas entre la primera y la ultima vela activa del dia. Las del cierre
    # del viernes o del fin de semana no cuentan; las de un minuto sin ticks a media manana si.
    dentro = 0
    if activas:
        primera, ultima = activas[0].inicio, activas[-1].inicio
        dentro = sum(1 for v in velas if es_plana_sin_volumen(v) and primera < v.inicio < ultima)
    return DiaDescargado(
        dia,
        activas,
        registros,
        descartadas,
        presente=True,
        volumen_cero_no_planas=dudosas,
        descartadas_dentro_de_sesion=dentro,
    )
