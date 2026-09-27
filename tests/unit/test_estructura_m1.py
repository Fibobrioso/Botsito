"""La geometria de la zona de entrada en M1 (domain/estructura_m1.py) sobre M1 SINTETICAS: la
referencia del breaker, la ruptura con mecha o con cuerpo, el bloque de origen, las zonas de
control del retroceso (cero, una, dos), las dos lecturas documentadas de «limpia» de A-21, sin
mirar al futuro, y las guardias."""

from __future__ import annotations

import pytest

from botsito.domain.estructura_m1 import (
    COMPRA,
    CUERPO,
    MECHA,
    PRIMER_ESQUEMA,
    SEGUNDO_ESQUEMA,
    SIN_MECHA_MAS_ALLA_DEL_EXTREMO,
    SOLO_UNA_ZONA_DE_CONTROL,
    VENTA,
    EstructuraError,
    bloque_de_origen,
    detectar_esquema,
    referencia_del_breaker,
    zonas_de_control,
)
from botsito.domain.valores import Puntos
from botsito.domain.velas import MinutoUtc, Vela

T0 = 31_500_000


def _v(n: int, a: int, c: int, lo: int | None = None, hi: int | None = None) -> Vela:
    return Vela(
        MinutoUtc(T0 + n),
        Puntos(a),
        Puntos(hi if hi is not None else max(a, c) + 1),
        Puntos(lo if lo is not None else min(a, c) - 1),
        Puntos(c),
        1,
    )


def _serie(pasos: list[tuple[int, int] | tuple[int, int, int | None, int | None]]) -> list[Vela]:
    velas = []
    for n, paso in enumerate(pasos):
        a, c = paso[0], paso[1]
        lo = paso[2] if len(paso) > 2 else None
        hi = paso[3] if len(paso) > 3 else None
        velas.append(_v(n, a, c, lo, hi))
    return velas


# Una compra tras tomar la liquidez: un tramo previo que deja un ALTO de M1 en 1120 (la referencia),
# la bajada que toma la liquidez (la toma es la vela 4), y despues el impulso.
PREVIO: list[tuple[int, int] | tuple[int, int, int | None, int | None]] = [
    (1000, 1050),
    (1050, 1100),
    (1100, 1119, None, 1120),  # el maximo de la racha verde: 1120
    (1119, 1060),  # roja: forma el ALTO en 1120
    (1060, 990),  # roja: la toma (cierra bajo la liquidez)
]
TOMA = 4


def test_la_referencia_del_breaker_es_el_ultimo_pivote_contrario_a_la_entrada() -> None:
    m1 = _serie(PREVIO)
    assert referencia_del_breaker(m1, TOMA + 1, COMPRA) == 1120
    assert referencia_del_breaker(m1, TOMA + 1, VENTA) is None  # no hay ningun BAJO formado
    assert referencia_del_breaker(m1, 0, COMPRA) is None


def test_primer_esquema_rompe_directo_y_el_bloque_es_la_ultima_contraria() -> None:
    """Dos rojas mas tras la toma (la ultima es el bloque), y tres verdes; la tercera pasa 1120
    con la mecha: primer esquema, cero zonas de control, la zona es el rango de la ultima roja."""
    m1 = _serie(
        [
            *PREVIO,
            (990, 980, 978, None),
            (980, 970, 966, 982),
            (970, 1030),
            (1030, 1090),
            (1090, 1119, None, 1125),
        ]
    )
    e = detectar_esquema(m1, TOMA, COMPRA, MECHA, 1, SOLO_UNA_ZONA_DE_CONTROL)
    assert e is not None
    assert e.cual == PRIMER_ESQUEMA and e.lado == COMPRA and e.zonas_de_control == 0
    assert (e.entrada, e.extremo, e.caja) == (982, 966, 16)
    assert e.referencia == 1120 and e.breaker_fin == m1[-1].fin
    assert (e.bloque_inicio, e.bloque_fin) == (m1[6].inicio, m1[6].fin)
    assert bloque_de_origen(m1, len(m1) - 1, COMPRA) == (6, 7)
    # con cuerpo no rompe todavia: la ultima cierra en 1119
    assert detectar_esquema(m1, TOMA, COMPRA, CUERPO, 1, SOLO_UNA_ZONA_DE_CONTROL) is None
    m1_cuerpo = [*m1[:-1], _v(len(m1) - 1, 1090, 1121)]
    ec = detectar_esquema(m1_cuerpo, TOMA, COMPRA, CUERPO, 1, SOLO_UNA_ZONA_DE_CONTROL)
    assert ec is not None and ec.cual == PRIMER_ESQUEMA


def test_segundo_esquema_con_una_zona_de_control_y_mas_de_una_invalida() -> None:
    una = _serie(
        [
            *PREVIO,
            (990, 980),  # roja tras la toma
            (980, 1040),  # primer impulso
            (1040, 1020),  # retroceso: dos rojas
            (1020, 1010, 1005, None),
            (1010, 1060),  # verde: forma el BAJO del retroceso (una zona de control)
            (1060, 1119, None, 1125),  # breaker con mecha
        ]
    )
    e = detectar_esquema(una, TOMA, COMPRA, MECHA, 1, SOLO_UNA_ZONA_DE_CONTROL)
    assert e is not None and e.cual == SEGUNDO_ESQUEMA and e.zonas_de_control == 1
    assert (e.entrada, e.extremo) == (1021, 1005)  # la ultima roja del retroceso
    assert zonas_de_control(una, TOMA, len(una) - 1, COMPRA) == 1
    dos = _serie(
        [
            *PREVIO,
            (990, 1040),
            (1040, 1020),
            (1020, 1060),  # primera zona
            (1060, 1045),
            (1045, 1080),  # segunda zona
            (1080, 1119, None, 1125),
        ]
    )
    assert zonas_de_control(dos, TOMA, len(dos) - 1, COMPRA) == 2
    assert detectar_esquema(dos, TOMA, COMPRA, MECHA, 1, SOLO_UNA_ZONA_DE_CONTROL) is None
    assert detectar_esquema(dos, TOMA, COMPRA, MECHA, 2, SOLO_UNA_ZONA_DE_CONTROL) is not None


def test_las_dos_lecturas_de_limpia_difieren_solo_si_una_mecha_pasa_el_extremo() -> None:
    limpio = _serie(
        [*PREVIO, (990, 980, 966, 991), (980, 1030), (1030, 1090), (1090, 1119, None, 1125)]
    )
    for lectura in (SOLO_UNA_ZONA_DE_CONTROL, SIN_MECHA_MAS_ALLA_DEL_EXTREMO):
        e = detectar_esquema(limpio, TOMA, COMPRA, MECHA, 1, lectura)
        assert e is not None and (e.entrada, e.extremo) == (991, 966), lectura
    # la primera verde del impulso baja con la mecha por debajo del extremo del bloque (966)
    sucio = _serie(
        [
            *PREVIO,
            (990, 980, 966, 991),
            (980, 1030, 960, None),
            (1030, 1090),
            (1090, 1119, None, 1125),
        ]
    )
    assert detectar_esquema(sucio, TOMA, COMPRA, MECHA, 1, SOLO_UNA_ZONA_DE_CONTROL) is not None
    assert detectar_esquema(sucio, TOMA, COMPRA, MECHA, 1, SIN_MECHA_MAS_ALLA_DEL_EXTREMO) is None


def test_una_venta_es_el_espejo() -> None:
    previo: list[tuple[int, int] | tuple[int, int, int | None, int | None]] = [
        (1000, 950),
        (950, 900),
        (900, 881, 880, None),
        (881, 940),
        (940, 1010),
    ]  # toma arriba
    m1 = _serie([*previo, (1010, 1020, None, 1024), (1020, 960), (960, 900), (900, 881, 875, None)])
    e = detectar_esquema(m1, 4, VENTA, MECHA, 1, SOLO_UNA_ZONA_DE_CONTROL)
    assert e is not None and e.lado == VENTA and e.cual == PRIMER_ESQUEMA
    assert e.referencia == 880 and (e.entrada, e.extremo) == (1009, 1024)


def test_sin_mirar_al_futuro_el_esquema_aparece_en_el_cierre_del_breaker_y_no_antes() -> None:
    m1 = _serie(
        [
            *PREVIO,
            (990, 980, 966, 991),
            (980, 1030),
            (1030, 1090),
            (1090, 1119, None, 1125),
            (1119, 1150),
        ]
    )
    for n in range(TOMA + 1, len(m1) + 1):
        e = detectar_esquema(m1[:n], TOMA, COMPRA, MECHA, 1, SOLO_UNA_ZONA_DE_CONTROL)
        assert (e is not None) == (n >= 9), n  # la vela 8 (indice) es el breaker: n = 9 velas
    e = detectar_esquema(m1, TOMA, COMPRA, MECHA, 1, SOLO_UNA_ZONA_DE_CONTROL)
    assert e is not None and e.breaker_fin == m1[8].fin


def test_las_guardias() -> None:
    m1 = _serie(PREVIO)
    with pytest.raises(EstructuraError, match="A-21"):
        detectar_esquema(m1, TOMA, COMPRA, MECHA, 1, "al_ojo")
    with pytest.raises(EstructuraError, match="lado"):
        detectar_esquema(m1, TOMA, "largo", MECHA, 1, SOLO_UNA_ZONA_DE_CONTROL)
    with pytest.raises(EstructuraError, match="criterio"):
        detectar_esquema(m1, TOMA, COMPRA, "tick", 1, SOLO_UNA_ZONA_DE_CONTROL)
    with pytest.raises(EstructuraError, match="toma"):
        detectar_esquema(m1, 9, COMPRA, MECHA, 1, SOLO_UNA_ZONA_DE_CONTROL)
    with pytest.raises(EstructuraError, match="tope"):
        detectar_esquema(m1, TOMA, COMPRA, MECHA, -1, SOLO_UNA_ZONA_DE_CONTROL)
