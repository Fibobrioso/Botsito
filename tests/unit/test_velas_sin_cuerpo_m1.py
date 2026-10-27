"""ADR-0085 (sesion 5, S-8, S-19 y S-24): en M1 la vela sin cuerpo no corta la racha, no es
contraria, no forma pivote, no entra en el extremo del punto y no cuenta como alternancia. V, sin
cuerpo, R da el punto en el maximo de la verde (en main, ninguno), con una y con tres; R, sin
cuerpo, V, R da lo mismo que R, V, R (dos zonas, sin esquema; en main, un esquema con una zona);
una vela de 1 punto de cuerpo sigue contando como color; la zona de control posterior salta la vela
sin cuerpo; por el camino real el productor liga la zona del punto que la vela sin cuerpo cortaba;
y las series de M15 no se mueven. Todo sintetico; falla con el codigo de main."""

from __future__ import annotations

from pathlib import Path

import pytest

from botsito.domain.estructura_m1 import (
    COMPRA,
    MECHA,
    SOLO_UNA_ZONA_DE_CONTROL,
    VENTA,
    _recorrer_zona_posterior,
    detectar_esquema,
    referencia_del_breaker,
    ultimo_punto_de_ruptura,
    zonas_de_control,
)
from botsito.domain.pivotes_m15 import (
    ALTO,
    BAJO,
    CIERRE_VELA_CONTRARIA,
    SIN_CUERPO_CORTA,
    SIN_CUERPO_NO_CUENTA,
    PivoteError,
    pivotes_formados,
)
from botsito.domain.velas import Vela
from botsito.engine import zonas
from botsito.engine.interprete import Resultado, Tri
from tests.unit import test_orden_stop_pivote as tosp
from tests.unit.test_a21_series import PREVIO_VENTA, _espejo
from tests.unit.test_estructura_m1 import PREVIO, TOMA, _serie
from tests.unit.test_pivotes_m15 import _m15

RAIZ = Path(__file__).resolve().parents[2]
Paso = tuple[int, int] | tuple[int, int, int | None, int | None]
S10: list[Paso] = [(990, 1040), (1040, 1020), (1020, 1050), (1050, 1030), (1030, 1119, None, 1125)]
CON_DOJI: list[Paso] = [
    (990, 1040), (1040, 1020), (1020, 1020), (1020, 1050), (1050, 1030), (1030, 1119, None, 1125),
]  # fmt: skip


def _m1_de(pasos: list[Paso], lado: str) -> list[Vela]:
    previo = PREVIO if lado == COMPRA else PREVIO_VENTA
    return _serie([*previo, *(pasos if lado == COMPRA else _espejo(pasos))])


@pytest.mark.parametrize("dojis", [1, 3])
@pytest.mark.parametrize("lado", [COMPRA, VENTA])
def test_verde_sin_cuerpo_roja_da_el_punto_en_el_maximo_de_la_verde(lado: str, dojis: int) -> None:
    """ev-v15-004037-a2ab3980 y ev-v15-003959-5898c61e («sean una o tres … en venta lo mismo»):
    el punto es el maximo de la verde, y la vela sin cuerpo no entra en el extremo (su mecha, mas
    alta, no cuenta). En main: ninguno."""
    # la roja con la mecha de arriba en su apertura (1020), para que la vela que marca el nivel
    # sea la verde y no la propia roja
    pasos: list[Paso] = [
        (1000, 1020), *[(1020, 1020, None, 1030)] * dojis, (1020, 1005, None, 1020),
    ]  # fmt: skip
    m1 = _serie(pasos if lado == COMPRA else _espejo(pasos))
    punto = ultimo_punto_de_ruptura(m1, lado)
    assert punto is not None
    assert punto.nivel == (1021 if lado == COMPRA else 2100 - 1021)  # el extremo de la verde
    assert punto.marca == 0  # la verde, no la vela sin cuerpo (mecha 1030) ni la roja
    # la referencia del breaker, por el mismo camino
    assert referencia_del_breaker(m1, len(m1), lado) == punto.nivel
    # y con el argumento de M15 (`corta_la_racha`), lo de antes: ninguno
    assert (
        pivotes_formados(
            m1, None, CIERRE_VELA_CONTRARIA, int(m1[-1].fin), sin_cuerpo=SIN_CUERPO_CORTA
        )
        == []
    )


@pytest.mark.parametrize("lado", [COMPRA, VENTA])
def test_roja_sin_cuerpo_verde_roja_da_lo_mismo_que_roja_verde_roja(lado: str) -> None:
    """ev-v16-000851-f5ae3b6f: la vela sin cuerpo no cuenta como alternancia. La fila del doji de
    test_a21_series.py daba en main un esquema con una zona; ahora dos zonas y ninguno, como
    S-10."""
    con, sin = _m1_de(CON_DOJI, lado), _m1_de(S10, lado)
    assert zonas_de_control(con, TOMA, len(con) - 1, lado) == 2
    assert zonas_de_control(sin, TOMA, len(sin) - 1, lado) == 2
    assert detectar_esquema(con, TOMA, lado, MECHA, 1, SOLO_UNA_ZONA_DE_CONTROL) is None
    assert detectar_esquema(sin, TOMA, lado, MECHA, 1, SOLO_UNA_ZONA_DE_CONTROL) is None


@pytest.mark.parametrize("lado", [COMPRA, VENTA])
def test_una_vela_de_un_punto_de_cuerpo_sigue_contando_como_color(lado: str) -> None:
    """DECISION DEL CONSULTOR (ADR-0085 §3): la de 1 punto es de su color (S-24: vale para trazar
    el punto), aunque ev-v16-000851 diga que tampoco cuenta; la tension va a la sesion 6."""
    pasos: list[Paso] = [(1000, 1020), (1020, 1021), (1021, 1005)]  # V, V de 1 punto, R
    m1 = _serie(pasos if lado == COMPRA else _espejo(pasos))
    punto = ultimo_punto_de_ruptura(m1, lado)
    assert punto is not None and punto.nivel == (1022 if lado == COMPRA else 2100 - 1022)
    # y en el retroceso, la de 1 punto alterna: R, V(1 punto), R y breaker -> dos zonas, sin esquema
    retro: list[Paso] = [
        (990, 1040),
        (1040, 1020),
        (1020, 1021),
        (1021, 1005),
        (1005, 1119, None, 1125),
    ]
    m1 = _m1_de(retro, lado)
    assert zonas_de_control(m1, TOMA, len(m1) - 1, lado) == 2
    assert detectar_esquema(m1, TOMA, lado, MECHA, 1, SOLO_UNA_ZONA_DE_CONTROL) is None


def test_la_zona_de_control_posterior_salta_la_vela_sin_cuerpo() -> None:
    """ADR-0061 §4 lee la zona posterior con la misma geometria: V, V, sin cuerpo, R, V(rompe) da
    el mismo extremo que V, V, R, V(rompe). En main el doji cortaba la racha y la R no dejaba
    extremo: (None, None)."""
    con = _serie([(1000, 1010), (1010, 1020), (1020, 1020), (1020, 1012), (1012, 1030)])
    sin = _serie([(1000, 1010), (1010, 1020), (1020, 1012), (1012, 1030)])
    assert _recorrer_zona_posterior(con, COMPRA, MECHA) == (4, 1021)
    assert _recorrer_zona_posterior(sin, COMPRA, MECHA) == (3, 1021)
    # en venta, en espejo
    con_v = _serie(_espejo([(1000, 1010), (1010, 1020), (1020, 1020), (1020, 1012), (1012, 1030)]))
    assert _recorrer_zona_posterior(con_v, VENTA, MECHA) == (4, 2100 - 1021)


def test_por_el_camino_real_el_productor_liga_la_zona_del_punto(tmp_path: Path) -> None:
    """`zona_del_punto` (engine/zonas.py) con el registro real: en una venta, R, R, sin cuerpo, V
    forma el BAJO en el minimo de las rojas y el productor liga su zona en el cierre de la verde;
    en main no habia punto y `toca_colocar_orden_limite` daba NO."""
    reg = tosp._registro(tmp_path)
    datos = tosp._Datos(tosp._serie([1000, 990, 980, 980, 985]), toma=tosp.M0 + 1)
    estado = tosp._estado()
    toca = zonas.primitivas_zona(reg, SOLO_UNA_ZONA_DE_CONTROL)["toca_colocar_orden_limite"]
    args = {"momento": "orden_limite_nace", "liga": "Z"}
    assert toca(args, tosp._momento(datos, 0), estado) == Resultado(Tri.NO)
    r = toca(args, tosp._momento(datos, 4), estado)
    assert isinstance(r, Resultado) and r.valor is Tri.SI
    z = zonas.zonas_del_dia(estado)[r.ligaduras["Z"]]
    assert z.lado == VENTA and z.entrada == 979 and z.extremo > z.entrada


def test_las_series_de_m15_no_se_mueven() -> None:
    """El otro marco: pivotes_m15 sigue con `corta_la_racha` por defecto (V, doji, R no forma
    pivote), y solo con `no_cuenta` lo formaria; un valor fuera de las dos lecturas se niega."""
    con_doji = [_m15(0, 100, 110), _m15(1, 110, 110), _m15(2, 110, 100)]
    t = int(con_doji[-1].fin)
    assert pivotes_formados(con_doji, None, CIERRE_VELA_CONTRARIA, t) == []
    (p,) = pivotes_formados(
        con_doji, None, CIERRE_VELA_CONTRARIA, t, sin_cuerpo=SIN_CUERPO_NO_CUENTA
    )
    assert p.lado == ALTO and p.nivel == 112
    bajista = [_m15(0, 130, 120), _m15(1, 120, 120), _m15(2, 120, 128)]
    assert pivotes_formados(bajista, None, CIERRE_VELA_CONTRARIA, t) == []
    (q,) = pivotes_formados(
        bajista, None, CIERRE_VELA_CONTRARIA, t, sin_cuerpo=SIN_CUERPO_NO_CUENTA
    )
    assert q.lado == BAJO and q.nivel == 118
    with pytest.raises(PivoteError, match="sin cuerpo"):
        pivotes_formados(con_doji, None, CIERRE_VELA_CONTRARIA, t, sin_cuerpo="a_ojo")
