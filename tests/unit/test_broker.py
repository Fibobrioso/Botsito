"""El broker simulado (ADR-0052, Fase 4) sobre ticks y velas SINTETICOS de 2030: el ciclo de vida
completo de una orden (colocada, modificada, llenada, cancelada, expirada), la posicion que se
cierra por stop, por objetivo o a mercado, los rechazos por limite del perfil registrados, la
coherencia entre la cuenta y el broker (equity = saldo + flotante en cada marca), los hechos de
origen broker, el respaldo M1 marcado, la comision por lado y el swap por corte diario, y el
determinismo. Sin cifras reales: contrato 1 y escala 1, y el P/L es la diferencia de puntos."""

from __future__ import annotations

import dataclasses
from datetime import UTC, datetime
from decimal import Decimal
from zoneinfo import ZoneInfo

import pytest

from botsito.data.velas import a_minuto
from botsito.domain.ticks import MS_POR_MINUTO, MilisegundoUtc, Tick
from botsito.domain.valores import Porcentaje, Puntos
from botsito.domain.velas import MinutoUtc, Vela
from botsito.engine.broker import (
    CANCELADA,
    COLOCADA,
    EXPIRADA,
    HECHO_OPERACION_ABIERTA,
    HECHO_ORDEN_PENDIENTE,
    LLENADA,
    MANUAL,
    MODIFICADA,
    RECHAZADA,
    Broker,
    BrokerError,
    Rechazo,
    ReglasBroker,
)
from botsito.engine.cuenta import EstadoCuenta, ReglasFase, evaluar_fase
from botsito.engine.llenado import OBJETIVO, RESPALDO_M1, STOP, TICKS, Configuracion, Mercado

SPREAD = 3
UNO = Decimal(1)
HUSO = ZoneInfo("America/New_York")
M0 = int(a_minuto(datetime(2030, 1, 15, 8, 0, tzinfo=UTC)))


def _ms(minuto: int, segundo: int = 0) -> int:
    return minuto * MS_POR_MINUTO + segundo * 1000


def _tick(minuto: int, segundo: int, bid: int) -> Tick:
    return Tick(MilisegundoUtc(_ms(minuto, segundo)), Puntos(bid + SPREAD), Puntos(bid), 0, 0)


def _vela(minuto: int, o: int, h: int, low: int, c: int) -> Vela:
    return Vela(MinutoUtc(minuto), Puntos(o), Puntos(h), Puntos(low), Puntos(c), 1)


def _reglas(**cambios: object) -> ReglasBroker:
    base = ReglasBroker(
        volumen_max_lotes=Decimal(10),
        ordenes_simultaneas_max=3,
        posiciones_dia_max=2,
        huso_corte=HUSO,
        comision_por_lote=Decimal(2),
        comision_por_lado=True,
        swap_largo_puntos=Decimal("-5"),
        swap_corto_puntos=Decimal("1"),
    )
    return dataclasses.replace(base, **cambios)  # type: ignore[arg-type]


def _cfg() -> Configuracion:
    return Configuracion(False, 0, lambda _m: SPREAD)


def _broker(ticks: list[Tick], m1: list[Vela] | None = None, **cambios: object) -> Broker:
    return Broker(_reglas(**cambios), _cfg(), Mercado(ticks, m1 or []), UNO, 1)


# ------------------------------------------------------------------------- ciclo de vida


def test_ciclo_de_vida_colocada_modificada_llenada_y_cierre_por_objetivo() -> None:
    # compra limite en 1000: minuto 0 no llega (BID 1000 -> ASK 1003); minuto 1 pasa (BID 995)
    ticks = [
        _tick(M0, 10, 1000),
        _tick(M0 + 1, 5, 995),
        _tick(M0 + 2, 0, 1015),
        _tick(M0 + 3, 0, 1021),
    ]
    b = _broker(ticks)
    o = b.colocar_limite("o1", "compra", 1000, UNO, 990, 1020, _ms(M0))
    assert not isinstance(o, Rechazo) and o.estado == COLOCADA
    assert b.hechos() == {HECHO_OPERACION_ABIERTA: False, HECHO_ORDEN_PENDIENTE: True}
    b.modificar("o1", _ms(M0, 30), objetivo=1020)
    assert b.ordenes["o1"].estado == MODIFICADA
    eventos = b.avanzar(_ms(M0 + 1, 30))
    assert eventos == [(_ms(M0 + 1, 5), LLENADA, "o1", TICKS)]
    assert b.hechos() == {HECHO_OPERACION_ABIERTA: True, HECHO_ORDEN_PENDIENTE: False}
    p = b.posiciones["pos-o1"]
    assert p.entrada == 1000 and p.abierta
    eventos = b.avanzar(_ms(M0 + 4))
    assert eventos == [(_ms(M0 + 3), OBJETIVO, "pos-o1", TICKS)]
    assert p.precio_cierre == 1020 and p.motivo_cierre == OBJETIVO
    ops = b.operaciones_cerradas()
    assert len(ops) == 1 and ops[0].cierre.precio == Decimal(1020)
    assert [(c.concepto, c.importe) for c in ops[0].cargos] == [
        ("comision", Decimal(2)),
        ("comision", Decimal(2)),
    ]
    assert [h for _, h in b.ordenes["o1"].historial] == [COLOCADA, MODIFICADA, LLENADA]


def test_cancelada_expirada_y_cierre_manual() -> None:
    ticks = [_tick(M0, 10, 1000), _tick(M0 + 1, 5, 995), _tick(M0 + 2, 0, 998)]
    b = _broker(ticks)
    b.colocar_limite("c", "compra", 900, UNO, 890, 920, _ms(M0))
    b.cancelar("c", _ms(M0, 20))
    assert b.ordenes["c"].estado == CANCELADA
    with pytest.raises(BrokerError, match="no esta pendiente"):
        b.cancelar("c", _ms(M0, 21))
    b.colocar_limite("e", "compra", 900, UNO, 890, 920, _ms(M0, 25), expira_ms=_ms(M0, 40))
    assert b.avanzar(_ms(M0 + 1)) == [(_ms(M0, 40), EXPIRADA, "e", TICKS)]
    b.colocar_limite("m", "compra", 1000, UNO, 990, 1020, _ms(M0 + 1))
    b.avanzar(_ms(M0 + 1, 30))
    assert b.posiciones["pos-m"].abierta
    p = b.cerrar_a_mercado("pos-m", _ms(M0 + 2, 1))
    assert (p.motivo_cierre, p.precio_cierre, p.fuente_cierre) == (MANUAL, 998, TICKS)
    with pytest.raises(BrokerError, match="no esta abierta"):
        b.cerrar_a_mercado("pos-m", _ms(M0 + 2, 2))


def test_cierre_por_stop_al_precio_del_tick_y_una_venta() -> None:
    # venta limite en 1000 (mira el BID: pasa por encima con 1001); stop 1010 (ASK); objetivo 990
    ticks = [_tick(M0, 5, 1001), _tick(M0 + 1, 0, 1004), _tick(M0 + 1, 30, 1009)]
    b = _broker(ticks)
    b.colocar_limite("v", "venta", 1000, Decimal(2), 1010, 990, _ms(M0))
    b.avanzar(_ms(M0 + 2))
    p = b.posiciones["pos-v"]
    # ASK = BID + 3: 1009 + 3 = 1012 >= 1010: stop al precio del tick (1012), no al nivel
    assert (p.motivo_cierre, p.precio_cierre, p.cerrada_ms) == (STOP, 1012, _ms(M0 + 1, 30))
    op = b.operaciones_cerradas()[0]
    assert op.direccion == "venta" and op.lotes == Decimal(2)


# -------------------------------------------------------------------------- rechazos


def test_los_limites_del_perfil_rechazan_y_quedan_registrados() -> None:
    ticks = [_tick(M0, 5, 995), _tick(M0 + 1, 0, 995), _tick(M0 + 2, 0, 995)]
    b = _broker(ticks)
    r = b.colocar_limite("grande", "compra", 1000, Decimal(11), 990, 1020, _ms(M0))
    assert isinstance(r, Rechazo) and r.motivo == "volumen_max_lotes"
    assert b.ordenes["grande"].estado == RECHAZADA
    for i in range(3):
        assert not isinstance(
            b.colocar_limite(f"o{i}", "compra", 900, UNO, 890, 920, _ms(M0)), Rechazo
        )
    r2 = b.colocar_limite("o3", "compra", 900, UNO, 890, 920, _ms(M0))
    assert isinstance(r2, Rechazo) and r2.motivo == "ordenes_simultaneas_max"
    # posiciones por dia: con dos llenadas hoy, la tercera se rechaza
    b2 = _broker(ticks)
    b2.colocar_limite("a", "compra", 1000, UNO, 990, 1020, _ms(M0))
    b2.colocar_limite("b", "compra", 1000, UNO, 990, 1020, _ms(M0))
    b2.avanzar(_ms(M0 + 1))
    assert sum(1 for p in b2.posiciones.values() if p.abierta) == 2
    r3 = b2.colocar_limite("c", "compra", 1000, UNO, 990, 1020, _ms(M0 + 1))
    assert isinstance(r3, Rechazo) and r3.motivo == "posiciones_dia_max"
    assert [x.motivo for x in b2.traza().rechazos] == ["posiciones_dia_max"]
    with pytest.raises(BrokerError, match="stop < precio < objetivo"):
        b2.colocar_limite("mal", "compra", 1000, UNO, 1010, 1020, _ms(M0 + 1))


# ----------------------------------------------------------------- coherencia con la cuenta


def _reglas_fase(capital: int) -> ReglasFase:
    return ReglasFase(
        "sintetico", "unica", Decimal(capital), HUSO, Porcentaje(50), "saldo_corte_diario",
        Porcentaje(90), False, "equity", None, None, False, None,
    )  # fmt: skip


def test_la_equity_de_la_cuenta_es_el_saldo_mas_el_flotante_del_broker_en_cada_marca() -> None:
    """Una larga que baja y luego cierra por objetivo: en cada marca del broker, la equity que
    la cuenta calcularia (saldo + flotante) coincide con `Broker.flotante()`, y al final la cuenta
    ve el mismo P/L neto que el broker entrego."""
    ticks = [
        _tick(M0, 5, 995),  # llena la compra en 1000 (ASK 998 < 1000)
        _tick(M0 + 1, 0, 992),
        _tick(M0 + 1, 30, 994),
        _tick(M0 + 2, 0, 1005),
        _tick(M0 + 3, 0, 1021),  # objetivo 1020
    ]
    b = _broker(ticks, comision_por_lado=False)
    b.colocar_limite("o", "compra", 1000, Decimal(2), 990, 1020, _ms(M0))
    saldo = Decimal(10_000)
    for hasta in (_ms(M0 + 1), _ms(M0 + 1, 45), _ms(M0 + 2, 30)):
        b.avanzar(hasta)
        p = b.posiciones["pos-o"]
        assert p.abierta
        flot = Decimal(p.ultimo_precio - p.entrada) * p.lotes
        assert b.flotante() == flot
        # el peor precio de cada minuto vivo es lo que la cuenta vigila
        assert all(
            precio
            == min(
                int(t.bid)
                for t in ticks
                if t.instante // MS_POR_MINUTO == ms // MS_POR_MINUTO and t.instante >= p.abierta_ms
            )
            for ms, precio in p.marcas
        )
    b.avanzar(_ms(M0 + 4))
    assert b.flotante() == 0
    op = b.operaciones_cerradas()[0]
    r = evaluar_fase([op], _reglas_fase(10_000), UNO)
    # P/L: (1020 - 1000) * 2 = 40, menos 2 * 2 de comision una vez = 4
    assert r.saldo_final == saldo + 40 - 4 and r.estado is EstadoCuenta.EN_CURSO
    assert r.dias[0].equity_minima == saldo + (992 - 1000) * 2 - 4


def test_el_respaldo_m1_llena_cierra_y_marca_sin_ticks() -> None:
    """Sin ningun tick: la limite se llena en el cierre de la M1 que pasa el precio, el stop salta
    en la M1 que lo toca -pesimista- y todo queda marcado como respaldo."""
    m1 = [
        _vela(M0, 1010, 1012, 1005, 1008),  # ASK minimo 1005 + 3 = 1008: no pasa 1000
        _vela(M0 + 1, 1006, 1007, 996, 1000),  # ASK minimo 999 < 1000: llena al cierre
        _vela(M0 + 2, 1000, 1025, 985, 1000),  # stop 990 y objetivo 1020 en la misma vela: stop
    ]
    b = _broker([], m1)
    b.colocar_limite("o", "compra", 1000, UNO, 990, 1020, _ms(M0))
    b.avanzar(_ms(M0 + 3))
    p = b.posiciones["pos-o"]
    assert (p.abierta_ms, p.fuente_apertura) == (_ms(M0 + 2), RESPALDO_M1)
    assert (p.motivo_cierre, p.precio_cierre, p.fuente_cierre) == (STOP, 990, RESPALDO_M1)
    assert b.traza().por_fuente() == {TICKS: 0, RESPALDO_M1: 2}


def test_swap_por_corte_diario_y_comision_una_vez() -> None:
    """Una larga viva a traves de la medianoche de Nueva York cobra un swap por noche; y con
    comision por operacion completa, un solo cargo."""
    # 15 de enero 04:00Z = 23:00 NY del 14; medianoche NY del 15 = 05:00Z
    m_ini = int(a_minuto(datetime(2030, 1, 15, 4, 0, tzinfo=UTC)))
    m_fin = int(a_minuto(datetime(2030, 1, 15, 6, 0, tzinfo=UTC)))
    ticks = [_tick(m_ini, 5, 995), _tick(m_fin, 0, 1021)]
    b = _broker(ticks, comision_por_lado=False)
    b.colocar_limite("o", "compra", 1000, Decimal(3), 990, 1020, _ms(m_ini))
    b.avanzar(_ms(m_fin + 1))
    op = b.operaciones_cerradas()[0]
    cargos = [(c.concepto, c.importe, c.instante) for c in op.cargos]
    assert cargos[0][:2] == ("comision", Decimal(6))
    assert len(cargos) == 2 and cargos[1][0] == "swap"
    # swap largo -5 puntos/lote/noche * 3 lotes * contrato 1 / escala 1 = cuesta 15
    assert cargos[1][1] == Decimal(15)
    assert cargos[1][2] == datetime(2030, 1, 15, 5, 0, tzinfo=UTC)


def test_determinismo_y_sin_mirar_al_futuro() -> None:
    ticks = [
        _tick(M0, 5, 995),
        _tick(M0 + 1, 0, 992),
        _tick(M0 + 2, 0, 1021),
        _tick(M0 + 5, 0, 900),
    ]

    def correr(hasta: int, con: list[Tick]) -> tuple[object, ...]:
        b = _broker(con)
        b.colocar_limite("o", "compra", 1000, UNO, 990, 1020, _ms(M0))
        b.avanzar(hasta)
        return (b.traza(), tuple(b.operaciones_cerradas()))

    uno, dos = correr(_ms(M0 + 6), ticks), correr(_ms(M0 + 6), ticks)
    assert uno == dos
    # lo decidido hasta el minuto 2 es lo mismo con o sin los ticks posteriores
    corto = correr(_ms(M0 + 3), ticks)
    sin_futuro = correr(_ms(M0 + 3), [t for t in ticks if t.instante < _ms(M0 + 3)])
    assert corto == sin_futuro
    with pytest.raises(BrokerError, match="hacia atras"):
        b = _broker(ticks)
        b.avanzar(_ms(M0 + 2))
        b.avanzar(_ms(M0 + 1))


def test_abrir_conocida_repite_un_llenado_real_y_el_perfil_sigue_mandando() -> None:
    """Una operacion cuyo llenado ya se conoce (el caso del trader) se abre sin pasar por el
    modelo; desde ahi el stop, el objetivo y el cierre a mercado si se deciden con el, y un limite
    del perfil sigue rechazando."""
    ticks = [_tick(M0, 5, 995), _tick(M0 + 1, 0, 1005), _tick(M0 + 2, 0, 1021)]
    b = _broker(ticks)
    p = b.abrir_conocida("real", "compra", 1000, UNO, 990, 1020, _ms(M0, 10), "caso")
    assert p.abierta and p.fuente_apertura == "caso" and b.hechos()[HECHO_OPERACION_ABIERTA]
    b.avanzar(_ms(M0 + 3))
    assert (p.motivo_cierre, p.precio_cierre, p.fuente_cierre) == (OBJETIVO, 1020, TICKS)
    assert b.traza().eventos[0] == (_ms(M0, 10), LLENADA, "real", "caso")
    with pytest.raises(BrokerError, match="volumen_max_lotes"):
        b.abrir_conocida("grande", "compra", 1000, Decimal(11), 990, 1020, _ms(M0 + 3))
    with pytest.raises(BrokerError, match="repetida"):
        b.abrir_conocida("real", "compra", 1000, UNO, 990, 1020, _ms(M0 + 3))
