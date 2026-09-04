"""Velas en la capa de datos (F15): conversion de instantes y CSV determinista.

El dominio ve `MinutoUtc` (entero); aqui se convierte a `datetime` con huso UTC y se serializa.
CSV M1: `ts_utc,abierta,maxima,minima,cierre,volumen`; CSV agregado: ademas `duracion_min`,
`n_m1` y `completa` (la vela que cruza un cambio de hora no dura el periodo nominal y la de
borde puede no estar cerrada). LF sin BOM, ascendente, sin duplicados, `ts_utc` en ISO 8601 con
sufijo `Z` y resolucion de minuto, todo entero. Cualquier desviacion al leer es un error: un
dataset congelado no se "arregla" al cargarlo.
"""

from __future__ import annotations

import csv
import io
from datetime import UTC, datetime, timedelta
from pathlib import Path

from botsito.domain.valores import Puntos
from botsito.domain.velas import MinutoUtc, Vela, VelaInvalidaError

COLUMNAS = ("ts_utc", "abierta", "maxima", "minima", "cierre", "volumen")
COLUMNAS_AGREGADAS = (*COLUMNAS, "duracion_min", "n_m1", "completa")
_EPOCA = datetime(1970, 1, 1, tzinfo=UTC)
_FORMATO_TS = "%Y-%m-%dT%H:%MZ"
_BOM = "﻿"


class VelasCsvError(ValueError):
    """El CSV no cumple el formato congelado."""


def a_minuto(instante: datetime) -> MinutoUtc:
    """`datetime` con huso -> minutos UTC desde la epoca. Un `datetime` sin huso es un error."""
    if instante.tzinfo is None or instante.utcoffset() is None:
        raise ValueError("el instante debe llevar huso")
    delta = instante.astimezone(UTC) - _EPOCA
    segundos = delta.days * 86400 + delta.seconds
    if segundos % 60 or delta.microseconds:
        raise ValueError(f"el instante no cae en un minuto exacto: {instante.isoformat()}")
    return MinutoUtc(segundos // 60)


def a_datetime(minuto: MinutoUtc | int) -> datetime:
    return _EPOCA + timedelta(minutes=int(minuto))


def formato_ts(minuto: MinutoUtc | int) -> str:
    return a_datetime(minuto).strftime(_FORMATO_TS)


def parse_ts(texto: str) -> MinutoUtc:
    try:
        return a_minuto(datetime.strptime(texto, _FORMATO_TS).replace(tzinfo=UTC))
    except ValueError as exc:
        raise VelasCsvError(f"ts_utc invalido {texto!r} (formato AAAA-MM-DDTHH:MMZ)") from exc


def escribir_csv(velas: list[Vela], agregadas: bool = False) -> str:
    """Texto CSV determinista. Exige orden ascendente estricto (sin duplicados).

    Sin `agregadas`, todas las velas deben ser M1 completas.
    """
    salida = io.StringIO()
    w = csv.writer(salida, lineterminator="\n")
    w.writerow(COLUMNAS_AGREGADAS if agregadas else COLUMNAS)
    anterior: int | None = None
    for v in velas:
        if anterior is not None and v.inicio <= anterior:
            raise VelasCsvError(f"velas desordenadas o duplicadas en {formato_ts(v.inicio)}")
        if not agregadas and (v.duracion_min != 1 or v.n_m1 != 1 or not v.completa):
            raise VelasCsvError(f"vela que no es M1 en un CSV de M1 ({formato_ts(v.inicio)})")
        anterior = v.inicio
        fila: list[object] = [formato_ts(v.inicio), v.abierta, v.maxima, v.minima, v.cierre]
        fila.append(v.volumen)
        if agregadas:
            fila += [v.duracion_min, v.n_m1, int(v.completa)]
        w.writerow(fila)
    return salida.getvalue()


def _entero_estricto(texto: str) -> int:
    """`int()` sin tolerancias: ni espacios, ni signo mas, ni guiones bajos."""
    if not texto or not (texto.isdigit() or (texto[0] == "-" and texto[1:].isdigit())):
        raise ValueError(f"no es un entero: {texto!r}")
    return int(texto)


def leer_csv(texto: str) -> list[Vela]:
    """Lee M1 o velas agregadas; la cabecera decide."""
    filas = list(csv.reader(io.StringIO(texto)))
    cabecera = tuple(filas[0]) if filas else ()
    if cabecera not in (COLUMNAS, COLUMNAS_AGREGADAS):
        raise VelasCsvError(f"cabecera invalida: se esperaba {','.join(COLUMNAS)}")
    agregadas = cabecera == COLUMNAS_AGREGADAS
    velas: list[Vela] = []
    anterior: int | None = None
    for n, fila in enumerate(filas[1:], start=2):
        if len(fila) != len(cabecera):
            raise VelasCsvError(f"linea {n}: {len(fila)} columnas, se esperaban {len(cabecera)}")
        inicio = parse_ts(fila[0])
        if anterior is not None and inicio <= anterior:
            raise VelasCsvError(f"linea {n}: velas desordenadas o duplicadas ({fila[0]})")
        anterior = inicio
        try:
            numeros = [_entero_estricto(x) for x in fila[1:]]
        except ValueError as exc:
            raise VelasCsvError(f"linea {n}: valor invalido ({exc})") from exc
        o, h, lo, c, vol = numeros[:5]
        duracion, n_m1, completa = (numeros[5], numeros[6], numeros[7]) if agregadas else (1, 1, 1)
        if completa not in (0, 1):
            raise VelasCsvError(f"linea {n}: completa debe ser 0 o 1")
        try:
            velas.append(
                Vela(
                    inicio,
                    Puntos(o),
                    Puntos(h),
                    Puntos(lo),
                    Puntos(c),
                    vol,
                    duracion,
                    n_m1,
                    bool(completa),
                )
            )
        except VelaInvalidaError as exc:
            raise VelasCsvError(f"linea {n}: {exc}") from exc
    return velas


def escribir_fichero(ruta: Path, velas: list[Vela], agregadas: bool = False) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(escribir_csv(velas, agregadas), encoding="utf-8", newline="\n")


def leer_fichero(ruta: Path) -> list[Vela]:
    try:
        texto = ruta.read_bytes().decode("utf-8")  # sin traduccion de saltos de linea
    except UnicodeDecodeError as exc:
        raise VelasCsvError(f"{ruta.name}: no es UTF-8") from exc
    if "\r" in texto or texto.startswith(_BOM):
        raise VelasCsvError(f"{ruta.name}: contiene CR o BOM; el formato congelado es LF sin BOM")
    return leer_csv(texto)
