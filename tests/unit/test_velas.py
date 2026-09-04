from datetime import UTC, datetime
from pathlib import Path

import pytest
from hypothesis import given
from hypothesis import strategies as st

from botsito.data.velas import (
    VelasCsvError,
    a_datetime,
    a_minuto,
    escribir_csv,
    escribir_fichero,
    formato_ts,
    leer_csv,
    leer_fichero,
    parse_ts,
)
from botsito.domain.valores import Puntos
from botsito.domain.velas import MinutoUtc, SerieVelas, Vela, VelaInvalidaError, combinar


def v(inicio: int, o: int, h: int, l: int, c: int, vol: int = 1, dur: int = 1) -> Vela:  # noqa: E741
    return Vela(MinutoUtc(inicio), Puntos(o), Puntos(h), Puntos(l), Puntos(c), vol, dur)


def test_invariantes_de_vela() -> None:
    assert v(0, 10, 12, 9, 11).fin == 1
    with pytest.raises(VelaInvalidaError, match="fuera de rango"):
        v(0, 10, 9, 9, 10)
    with pytest.raises(VelaInvalidaError, match="fuera de rango"):
        v(0, 10, 12, 11, 10)
    with pytest.raises(VelaInvalidaError, match="entero"):
        Vela(MinutoUtc(0), 1.0, Puntos(1), Puntos(1), Puntos(1), 1)  # type: ignore[arg-type]
    with pytest.raises(VelaInvalidaError, match="entero"):
        Vela(MinutoUtc(0), True, Puntos(1), Puntos(1), Puntos(1), 1)  # type: ignore[arg-type]
    with pytest.raises(VelaInvalidaError, match="entero"):
        Vela(MinutoUtc(0), Puntos(1), Puntos(1), Puntos(1), Puntos(1), 1.0)  # type: ignore[arg-type]
    with pytest.raises(VelaInvalidaError, match="negativo"):
        v(0, 1, 1, 1, 1, -1)
    with pytest.raises(VelaInvalidaError, match="positivo"):
        v(0, 1, 1, 1, 1, 1, 0)
    with pytest.raises(VelaInvalidaError, match="1970"):
        v(-1, 1, 1, 1, 1)
    with pytest.raises(VelaInvalidaError, match="n_m1"):
        Vela(MinutoUtc(0), Puntos(1), Puntos(1), Puntos(1), Puntos(1), 1, 1, 2)
    with pytest.raises(VelaInvalidaError, match="booleano"):
        Vela(MinutoUtc(0), Puntos(1), Puntos(1), Puntos(1), Puntos(1), 1, 1, 1, 1)  # type: ignore[arg-type]
    with pytest.raises(VelaInvalidaError, match="desordenadas"):
        SerieVelas("X", 1, 1, 1, (v(1, 1, 1, 1, 1), v(0, 1, 1, 1, 1)))
    with pytest.raises(VelaInvalidaError, match="positivo"):
        SerieVelas("X", 1, 0, 1, ())


def test_combinar() -> None:
    velas = [v(0, 10, 12, 9, 11, 1), v(1, 11, 15, 10, 14, 2), v(2, 14, 14, 8, 9, 3)]
    c = combinar(velas, MinutoUtc(0), 15, completa=False)
    assert (c.abierta, c.maxima, c.minima, c.cierre, c.volumen, c.duracion_min) == (
        10,
        15,
        8,
        9,
        6,
        15,
    )
    assert c.n_m1 == 3 and c.completa is False
    with pytest.raises(VelaInvalidaError, match="vacia"):
        combinar([], MinutoUtc(0), 15)
    with pytest.raises(VelaInvalidaError, match="desordenadas"):
        combinar([velas[1], velas[0]], MinutoUtc(0), 15)
    with pytest.raises(VelaInvalidaError, match="fuera del periodo"):
        combinar(velas, MinutoUtc(1), 15)
    with pytest.raises(VelaInvalidaError, match="fuera del periodo"):
        combinar(velas, MinutoUtc(0), 2)


def test_conversion_de_instantes() -> None:
    m = a_minuto(datetime(2026, 7, 2, 9, 30, tzinfo=UTC))
    assert formato_ts(m) == "2026-07-02T09:30Z" and parse_ts("2026-07-02T09:30Z") == m
    assert a_datetime(m) == datetime(2026, 7, 2, 9, 30, tzinfo=UTC)
    with pytest.raises(ValueError, match="huso"):
        a_minuto(datetime(2026, 7, 2, 9, 30))
    with pytest.raises(ValueError, match="minuto exacto"):
        a_minuto(datetime(2026, 7, 2, 9, 30, 5, tzinfo=UTC))
    with pytest.raises(VelasCsvError, match="ts_utc invalido"):
        parse_ts("2026-07-02 09:30")


def test_csv_ida_y_vuelta_determinista(tmp_path: Path) -> None:
    velas = [v(29_000_000, 115059, 115070, 115050, 115060, 92700), v(29_000_001, 1, 2, 0, 1, 0)]
    texto = escribir_csv(velas)
    assert texto.startswith("ts_utc,abierta,maxima,minima,cierre,volumen\n")
    assert "\r" not in texto and texto == escribir_csv(velas)
    assert leer_csv(texto) == velas
    ruta = tmp_path / "m1.csv"
    escribir_fichero(ruta, velas)
    assert ruta.read_bytes() == texto.encode("utf-8")
    assert leer_fichero(ruta) == velas
    # Agregadas: duracion, n_m1 y completa viajan en el fichero; una agregada no cabe en un CSV M1.
    agregada = combinar(velas, MinutoUtc(29_000_000), 15, completa=False)
    texto_agg = escribir_csv([agregada], agregadas=True)
    assert texto_agg.splitlines()[0].endswith(",duracion_min,n_m1,completa")
    assert leer_csv(texto_agg) == [agregada]
    with pytest.raises(VelasCsvError, match="no es M1"):
        escribir_csv([agregada])


@pytest.mark.parametrize(
    ("texto", "mensaje"),
    [
        ("a,b\n", "cabecera"),
        ("ts_utc,abierta,maxima,minima,cierre,volumen\n2026-07-02T09:30Z,1,2\n", "columnas"),
        (
            "ts_utc,abierta,maxima,minima,cierre,volumen\n2026-07-02T09:30Z,1,2,0,1,1\n"
            "2026-07-02T09:30Z,1,2,0,1,1\n",
            "duplicadas",
        ),
        (
            "ts_utc,abierta,maxima,minima,cierre,volumen\n2026-07-02T09:31Z,1,2,0,1,1\n"
            "2026-07-02T09:30Z,1,2,0,1,1\n",
            "desordenadas",
        ),
        (
            "ts_utc,abierta,maxima,minima,cierre,volumen\n2026-07-02T09:30Z,1.5,2,0,1,1\n",
            "invalido",
        ),
        ("ts_utc,abierta,maxima,minima,cierre,volumen\n2026-07-02T09:30Z,3,2,0,1,1\n", "rango"),
        ("ts_utc,abierta,maxima,minima,cierre,volumen\n2026-07-02T09:30Z,1,2,0,1,x\n", "invalido"),
        ("ts_utc,abierta,maxima,minima,cierre,volumen\n2026-07-02T09:30Z, 1,2,0,1,1\n", "invalido"),
        ("ts_utc,abierta,maxima,minima,cierre,volumen\n2026-07-02T09:30Z,+1,2,0,1,1\n", "invalido"),
        (
            "ts_utc,abierta,maxima,minima,cierre,volumen,duracion_min,n_m1,completa\n"
            "2026-07-02T09:30Z,1,2,0,1,1,15,1,2\n",
            "0 o 1",
        ),
    ],
)
def test_csv_rechazos(texto: str, mensaje: str) -> None:
    with pytest.raises(VelasCsvError, match=mensaje):
        leer_csv(texto)


def test_csv_con_crlf_o_no_utf8_rechazado(tmp_path: Path) -> None:
    ruta = tmp_path / "m1.csv"
    ruta.write_bytes(b"ts_utc,abierta,maxima,minima,cierre,volumen\r\n")
    with pytest.raises(VelasCsvError, match="CR"):
        leer_fichero(ruta)
    ruta.write_bytes("ts_utc,abierta,maxima,minima,cierre,volumen\n".encode("utf-16"))
    with pytest.raises(VelasCsvError, match="UTF-8"):
        leer_fichero(ruta)
    ruta.write_bytes("\ufeffts_utc,abierta,maxima,minima,cierre,volumen\n".encode())
    with pytest.raises(VelasCsvError, match="BOM"):
        leer_fichero(ruta)


@given(
    inicio=st.integers(min_value=0, max_value=40_000_000),
    precios=st.lists(st.integers(min_value=0, max_value=10_000_000), min_size=4, max_size=4),
)
def test_csv_conserva_cualquier_vela_valida(inicio: int, precios: list[int]) -> None:
    lo, hi = min(precios), max(precios)
    vela = Vela(
        MinutoUtc(inicio), Puntos(precios[0]), Puntos(hi), Puntos(lo), Puntos(precios[1]), 7
    )
    assert leer_csv(escribir_csv([vela])) == [vela]
