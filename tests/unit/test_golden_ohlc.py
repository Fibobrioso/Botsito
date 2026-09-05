"""Golden: H4 del 2026-07-02 (dia del caso del trader) con los dos anclajes, revisado a mano.

Dos velas se comprobaron de forma independiente en el informe de F15: la primera de Madrid
(22:00Z-02:00Z, solo 00:00-01:59Z presentes: 120 M1, o=113773 h=113857 l=113749 c=113814) y la de
servidor 09:00Z-13:00Z (240 M1, o=114198 h=114727 l=113953 c=114512).
"""

from datetime import date
from pathlib import Path

import pytest

from botsito.data.agregacion import agregar
from botsito.data.dukascopy import descargar_dia
from botsito.data.velas import escribir_csv, leer_fichero
from botsito.domain.valores import HoraLocal

RAIZ = Path(__file__).resolve().parents[1]
FIXTURE = RAIZ / "fixtures" / "ohlc" / "EURUSD_2026-07-02.bi5"
GOLDEN = RAIZ / "golden" / "ohlc"


def _m1() -> list:  # type: ignore[type-arg]
    return list(descargar_dia("F", date(2026, 7, 2), lambda _u: FIXTURE.read_bytes()).velas)


@pytest.mark.golden
@pytest.mark.parametrize(
    ("nombre", "anclaje"),
    [
        ("madrid", HoraLocal("00:00", "Europe/Madrid")),
        ("servidor", HoraLocal("17:00", "America/New_York")),
    ],
)
def test_h4_del_dia_del_caso_coincide_con_el_golden(nombre: str, anclaje: HoraLocal) -> None:
    esperado = GOLDEN / f"EURUSD_2026-07-02_H4_{nombre}.csv"
    salida = agregar(_m1(), 240, anclaje)
    assert escribir_csv(salida, agregadas=True) == esperado.read_bytes().decode("utf-8")
    assert leer_fichero(esperado) == salida


@pytest.mark.golden
def test_velas_comprobadas_a_mano() -> None:
    madrid = agregar(_m1(), 240, HoraLocal("00:00", "Europe/Madrid"))
    v = madrid[0]
    assert (v.n_m1, v.abierta, v.maxima, v.minima, v.cierre) == (
        120,
        113773,
        113857,
        113749,
        113814,
    )
    servidor = agregar(_m1(), 240, HoraLocal("17:00", "America/New_York"))
    v = servidor[3]
    assert (v.n_m1, v.abierta, v.maxima, v.minima, v.cierre) == (
        240,
        114198,
        114727,
        113953,
        114512,
    )
    assert not madrid[-1].completa and not servidor[-1].completa  # el dia termina a medias
