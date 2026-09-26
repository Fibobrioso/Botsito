"""El modelo de llenado (ADR-0051, Fase 3) sobre ticks y velas SINTETICOS de 2030: sin mirar al
futuro; determinismo; una M1 con stop y objetivo a la vez -con ticks gana el orden real, el
respaldo elige el stop-; una limite tocada justo en su precio, a cada lado del spread; un tramo sin
ticks que cae al respaldo y queda marcado; y el hueco que llena el stop a la apertura."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from botsito.data.velas import a_minuto
from botsito.domain.ticks import MS_POR_MINUTO, MilisegundoUtc, Tick
from botsito.domain.valores import Puntos
from botsito.domain.velas import MinutoUtc, Vela
from botsito.engine.llenado import (
    LLENADO,
    OBJETIVO,
    RESPALDO_M1,
    STOP,
    TICKS,
    Configuracion,
    LlenadoError,
    Mercado,
    primer_llenado_limite,
    primera_salida,
    spread_por_hora,
)

SPREAD = 3
M0 = int(a_minuto(datetime(2030, 1, 15, 8, 0, tzinfo=UTC)))  # minuto UTC de las 08:00Z


def _cfg(al_toque: bool = False, deslizamiento: int = 0) -> Configuracion:
    return Configuracion(al_toque, deslizamiento, lambda _m: SPREAD)


def _ms(minuto: int, segundo: int = 0, ms: int = 0) -> int:
    return minuto * MS_POR_MINUTO + segundo * 1000 + ms


def _tick(minuto: int, segundo: int, bid: int, spread: int = SPREAD) -> Tick:
    return Tick(MilisegundoUtc(_ms(minuto, segundo)), Puntos(bid + spread), Puntos(bid), 0, 0)


def _vela(minuto: int, o: int, h: int, low: int, c: int) -> Vela:
    return Vela(MinutoUtc(minuto), Puntos(o), Puntos(h), Puntos(low), Puntos(c), 1)


# --------------------------------------------------------------------------- limites al toque


def test_una_limite_de_compra_se_llena_cuando_el_ask_pasa_su_precio_y_no_al_tocarlo() -> None:
    # ASK = BID + 3: BID 997 -> ASK 1000 (toca), BID 996 -> ASK 999 (pasa)
    ticks = [_tick(M0, 1, 999), _tick(M0, 2, 997), _tick(M0, 3, 996)]
    mercado = Mercado(ticks, [])
    ev = primer_llenado_limite("compra", 1000, _ms(M0), _ms(M0 + 1), mercado, _cfg())
    assert ev is not None and (ev.tipo, ev.instante_ms, ev.precio, ev.fuente) == (
        LLENADO,
        _ms(M0, 3),
        1000,
        TICKS,
    )
    al_toque = primer_llenado_limite("compra", 1000, _ms(M0), _ms(M0 + 1), mercado, _cfg(True))
    assert al_toque is not None and al_toque.instante_ms == _ms(M0, 2)


def test_una_limite_de_venta_mira_el_bid_y_exige_pasarlo() -> None:
    ticks = [_tick(M0, 1, 999), _tick(M0, 2, 1000), _tick(M0, 3, 1001)]
    mercado = Mercado(ticks, [])
    ev = primer_llenado_limite("venta", 1000, _ms(M0), _ms(M0 + 1), mercado, _cfg())
    assert ev is not None and ev.instante_ms == _ms(M0, 3) and ev.precio == 1000
    # con ticks de ASK que pasan pero BID que no, una venta no se llena: mira el BID
    solo_ask = [Tick(MilisegundoUtc(_ms(M0, 1)), Puntos(1010), Puntos(999), 0, 0)]
    assert (
        primer_llenado_limite("venta", 1000, _ms(M0), _ms(M0 + 1), Mercado(solo_ask, []), _cfg())
        is None
    )


def test_el_tick_en_el_que_se_decide_no_cuenta_y_el_fin_de_la_ventana_tampoco() -> None:
    ticks = [_tick(M0, 0, 990), _tick(M0, 30, 990)]
    mercado = Mercado(ticks, [])
    # decidido en el tick de las 08:00:00: ese no llena; el de las 08:00:30, si
    ev = primer_llenado_limite("compra", 1000, _ms(M0, 0), _ms(M0 + 1), mercado, _cfg())
    assert ev is not None and ev.instante_ms == _ms(M0, 30)
    assert primer_llenado_limite("compra", 1000, _ms(M0, 0), _ms(M0, 30), mercado, _cfg()) is None
    assert primer_llenado_limite("compra", 1000, _ms(M0, 30), _ms(M0 + 1), mercado, _cfg()) is None


# ------------------------------------------------------------------- stop y objetivo a la vez


def test_una_m1_con_stop_y_objetivo_a_la_vez() -> None:
    """Larga en 1000, stop 990, objetivo 1010. Los ticks del minuto suben primero al objetivo y
    luego caen al stop: con ticks gana el objetivo (el orden real); el respaldo M1, que solo ve la
    vela, elige el stop."""
    ticks = [_tick(M0, 5, 1005), _tick(M0, 10, 1011), _tick(M0, 40, 989)]
    vela = _vela(M0, 1000, 1011, 989, 995)
    cfg = _cfg()
    con_ticks = primera_salida(
        "compra", 990, 1010, _ms(M0), _ms(M0 + 1), Mercado(ticks, [vela]), cfg
    )
    assert con_ticks is not None and (con_ticks.tipo, con_ticks.instante_ms, con_ticks.precio) == (
        OBJETIVO,
        _ms(M0, 10),
        1010,
    )
    respaldo = primera_salida("compra", 990, 1010, _ms(M0), _ms(M0 + 1), Mercado([], [vela]), cfg)
    assert respaldo is not None and (respaldo.tipo, respaldo.precio, respaldo.fuente) == (
        STOP,
        990,
        RESPALDO_M1,
    )
    assert respaldo.instante_ms == _ms(M0 + 1)  # el CIERRE de la vela
    # el mismo tick que cruza stop y objetivo (hueco): gana el stop, al precio del tick
    salto = [Tick(MilisegundoUtc(_ms(M0, 5)), Puntos(1013), Puntos(985), 0, 0)]
    ev = primera_salida("compra", 990, 1010, _ms(M0), _ms(M0 + 1), Mercado(salto, []), cfg)
    assert ev is not None and (ev.tipo, ev.precio) == (STOP, 985)


def test_una_corta_mira_el_ask_para_el_stop_y_el_objetivo() -> None:
    # corta en 1000, stop 1010, objetivo 990; ASK = BID + 3
    ticks = [_tick(M0, 5, 1006), _tick(M0, 6, 1007), _tick(M0, 7, 986)]
    ev = primera_salida("venta", 1010, 990, _ms(M0), _ms(M0 + 1), Mercado(ticks, []), _cfg())
    assert ev is not None and (ev.tipo, ev.instante_ms, ev.precio) == (STOP, _ms(M0, 6), 1010)
    ticks = [_tick(M0, 5, 988), _tick(M0, 6, 986)]
    ev = primera_salida("venta", 1010, 990, _ms(M0), _ms(M0 + 1), Mercado(ticks, []), _cfg())
    assert ev is not None and (ev.tipo, ev.instante_ms) == (OBJETIVO, _ms(M0, 6))
    with pytest.raises(LlenadoError):
        primera_salida("venta", 990, 1010, _ms(M0), _ms(M0 + 1), Mercado(ticks, []), _cfg())


def test_el_hueco_del_respaldo_llena_el_stop_a_la_apertura_y_el_deslizamiento_fijo_se_suma() -> (
    None
):
    vela = _vela(M0, 980, 990, 975, 985)  # abre por debajo del stop 990
    ev = primera_salida("compra", 990, 1010, _ms(M0), _ms(M0 + 1), Mercado([], [vela]), _cfg())
    assert ev is not None and (ev.tipo, ev.precio, ev.fuente) == (STOP, 980, RESPALDO_M1)
    con_desliz = primera_salida(
        "compra", 990, 1010, _ms(M0), _ms(M0 + 1), Mercado([], [vela]), _cfg(deslizamiento=2)
    )
    assert con_desliz is not None and con_desliz.precio == 978


# --------------------------------------------------------------------- respaldo y marcado


def test_un_tramo_sin_ticks_cae_al_respaldo_y_queda_marcado() -> None:
    """Minuto 0 con ticks que no llenan; minuto 1 SIN ticks con una M1 que si: el evento sale del
    respaldo, marcado, en el cierre de esa vela; y el spread supuesto se aplica al ASK."""
    ticks = [_tick(M0, 10, 1005)]
    m1 = [_vela(M0, 1005, 1006, 1004, 1005), _vela(M0 + 1, 1004, 1005, 996, 1000)]
    mercado = Mercado(ticks, m1)
    ev = primer_llenado_limite("compra", 1000, _ms(M0), _ms(M0 + 2), mercado, _cfg())
    assert ev is not None and (ev.fuente, ev.minuto, ev.instante_ms) == (
        RESPALDO_M1,
        M0 + 1,
        _ms(M0 + 2),
    )
    # con spread supuesto 5, el ASK minimo es 996 + 5 = 1001: no pasa por debajo de 1000
    cfg5 = Configuracion(False, 0, lambda _m: 5)
    assert primer_llenado_limite("compra", 1000, _ms(M0), _ms(M0 + 2), mercado, cfg5) is None
    # y un minuto sin ticks ni M1 no decide nada
    assert primer_llenado_limite("compra", 1000, _ms(M0 + 5), _ms(M0 + 6), mercado, _cfg()) is None


def test_sin_mirar_al_futuro_y_determinista() -> None:
    ticks = [_tick(M0, 5, 1005), _tick(M0, 10, 1011), _tick(M0 + 1, 3, 989), _tick(M0 + 2, 0, 900)]
    m1 = [_vela(M0 + 3, 900, 950, 850, 900)]
    cfg = _cfg()
    completo = Mercado(ticks, m1)
    ev = primera_salida("compra", 990, 1010, _ms(M0), _ms(M0 + 4), completo, cfg)
    assert ev is not None and ev.instante_ms == _ms(M0, 10)
    # recortar todo lo posterior al evento no cambia el evento
    recortado = Mercado([t for t in ticks if t.instante <= ev.instante_ms], [])
    assert primera_salida("compra", 990, 1010, _ms(M0), _ms(M0 + 4), recortado, cfg) == ev
    # y dos veces igual
    assert primera_salida("compra", 990, 1010, _ms(M0), _ms(M0 + 4), completo, cfg) == ev
    ll = primer_llenado_limite("venta", 1010, _ms(M0), _ms(M0 + 4), completo, cfg)
    assert ll == primer_llenado_limite("venta", 1010, _ms(M0), _ms(M0 + 4), completo, cfg)


def test_spread_por_hora_y_ticks_desordenados() -> None:
    spread = spread_por_hora({8: 7}, 4, lambda m: 8 if m == M0 else 9)
    assert spread(MinutoUtc(M0)) == 7 and spread(MinutoUtc(M0 + 1)) == 4
    with pytest.raises(LlenadoError, match="desordenados"):
        Mercado([_tick(M0, 5, 1000), _tick(M0, 4, 1000)], [])
