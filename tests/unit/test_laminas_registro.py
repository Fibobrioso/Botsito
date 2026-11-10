"""Lo que la rama `trabajo/laminas` anade al dominio como REGISTRO (respuesta del consultor a la
fase 0, puntos 1 y 2): la H4 que fija el sesgo y las que salta, con su motivo, y los pivotes que
cuenta RN-009. Sobre velas SINTETICAS. Lo que se comprueba es que lo que ya habia sale identico:
el sesgo y sus contadores contra una copia literal del `sesgo_h4` de main, y `zonas_de_control`
contra una copia literal de la de main, en los casos de los tests que ya existian y en series al
azar (Hypothesis). La prueba de fondo son F4.1 y F4.2 a 0 bytes."""

from __future__ import annotations

from collections.abc import Sequence

from hypothesis import given, settings
from hypothesis import strategies as st

from botsito.domain.estructura_m1 import (
    COMPRA,
    VENTA,
    _pivotes_m1,
    _signo,
    pivotes_de_control,
    zonas_de_control,
)
from botsito.domain.pivotes_m15 import ALTO, BAJO, color
from botsito.domain.sesgo import (
    CUERPO,
    MECHA,
    SALTADA_COLOR_CONTRARIO,
    SALTADA_NEUTRA_DOBLE,
    SALTADA_NEUTRA_SIMPLE,
    Sesgo,
    _extremos,
    sesgo_h4,
)
from botsito.domain.valores import Puntos
from botsito.domain.velas import MinutoUtc, Vela
from tests.unit.test_estructura_m1 import PREVIO, TOMA, _serie
from tests.unit.test_sesgo_h4 import FIN, H4, TOPE, h4

# ------------------------------------------------------------------ las copias literales de main


def _sesgo_de_main(
    velas_h4: Sequence[Vela], apertura_sesion: MinutoUtc, tope: int, criterio: str
) -> tuple[Sesgo, int | None, int, bool, int, int, int]:
    """`domain.sesgo.sesgo_h4` de main (e5394c5), copiado tal cual salvo que devuelve la tupla de
    los campos que ya habia."""
    cerradas = sorted((v for v in velas_h4 if v.fin <= apertura_sesion), key=lambda v: v.inicio)
    miradas = 0
    saltadas = [0, 0, 0]

    def fija(
        sesgo: Sesgo, puntos: int | None, doble: bool
    ) -> tuple[Sesgo, int | None, int, bool, int, int, int]:
        return (sesgo, puntos, miradas, doble, *saltadas)  # type: ignore[return-value]

    for i in range(len(cerradas) - 1, 0, -1):
        if miradas == tope:
            break
        miradas += 1
        vela = cerradas[i]
        alto, bajo = _extremos(vela, criterio)
        alto_ant, bajo_ant = _extremos(cerradas[i - 1], criterio)
        arriba, abajo = alto - alto_ant, bajo_ant - bajo
        verde, roja = vela.cierre > vela.abierta, vela.cierre < vela.abierta
        if arriba > 0 and abajo > 0:
            if verde:
                return fija(Sesgo.ALCISTA, arriba, True)
            if roja:
                return fija(Sesgo.BAJISTA, abajo, True)
            saltadas[2] += 1
        elif arriba > 0 or abajo > 0:
            if arriba > 0 and verde:
                return fija(Sesgo.ALCISTA, arriba, False)
            if abajo > 0 and roja:
                return fija(Sesgo.BAJISTA, abajo, False)
            saltadas[0 if (verde or roja) else 1] += 1
    return fija(Sesgo.INSUFICIENTE, None, False)


def _zonas_de_main(m1: Sequence[Vela], desde: int, hasta: int, lado: str) -> int:
    """`domain.estructura_m1.zonas_de_control` de main (e5394c5), copiada tal cual."""
    _signo(lado)
    sentido = BAJO if lado == COMPRA else ALTO
    signo = 1 if lado == COMPRA else -1
    if hasta <= desde:
        return 0
    primer_impulso = next((k for k in range(desde + 1, hasta + 1) if color(m1[k]) == signo), None)
    if primer_impulso is None:
        return 0
    instante = int(m1[hasta].fin)
    n = 0
    for p in _pivotes_m1(m1, instante, hasta + 1):
        if p.lado == sentido and int(p.contraria_inicio) > int(m1[primer_impulso].inicio):
            n += 1
    return n


def _como_main(r: object) -> tuple[object, ...]:
    return tuple(
        getattr(r, c)
        for c in (
            "sesgo",
            "ruptura_puntos",
            "velas_miradas",
            "doble_ruptura",
            "saltadas_color_contrario",
            "saltadas_neutras_simples",
            "saltadas_neutras_dobles",
        )
    )


# --------------------------------------------------------------------------------- el sesgo

# Los casos de tests/unit/test_sesgo_h4.py, con sus velas tal cual
CASOS_SESGO: list[tuple[list[Vela], int, int, str]] = [
    ([h4(0, 110, 100), h4(1, 112, 101), h4(2, 111, 99, abierta=110, cierre=102)], FIN, TOPE, MECHA),
    (
        [
            h4(0, 110, 100),
            h4(1, 108, 98, abierta=107, cierre=99),
            h4(2, 111, 103, abierta=104, cierre=109),
        ],
        FIN,
        TOPE,
        MECHA,
    ),
    (
        [
            h4(0, 110, 100, abierta=103, cierre=107),
            h4(1, 112, 101, abierta=102, cierre=109),
            h4(2, 114, 104, abierta=112, cierre=105),
        ],
        FIN,
        TOPE,
        CUERPO,
    ),
    ([h4(0, 110, 100), h4(1, 107, 99, abierta=106, cierre=100), h4(2, 107, 99)], FIN, TOPE, MECHA),
    ([h4(0, 110, 100), h4(1, 112, 99, abierta=105, cierre=105)], 2 * H4, TOPE, MECHA),
    (
        [
            h4(0, 110, 100),
            h4(1, 112, 101),
            h4(2, 115, 98, abierta=105, cierre=105),
            h4(3, 118, 95, abierta=106, cierre=106),
        ],
        4 * H4,
        TOPE,
        MECHA,
    ),
    (
        [
            h4(0, 110, 100),
            h4(1, 112, 101),
            h4(2, 115, 98, abierta=105, cierre=105),
            h4(3, 118, 95, abierta=106, cierre=106),
        ],
        4 * H4,
        2,
        MECHA,
    ),
    ([h4(0, 110, 100), h4(1, 112, 101), h4(2, 111, 102), h4(3, 111, 102)], 4 * H4, 2, MECHA),
    (
        [h4(0, 110, 100, abierta=101, cierre=109), h4(1, 115, 102, abierta=103, cierre=108)],
        2 * H4,
        TOPE,
        CUERPO,
    ),
    ([], FIN, TOPE, MECHA),
]


def test_sobre_los_casos_que_ya_habia_el_sesgo_y_los_contadores_salen_identicos() -> None:
    for velas, apertura, tope, criterio in CASOS_SESGO:
        r = sesgo_h4(velas, MinutoUtc(apertura), tope, criterio)
        assert _como_main(r) == _sesgo_de_main(velas, MinutoUtc(apertura), tope, criterio)


def test_el_registro_dice_la_vela_que_fija_y_cada_saltada_con_su_motivo() -> None:
    # alcista con una saltada por el color: la ultima rompe arriba y cierra roja
    previa = [h4(0, 110, 100, abierta=103, cierre=107), h4(1, 112, 101, abierta=102, cierre=109)]
    r = sesgo_h4([*previa, h4(2, 114, 104, abierta=112, cierre=105)], MinutoUtc(FIN), TOPE, CUERPO)
    assert r.sesgo is Sesgo.ALCISTA and r.vela_que_fija == MinutoUtc(H4)
    assert r.h4_saltadas == ((MinutoUtc(2 * H4), SALTADA_COLOR_CONTRARIO),)
    # dos dobles neutras saltadas, de la mas reciente a la mas antigua
    velas = [
        h4(0, 110, 100),
        h4(1, 112, 101),
        h4(2, 115, 98, abierta=105, cierre=105),
        h4(3, 118, 95, abierta=106, cierre=106),
    ]
    r = sesgo_h4(velas, MinutoUtc(4 * H4), TOPE, MECHA)
    assert r.vela_que_fija == MinutoUtc(H4)
    assert r.h4_saltadas == (
        (MinutoUtc(3 * H4), SALTADA_NEUTRA_DOBLE),
        (MinutoUtc(2 * H4), SALTADA_NEUTRA_DOBLE),
    )
    # una de un extremo sin cuerpo, y el INSUFICIENTE no fija ninguna
    r = sesgo_h4(
        [h4(0, 110, 100), h4(1, 112, 101, abierta=105, cierre=105)], MinutoUtc(2 * H4), TOPE, MECHA
    )
    assert r.sesgo is Sesgo.INSUFICIENTE and r.vela_que_fija is None
    assert r.h4_saltadas == ((MinutoUtc(H4), SALTADA_NEUTRA_SIMPLE),)


_PRECIO = st.integers(min_value=90, max_value=130)


@st.composite
def _velas_h4(draw: st.DrawFn) -> list[Vela]:
    velas = []
    for k in range(draw(st.integers(min_value=0, max_value=9))):
        a, c = draw(_PRECIO), draw(_PRECIO)
        alto = max(a, c) + draw(st.integers(min_value=0, max_value=5))
        bajo = min(a, c) - draw(st.integers(min_value=0, max_value=5))
        velas.append(
            Vela(MinutoUtc(k * H4), Puntos(a), Puntos(alto), Puntos(bajo), Puntos(c), 0, H4, H4)
        )
    return velas


@settings(max_examples=400, deadline=None)
@given(
    velas=_velas_h4(),
    apertura=st.integers(min_value=0, max_value=10 * H4),
    tope=st.integers(min_value=1, max_value=8),
    criterio=st.sampled_from([MECHA, CUERPO]),
)
def test_al_azar_el_sesgo_y_los_contadores_salen_como_en_main_y_el_registro_cuadra(
    velas: list[Vela], apertura: int, tope: int, criterio: str
) -> None:
    r = sesgo_h4(velas, MinutoUtc(apertura), tope, criterio)
    assert _como_main(r) == _sesgo_de_main(velas, MinutoUtc(apertura), tope, criterio)
    motivos = [m for _, m in r.h4_saltadas]
    assert motivos.count(SALTADA_COLOR_CONTRARIO) == r.saltadas_color_contrario
    assert motivos.count(SALTADA_NEUTRA_SIMPLE) == r.saltadas_neutras_simples
    assert motivos.count(SALTADA_NEUTRA_DOBLE) == r.saltadas_neutras_dobles
    con_lado = r.sesgo in (Sesgo.ALCISTA, Sesgo.BAJISTA)
    assert (r.vela_que_fija is not None) == con_lado
    if con_lado:
        assert len(r.h4_saltadas) <= r.velas_miradas - 1
        assert all(int(i) > int(r.vela_que_fija) for i, _ in r.h4_saltadas)  # type: ignore[arg-type]


# ------------------------------------------------------------------- las zonas de control


def _con_zonas(n: int) -> list[Vela]:
    """Las series de tests/unit/test_estructura_m1.py con cero, una y dos zonas de control."""
    tras = {
        0: [
            (990, 980, 978, None),
            (980, 970, 966, 982),
            (970, 1030),
            (1030, 1090),
            (1090, 1119, None, 1125),
        ],
        1: [
            (990, 980),
            (980, 1040),
            (1040, 1020),
            (1020, 1010, 1005, None),
            (1010, 1060),
            (1060, 1119, None, 1125),
        ],
        2: [
            (990, 1040),
            (1040, 1020),
            (1020, 1060),
            (1060, 1045),
            (1045, 1080),
            (1080, 1119, None, 1125),
        ],
    }[n]
    return _serie([*PREVIO, *tras])  # type: ignore[list-item]


def test_cero_una_y_dos_zonas_el_numero_es_el_de_main_y_los_pivotes_son_bajos_del_retroceso() -> (
    None
):
    for n in (0, 1, 2):
        m1 = _con_zonas(n)
        pivotes = pivotes_de_control(m1, TOMA, len(m1) - 1, COMPRA)
        assert len(pivotes) == n == zonas_de_control(m1, TOMA, len(m1) - 1, COMPRA)
        assert _zonas_de_main(m1, TOMA, len(m1) - 1, COMPRA) == n
        assert all(p.lado == BAJO for p in pivotes)
        assert all(
            int(m1[TOMA].inicio) < int(p.contraria_inicio) <= int(m1[-1].inicio) for p in pivotes
        )


@st.composite
def _velas_m1(draw: st.DrawFn) -> list[Vela]:
    velas = []
    precio = 1000
    for k in range(draw(st.integers(min_value=0, max_value=24))):
        c = precio + draw(st.integers(min_value=-30, max_value=30))
        alto = max(precio, c) + draw(st.integers(min_value=0, max_value=6))
        bajo = min(precio, c) - draw(st.integers(min_value=0, max_value=6))
        velas.append(
            Vela(
                MinutoUtc(31_500_000 + k), Puntos(precio), Puntos(alto), Puntos(bajo), Puntos(c), 1
            )
        )
        precio = c
    return velas


@settings(max_examples=400, deadline=None)
@given(
    m1=_velas_m1(),
    desde=st.integers(min_value=0, max_value=24),
    lado=st.sampled_from([COMPRA, VENTA]),
)
def test_al_azar_las_zonas_de_control_salen_como_en_main(
    m1: list[Vela], desde: int, lado: str
) -> None:
    if not m1:
        return
    hasta = len(m1) - 1
    desde = min(desde, hasta)
    n = _zonas_de_main(m1, desde, hasta, lado)
    assert zonas_de_control(m1, desde, hasta, lado) == n
    assert len(pivotes_de_control(m1, desde, hasta, lado)) == n
