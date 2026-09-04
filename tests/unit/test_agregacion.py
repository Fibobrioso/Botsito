"""Agregacion con anclaje por reloj de pared: casos sinteticos, propiedades y datos reales de las
semanas de cambio de hora (UE 2026-03-29 y 2025-10-26; EE. UU. 2026-03-08 y 2025-11-02)."""

from datetime import date
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from botsito.data.agregacion import (
    AnclajeError,
    agregar,
    huecos,
    limites_del_dia,
    limites_entre,
)
from botsito.data.dukascopy import descargar_dia
from botsito.data.velas import formato_ts, parse_ts
from botsito.domain.valores import HoraLocal, Puntos
from botsito.domain.velas import MinutoUtc, Vela

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "ohlc"
MADRID = HoraLocal("00:00", "Europe/Madrid")
SERVIDOR = HoraLocal("17:00", "America/New_York")  # 00:00 de servidor (NY + 7 h), ADR-0005
UTC0 = HoraLocal("00:00", "UTC")
H4 = 240
M15 = 15


def m1(ts: str, o: int = 10, h: int = 12, lo: int = 9, c: int = 11, vol: int = 1) -> Vela:
    return Vela(parse_ts(ts), Puntos(o), Puntos(h), Puntos(lo), Puntos(c), vol)


def dia_real(dia: str) -> list[Vela]:
    d = date.fromisoformat(dia)
    return list(
        descargar_dia("F", d, lambda _u: (FIXTURES / f"EURUSD_{dia}.bi5").read_bytes()).velas
    )


def inicios(velas: list[Vela]) -> list[str]:
    return [formato_ts(v.inicio) for v in velas]


def test_limites_h4_madrid_invierno_y_verano() -> None:
    assert [formato_ts(m) for m in limites_del_dia(date(2026, 3, 27), H4, MADRID)] == [
        "2026-03-26T23:00Z",
        "2026-03-27T03:00Z",
        "2026-03-27T07:00Z",
        "2026-03-27T11:00Z",
        "2026-03-27T15:00Z",
        "2026-03-27T19:00Z",
    ]
    assert [formato_ts(m) for m in limites_del_dia(date(2026, 3, 30), H4, MADRID)] == [
        "2026-03-29T22:00Z",
        "2026-03-30T02:00Z",
        "2026-03-30T06:00Z",
        "2026-03-30T10:00Z",
        "2026-03-30T14:00Z",
        "2026-03-30T18:00Z",
    ]


def test_limites_servidor_ny_es_el_cierre_del_mercado() -> None:
    # EST (UTC-5): 17:00 NY = 22:00Z ; EDT (UTC-4): 17:00 NY = 21:00Z
    assert formato_ts(limites_del_dia(date(2026, 3, 6), H4, SERVIDOR)[0]) == "2026-03-06T22:00Z"
    assert formato_ts(limites_del_dia(date(2026, 3, 9), H4, SERVIDOR)[0]) == "2026-03-09T21:00Z"
    assert len(limites_del_dia(date(2026, 3, 9), H4, SERVIDOR)) == 6


def test_dia_de_cambio_primavera_omite_el_instante_inexistente() -> None:
    # 2026-03-29 en Madrid: de 02:00 se salta a 03:00. Con anclaje 02:00 y periodo 1 h, el limite
    # de las 02:00 no existe: quedan 23 limites (23 horas de pared).
    limites = limites_del_dia(date(2026, 3, 29), 60, HoraLocal("02:00", "Europe/Madrid"))
    assert len(limites) == 23
    assert formato_ts(limites[0]) == "2026-03-29T01:00Z"  # 03:00 CEST


def test_dia_de_cambio_otono_produce_los_dos_pliegues() -> None:
    # 2025-10-26 en Madrid: 02:00-03:00 CEST y luego 02:00-03:00 CET. M15 con anclaje 00:00:
    # 96 limites de pared + 4 repetidos = 100, alineados a cuartos de hora UTC sin saltos.
    limites = limites_del_dia(date(2025, 10, 26), M15, MADRID)
    assert len(limites) == 100
    diffs = {int(b) - int(a) for a, b in zip(limites, limites[1:], strict=False)}
    assert diffs == {15}
    assert formato_ts(limites[0]) == "2025-10-25T22:00Z"
    assert formato_ts(limites[-1]) == "2025-10-26T22:45Z"


def test_periodo_y_huso_invalidos() -> None:
    with pytest.raises(AnclajeError, match="dividir 1440"):
        limites_del_dia(date(2026, 7, 2), 7, MADRID)
    with pytest.raises(AnclajeError, match="huso desconocido"):
        limites_del_dia(date(2026, 7, 2), H4, HoraLocal("00:00", "Marte/Olympus"))
    with pytest.raises(AnclajeError, match="nombre IANA exacto"):  # en Windows resolveria
        limites_del_dia(date(2026, 7, 2), H4, HoraLocal("00:00", "Europe/madrid"))
    with pytest.raises(ValueError, match="hora invalida"):
        HoraLocal("25:00", "UTC")
    with pytest.raises(ValueError, match="hora invalida"):
        HoraLocal("0700", "UTC")
    with pytest.raises(ValueError, match="huso invalido"):
        HoraLocal("07:00", "")
    with pytest.raises(AnclajeError, match="desordenadas"):
        agregar([m1("2026-07-02T09:01Z"), m1("2026-07-02T09:00Z")], M15, UTC0)


def test_agregacion_sintetica_m15() -> None:
    velas = [
        m1("2026-07-02T09:00Z", 10, 12, 9, 11, 1),
        m1("2026-07-02T09:07Z", 11, 15, 10, 14, 2),
        m1("2026-07-02T09:14Z", 14, 14, 8, 9, 3),
        m1("2026-07-02T09:15Z", 9, 9, 9, 9, 4),
        m1("2026-07-02T09:44Z", 1, 2, 1, 2, 5),  # 09:30 sin velas: no se inventa
    ]
    salida = agregar(velas, M15, MADRID)
    assert inicios(salida) == ["2026-07-02T09:00Z", "2026-07-02T09:15Z", "2026-07-02T09:30Z"]
    a, b, c = salida
    assert (a.abierta, a.maxima, a.minima, a.cierre, a.volumen, a.duracion_min) == (
        10,
        15,
        8,
        9,
        6,
        15,
    )
    assert (b.volumen, c.volumen) == (4, 5)
    assert agregar([], M15, MADRID) == []


def test_limites_entre_incluye_el_anterior() -> None:
    desde, hasta = parse_ts("2026-07-02T09:07Z"), parse_ts("2026-07-02T09:20Z")
    lims = limites_entre(desde, hasta, M15, UTC0)
    assert [formato_ts(x) for x in lims] == [
        "2026-07-02T09:00Z",
        "2026-07-02T09:15Z",
        "2026-07-02T09:30Z",
    ]


def _cada_4h(primero: str, n: int) -> list[tuple[str, int]]:
    """n limites de 4 h a partir del primero (derivacion independiente de la agregacion)."""
    m = parse_ts(primero)
    return [(formato_ts(m + 240 * k), 240) for k in range(n)]


def _dia_completo(primer_limite: str, dia: str) -> list[tuple[str, int]]:
    """Sesion 00:00Z-23:59Z: 6 velas desde el limite anterior a medianoche + la de las 2x:00Z."""
    return _cada_4h(primer_limite, 7)


def _viernes(primer_limite: str, dia: str) -> list[tuple[str, int]]:
    """Sesion 00:00Z hasta el cierre (17:00 NY): 6 velas."""
    return _cada_4h(primer_limite, 6)


@pytest.mark.parametrize(
    ("dia", "anclaje", "esperado"),
    [
        # Viernes 2026-03-27 (CET; EE. UU. ya en EDT). Sesion 00:00Z-20:59Z.
        (
            "2026-03-27",
            MADRID,
            [
                ("2026-03-26T23:00Z", 240),
                ("2026-03-27T03:00Z", 240),
                ("2026-03-27T07:00Z", 240),
                ("2026-03-27T11:00Z", 240),
                ("2026-03-27T15:00Z", 240),
                ("2026-03-27T19:00Z", 240),
            ],
        ),
        (
            "2026-03-27",
            SERVIDOR,
            [
                ("2026-03-26T21:00Z", 240),
                ("2026-03-27T01:00Z", 240),
                ("2026-03-27T05:00Z", 240),
                ("2026-03-27T09:00Z", 240),
                ("2026-03-27T13:00Z", 240),
                ("2026-03-27T17:00Z", 240),
            ],
        ),
        # Lunes 2026-03-30 (CEST y EDT). Sesion 00:00Z-23:59Z.
        (
            "2026-03-30",
            MADRID,
            [
                ("2026-03-29T22:00Z", 240),
                ("2026-03-30T02:00Z", 240),
                ("2026-03-30T06:00Z", 240),
                ("2026-03-30T10:00Z", 240),
                ("2026-03-30T14:00Z", 240),
                ("2026-03-30T18:00Z", 240),
                ("2026-03-30T22:00Z", 240),
            ],
        ),
        # Viernes 2026-03-06 (CET y EST): el servidor cierra a las 22:00Z.
        (
            "2026-03-06",
            SERVIDOR,
            [
                ("2026-03-05T22:00Z", 240),
                ("2026-03-06T02:00Z", 240),
                ("2026-03-06T06:00Z", 240),
                ("2026-03-06T10:00Z", 240),
                ("2026-03-06T14:00Z", 240),
                ("2026-03-06T18:00Z", 240),
            ],
        ),
        # Domingo 2026-03-08 (EE. UU. cambia a EDT a las 07:00Z): apertura 21:00Z = 17:00 EDT.
        ("2026-03-08", SERVIDOR, [("2026-03-08T21:00Z", 240)]),
        ("2026-03-08", MADRID, [("2026-03-08T19:00Z", 240), ("2026-03-08T23:00Z", 240)]),
        # Lunes 2025-11-03 (EST, CET): servidor 22:00Z.
        (
            "2025-11-03",
            SERVIDOR,
            [
                ("2025-11-02T22:00Z", 240),
                ("2025-11-03T02:00Z", 240),
                ("2025-11-03T06:00Z", 240),
                ("2025-11-03T10:00Z", 240),
                ("2025-11-03T14:00Z", 240),
                ("2025-11-03T18:00Z", 240),
                ("2025-11-03T22:00Z", 240),
            ],
        ),
        # Lunes 2025-10-27 (CET; EE. UU. aun EDT): Madrid 23:00Z, servidor 21:00Z.
        (
            "2025-10-27",
            MADRID,
            [
                ("2025-10-26T23:00Z", 240),
                ("2025-10-27T03:00Z", 240),
                ("2025-10-27T07:00Z", 240),
                ("2025-10-27T11:00Z", 240),
                ("2025-10-27T15:00Z", 240),
                ("2025-10-27T19:00Z", 240),
                ("2025-10-27T23:00Z", 240),
            ],
        ),
        ("2025-10-27", SERVIDOR, _dia_completo("2025-10-26T21:00Z", "2025-10-27")),
        # Viernes 2025-10-24 (CEST, EDT): sesion hasta 20:59Z.
        ("2025-10-24", MADRID, _viernes("2025-10-23T22:00Z", "2025-10-24")),
        ("2025-10-24", SERVIDOR, _viernes("2025-10-23T21:00Z", "2025-10-24")),
        # Viernes 2025-10-31 (CET; EE. UU. aun EDT hasta el 2 nov).
        ("2025-10-31", MADRID, _viernes("2025-10-30T23:00Z", "2025-10-31")),
        ("2025-10-31", SERVIDOR, _viernes("2025-10-30T21:00Z", "2025-10-31")),
        # Lunes 2025-11-03 (CET, EST).
        ("2025-11-03", MADRID, _dia_completo("2025-11-02T23:00Z", "2025-11-03")),
        # Viernes 2026-03-06 (CET, EST): sesion hasta 21:59Z, cierre 22:00Z = 17:00 EST.
        ("2026-03-06", MADRID, _viernes("2026-03-05T23:00Z", "2026-03-06")),
        # Lunes 2026-03-09 (CET; EE. UU. ya EDT): semana de desfase.
        ("2026-03-09", MADRID, _dia_completo("2026-03-08T23:00Z", "2026-03-09")),
        ("2026-03-09", SERVIDOR, _dia_completo("2026-03-08T21:00Z", "2026-03-09")),
        # Lunes 2026-03-30 (CEST, EDT).
        ("2026-03-30", SERVIDOR, _dia_completo("2026-03-29T21:00Z", "2026-03-30")),
    ],
)
def test_h4_reales_en_las_semanas_de_cambio_de_hora(
    dia: str, anclaje: HoraLocal, esperado: list[tuple[str, int]]
) -> None:
    velas = dia_real(dia)
    salida = agregar(velas, H4, anclaje)
    assert [(formato_ts(v.inicio), v.duracion_min) for v in salida] == esperado
    # Ninguna M1 se pierde ni se cuenta dos veces.
    assert sum(v.volumen for v in salida) == sum(v.volumen for v in velas)
    assert max(v.maxima for v in salida) == max(v.maxima for v in velas)
    assert min(v.minima for v in salida) == min(v.minima for v in velas)


def test_semana_completa_no_duplica_ni_pierde_limites() -> None:
    """Viernes + domingo + lunes seguidos: la vela del domingo 21:00Z (servidor) sigue hasta el
    lunes 01:00Z sin cortarse a medianoche UTC."""
    velas = dia_real("2026-03-06") + dia_real("2026-03-08") + dia_real("2026-03-09")
    salida = agregar(velas, H4, SERVIDOR)
    ini = inicios(salida)
    assert ini[6:8] == ["2026-03-08T21:00Z", "2026-03-09T01:00Z"]
    assert all(v.duracion_min == 240 for v in salida)
    domingo = salida[6]
    assert domingo.volumen == sum(
        v.volumen for v in velas if "2026-03-08" in formato_ts(v.inicio)
    ) + sum(
        v.volumen
        for v in velas
        if formato_ts(v.inicio) < "2026-03-09T01:00Z" and "2026-03-09" in formato_ts(v.inicio)
    )


def test_causalidad_truncar_no_cambia_velas_cerradas() -> None:
    velas = dia_real("2026-07-02")
    completo = agregar(velas, H4, MADRID)
    truncado = agregar(velas[:700], H4, MADRID)
    assert truncado[:-1] == completo[: len(truncado) - 1]


def test_huecos() -> None:
    velas = [m1("2026-07-02T09:00Z"), m1("2026-07-02T09:01Z"), m1("2026-07-02T09:05Z")]
    h = huecos(velas)
    assert len(h) == 1 and h[0].minutos == 3 and formato_ts(h[0].desde) == "2026-07-02T09:02Z"
    assert huecos(velas[:2]) == []


@settings(max_examples=60, deadline=None)
@given(
    st.lists(
        st.tuples(
            st.integers(min_value=0, max_value=6 * 60 - 1),
            st.lists(st.integers(min_value=1, max_value=1000), min_size=4, max_size=4),
        ),
        min_size=1,
        max_size=80,
        unique_by=lambda t: t[0],
    ),
    st.sampled_from([M15, 60, H4]),
    st.sampled_from([MADRID, SERVIDOR, UTC0]),
)
def test_propiedades_de_agregacion(
    puntos: list[tuple[int, list[int]]], periodo: int, anclaje: HoraLocal
) -> None:
    base = parse_ts("2026-07-02T06:00Z")
    velas = []
    for desplazamiento, p in sorted(puntos):
        lo, hi = min(p), max(p)
        velas.append(
            Vela(
                MinutoUtc(base + desplazamiento),
                Puntos(p[0]),
                Puntos(hi),
                Puntos(lo),
                Puntos(p[1]),
                1,
            )
        )
    salida = agregar(velas, periodo, anclaje)
    assert sum(v.volumen for v in salida) == len(velas)
    assert max(v.maxima for v in salida) == max(v.maxima for v in velas)
    assert min(v.minima for v in salida) == min(v.minima for v in velas)
    assert salida[0].abierta == velas[0].abierta and salida[-1].cierre == velas[-1].cierre
    for a, b in zip(salida, salida[1:], strict=False):
        assert a.fin <= b.inicio
    for v in salida:
        if anclaje is UTC0:
            assert (int(v.inicio) - anclaje.minutos_del_dia) % periodo == 0
