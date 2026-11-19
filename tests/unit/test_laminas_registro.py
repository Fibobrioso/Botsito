"""Lo que la rama `trabajo/laminas` anade al dominio como REGISTRO (respuesta del consultor a la
fase 0, puntos 1 y 2): la H4 que fija el sesgo y las que salta, con su motivo, y los pivotes que
cuenta RN-009. Sobre velas SINTETICAS. Lo que se comprueba es que lo que ya habia sale identico:
el sesgo y sus contadores contra una copia literal del `sesgo_h4` de main, y `zonas_de_control`
contra una copia literal de la de main, en los casos de los tests que ya existian y en series al
azar (Hypothesis). La prueba de fondo son F4.1 y F4.2 a 0 bytes."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

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
    ResultadoSesgo,
    Sesgo,
    sesgo_h4,
)
from botsito.domain.valores import Puntos
from botsito.domain.velas import MinutoUtc, Vela
from tests.unit.test_estructura_m1 import PREVIO, TOMA, _serie
from tests.unit.test_sesgo_h4 import FIN, H4, TOPE, h4

# ------------------------------------------------------------------ las copias literales de main


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


def _cuadra(r: ResultadoSesgo) -> None:
    """Lo que el registro tiene que cumplir con la regla del rango vigente (ADR-0094)."""
    motivos = [m for _, m in r.h4_saltadas]
    assert motivos.count(SALTADA_COLOR_CONTRARIO) == r.saltadas_color_contrario
    assert motivos.count(SALTADA_NEUTRA_SIMPLE) == r.saltadas_neutras_simples
    assert motivos.count(SALTADA_NEUTRA_DOBLE) == r.saltadas_neutras_dobles
    con_lado = r.sesgo in (Sesgo.ALCISTA, Sesgo.BAJISTA)
    assert (r.vela_que_fija is not None) == con_lado
    assert (r.ruptura_puntos is not None) == con_lado
    assert len(r.h4_saltadas) <= r.velas_miradas
    fija, puntos = r.vela_que_fija, r.ruptura_puntos
    if fija is not None and puntos is not None:
        # con lado, el rango vigente es la H4 que lo fijo, y las saltadas son posteriores
        assert r.rango_vela == fija
        assert puntos > 0
        assert all(int(i) > int(fija) for i, _ in r.h4_saltadas)
    if r.rango_alto is not None and r.rango_bajo is not None:
        assert r.rango_vela is not None and r.rango_alto >= r.rango_bajo


def test_sobre_los_casos_que_ya_habia_el_registro_cuadra_con_la_regla_del_rango() -> None:
    """Hasta ADR-0094 este test comparaba el sesgo y sus contadores con una copia literal del
    `sesgo_h4` de main (e5394c5); desde la regla del rango vigente el resultado cambia A
    PROPOSITO (trabajo/activar-sesion-07), y lo que se comprueba es que el registro cuadra."""
    for velas, apertura, tope, criterio in CASOS_SESGO:
        _cuadra(sesgo_h4(velas, MinutoUtc(apertura), tope, criterio))


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
def test_al_azar_el_registro_del_sesgo_cuadra_con_la_regla_del_rango(
    velas: list[Vela], apertura: int, tope: int, criterio: str
) -> None:
    """Hasta ADR-0094 comparaba ademas con la copia literal de main (arriba); ya no."""
    _cuadra(sesgo_h4(velas, MinutoUtc(apertura), tope, criterio))


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


# ------------------------------------------------ la respuesta a la PARADA final, punto 4


def test_una_segunda_evaluacion_sin_saltadas_borra_las_de_la_primera() -> None:
    """Dos evaluaciones de `sesgo_h4_al_abrir` en la misma sesion: la primera salta una H4 por el
    color y fija con doble ruptura, la segunda no salta ninguna ni es doble. Despues de la segunda
    no puede quedar ninguna anotacion de la primera: si quedaran la lista y su recuento a la vez,
    casarian y la lamina dibujaria como saltada una H4 que la evaluacion vigente no salto. Con el
    codigo de 675ee62 este test falla (solo se escribian, nunca se borraban)."""
    from botsito.config.registro import cargar_registro
    from botsito.engine.interprete import EstadoDia, Momento
    from botsito.engine.motor import DatosMercado
    from botsito.engine.primitivas import (
        ANOTACION_DOBLE_RUPTURA,
        ANOTACION_SALTADAS_COLOR,
        ANOTACION_SESGO_RANGO,
        ANOTACION_SESGO_SALTADAS,
        ANOTACION_SESGO_VELA,
        primitivas_escritas,
    )

    registro = cargar_registro(
        Path(__file__).resolve().parents[2] / "knowledge" / "spec" / "parametros.yaml"
    )
    sesgo = primitivas_escritas(registro).predicados["sesgo_h4_al_abrir"]
    args = {"que": "vela_h4_cerrada", "contra": "rango_h4_vigente",
            "criterio": "sesgo_h4_criterio_ruptura", "tope": "sesgo_h4_tope_velas",
            "rango_nuevo": "sesgo_h4_rango_nuevo"}  # fmt: skip
    estado = EstadoDia()
    # la primera: la ultima rompe arriba y cierra roja (saltada por el color); la anterior rompe
    # los dos extremos y cierra verde (doble ruptura)
    primera = [
        h4(0, 110, 100),
        h4(1, 112, 99, abierta=101, cierre=108),
        h4(2, 114, 104, abierta=112, cierre=105),
    ]
    sesgo(args, Momento(MinutoUtc(FIN), "07-11", True, DatosMercado(primera)), estado)
    anot = estado.anotaciones["07-11"]
    assert anot[ANOTACION_SALTADAS_COLOR] == "1" and ANOTACION_SESGO_SALTADAS in anot
    assert anot[ANOTACION_DOBLE_RUPTURA] == "si" and ANOTACION_SESGO_VELA in anot
    # la segunda: rompe arriba y cierra verde, de un solo extremo; nada saltado
    segunda = [h4(0, 110, 100), h4(1, 112, 101)]
    sesgo(args, Momento(MinutoUtc(2 * H4), "07-11", True, DatosMercado(segunda)), estado)
    anot = estado.anotaciones["07-11"]
    assert ANOTACION_SALTADAS_COLOR not in anot and ANOTACION_SESGO_SALTADAS not in anot
    assert ANOTACION_DOBLE_RUPTURA not in anot
    assert anot[ANOTACION_SESGO_VELA] == str(H4)
    # ADR-0094: el rango vigente, `alto:bajo:inicio`, es la H4 que fija el sesgo
    assert anot[ANOTACION_SESGO_RANGO] == f"112:101:{H4}"
