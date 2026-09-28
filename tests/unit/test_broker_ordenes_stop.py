"""Las ordenes STOP de entrada y el rechazo de pendientes mal colocadas (ADR-0056 §2-3, ADR-0057;
rama `trabajo/broker-ordenes-stop`), sobre ticks y velas SINTETICOS de 2030. Contrato 1 y escala
1: los precios son puntos. El ASK es el BID mas 3."""

from __future__ import annotations

import argparse
import dataclasses
from collections.abc import Callable
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from botsito.data.velas import a_minuto
from botsito.domain.ticks import MS_POR_MINUTO, MilisegundoUtc, Tick
from botsito.domain.valores import Puntos
from botsito.domain.velas import MinutoUtc, Vela
from botsito.engine.broker import (
    COLOCADA,
    LLENADA,
    MOTIVO_PRECIO_INVALIDO,
    MOTIVO_STOPS_LEVEL,
    RECHAZADA,
    Broker,
    BrokerError,
    Orden,
    Rechazo,
    ReglasBroker,
)
from botsito.engine.diagnostico import Diagnostico, nombre_etiquetado
from botsito.engine.llenado import (
    RESPALDO_M1,
    STOP,
    TICKS,
    TIPO_LIMITE,
    TIPO_STOP,
    Configuracion,
    Lado,
    Mercado,
    lado_equivocado,
)

SPREAD = 3
UNO = Decimal(1)
# (id, la forma de colocar, lado, precio, stop, objetivo)
Caso = tuple[str, Callable[..., Orden | Rechazo], Lado, int, int, int]
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
        ordenes_simultaneas_max=10,
        posiciones_dia_max=10,
        huso_corte=ZoneInfo("UTC"),
        comision_por_lote=Decimal(0),
        comision_por_lado=True,
        swap_largo_puntos=Decimal(0),
        swap_corto_puntos=Decimal(0),
    )
    return dataclasses.replace(base, **cambios)  # type: ignore[arg-type]


def _broker(
    ticks: list[Tick],
    m1: list[Vela] | None = None,
    stops_level: int | None = 0,
    deslizamiento: int = 0,
    **cambios: object,
) -> Broker:
    """Por defecto con un stops level de 0 en diagnostico: deja colocar stops sin minimo."""
    return Broker(
        _reglas(**cambios),
        Configuracion(False, deslizamiento, lambda _m: SPREAD),
        Mercado(ticks, m1 or []),
        UNO,
        1,
        stops_level_diagnostico=stops_level,
    )


# ------------------------------------------------------------------ el llenado de una stop


def test_una_venta_stop_salta_cuando_el_bid_toca_el_nivel_y_se_llena_en_ese_tick() -> None:
    ticks = [_tick(M0, 0, 1010), _tick(M0, 20, 1005), _tick(M0, 40, 1000), _tick(M0 + 1, 0, 990)]
    b = _broker(ticks)
    o = b.colocar_stop("v", "venta", 1000, UNO, 1020, 950, _ms(M0, 1))
    assert not isinstance(o, Rechazo) and o.tipo == TIPO_STOP and o.estado == COLOCADA
    assert b.avanzar(_ms(M0 + 1, 30)) == [(_ms(M0, 40), LLENADA, "v", TICKS)]
    p = b.posiciones["pos-v"]
    assert (p.entrada, p.deslizamiento_entrada, p.lado) == (1000, 0, "venta")


def test_una_compra_stop_salta_cuando_el_ask_toca_el_nivel() -> None:
    # compra stop en 1000: el ASK (BID + 3) llega a 1000 con el BID en 997
    ticks = [_tick(M0, 0, 990), _tick(M0, 20, 995), _tick(M0, 40, 997)]
    b = _broker(ticks)
    b.colocar_stop("c", "compra", 1000, UNO, 980, 1060, _ms(M0, 1))
    assert b.avanzar(_ms(M0 + 1)) == [(_ms(M0, 40), LLENADA, "c", TICKS)]
    assert b.posiciones["pos-c"].entrada == 1000


def test_con_hueco_se_llena_al_precio_del_tick_peor_que_el_nivel_y_lo_registra() -> None:
    # el BID salta de 1008 a 994 sin pasar por 1000: la venta se llena a 994, 6 puntos en contra
    ticks = [_tick(M0, 0, 1010), _tick(M0, 20, 1008), _tick(M0, 40, 994)]
    b = _broker(ticks)
    b.colocar_stop("v", "venta", 1000, UNO, 1020, 950, _ms(M0, 1))
    b.avanzar(_ms(M0 + 1))
    p = b.posiciones["pos-v"]
    assert (p.entrada, p.deslizamiento_entrada) == (994, 6)
    # y el deslizamiento fijo de la configuracion (DN-3) se suma en contra
    b2 = _broker(ticks, deslizamiento=2)
    b2.colocar_stop("v", "venta", 1000, UNO, 1020, 950, _ms(M0, 1))
    b2.avanzar(_ms(M0 + 1))
    assert (b2.posiciones["pos-v"].entrada, b2.posiciones["pos-v"].deslizamiento_entrada) == (
        992,
        8,
    )


def test_una_limite_no_desliza() -> None:
    ticks = [_tick(M0, 0, 990), _tick(M0, 20, 995), _tick(M0, 40, 1004)]
    b = _broker(ticks, deslizamiento=2)
    b.colocar_limite("l", "venta", 1000, UNO, 1020, 950, _ms(M0, 1))
    b.avanzar(_ms(M0 + 1))
    assert (b.posiciones["pos-l"].entrada, b.posiciones["pos-l"].deslizamiento_entrada) == (1000, 0)


def test_el_respaldo_m1_llena_al_nivel_o_a_la_apertura_si_la_vela_abre_pasada() -> None:
    velas = [_vela(M0, 1012, 1015, 1008, 1010), _vela(M0 + 1, 1008, 1009, 998, 999)]
    b = _broker([], velas)
    b.colocar_stop("v", "venta", 1000, UNO, 1020, 950, _ms(M0 + 1))
    assert b.avanzar(_ms(M0 + 2)) == [(_ms(M0 + 2), LLENADA, "v", RESPALDO_M1)]
    assert (b.posiciones["pos-v"].entrada, b.posiciones["pos-v"].deslizamiento_entrada) == (1000, 0)
    hueco = [_vela(M0, 1012, 1015, 1008, 1010), _vela(M0 + 1, 995, 996, 990, 991)]
    b2 = _broker([], hueco)
    b2.colocar_stop("v", "venta", 1000, UNO, 1020, 950, _ms(M0 + 1))
    b2.avanzar(_ms(M0 + 2))
    assert (b2.posiciones["pos-v"].entrada, b2.posiciones["pos-v"].deslizamiento_entrada) == (
        995,
        5,
    )


def test_misma_vela_la_stop_sigue_la_convencion_de_la_limite() -> None:
    """Respaldo M1: el llenado se sella al cierre de la vela y la salida solo se mira desde la
    siguiente, igual para una limite que para una stop. Con ticks, el orden real."""
    for tipo, previa in ((TIPO_LIMITE, 990), (TIPO_STOP, 1010)):
        velas = [
            _vela(M0, previa, previa + 1, previa - 1, previa),
            _vela(M0 + 1, 1000, 1025, 995, 1001),  # llena y toca el stop 1020 en la misma vela
            _vela(M0 + 2, 1001, 1003, 999, 1002),  # tranquila
            _vela(M0 + 3, 1002, 1030, 1001, 1028),  # el stop
        ]
        b = _broker([], velas)
        colocar = b.colocar_limite if tipo == TIPO_LIMITE else b.colocar_stop
        colocar("o", "venta", 1000, UNO, 1020, 950, _ms(M0 + 1))
        b.avanzar(_ms(M0 + 3))
        p = b.posiciones["pos-o"]
        assert p.abierta, f"{tipo}: la salida no se mira en la vela del llenado"
        b.avanzar(_ms(M0 + 4))
        assert (p.motivo_cierre, p.cerrada_ms) == (STOP, _ms(M0 + 4)), tipo
    # con ticks: se llena a los 20 s y el stop salta a los 40 s del mismo minuto
    ticks = [_tick(M0, 0, 1010), _tick(M0, 20, 1000), _tick(M0, 40, 1017)]
    b = _broker(ticks)
    b.colocar_stop("v", "venta", 1000, UNO, 1020, 950, _ms(M0, 1))
    eventos = b.avanzar(_ms(M0 + 1))
    assert eventos == [(_ms(M0, 20), LLENADA, "v", TICKS), (_ms(M0, 40), STOP, "pos-v", TICKS)]


# ------------------------------------------------------- el rechazo de las mal colocadas


def test_las_cuatro_pendientes_mal_colocadas_se_rechazan_y_nunca_se_llenan() -> None:
    # cotizacion al colocar: BID 1000, ASK 1003; despues el precio recorre todos los niveles
    ticks = [_tick(M0, 0, 1000), _tick(M0 + 1, 0, 980), _tick(M0 + 2, 0, 1030)]
    b = _broker(ticks)
    mal: list[Caso] = [
        ("vs", b.colocar_stop, "venta", 1005, 1025, 950),  # venta stop por encima del bid
        ("cs", b.colocar_stop, "compra", 1001, 980, 1060),  # compra stop por debajo del ask
        ("vl", b.colocar_limite, "venta", 995, 1015, 950),  # venta limite por debajo del bid
        ("cl", b.colocar_limite, "compra", 1008, 990, 1060),  # compra limite por encima del ask
    ]
    for id, colocar, lado, precio, stop, objetivo in mal:
        r = colocar(id, lado, precio, UNO, stop, objetivo, _ms(M0, 1))
        assert isinstance(r, Rechazo) and r.motivo == MOTIVO_PRECIO_INVALIDO, id
        assert b.ordenes[id].estado == RECHAZADA
    assert not [e for e in b.avanzar(_ms(M0 + 3)) if e[1] == LLENADA]
    assert [r.motivo for r in b.traza().rechazos] == [MOTIVO_PRECIO_INVALIDO] * 4
    assert not b.posiciones


def test_las_bien_colocadas_y_las_del_nivel_exacto_pasan() -> None:
    ticks = [_tick(M0, 0, 1000)]
    b = _broker(ticks)
    bien: list[Caso] = [
        ("vs", b.colocar_stop, "venta", 995, 1015, 950),
        ("cs", b.colocar_stop, "compra", 1008, 990, 1060),
        ("vl", b.colocar_limite, "venta", 1005, 1025, 950),
        ("cl", b.colocar_limite, "compra", 995, 980, 1060),
        ("vl0", b.colocar_limite, "venta", 1000, 1020, 950),  # en el nivel: la limite espera
        ("vs0", b.colocar_stop, "venta", 1000, 1020, 950),  # en el nivel: la stop salta despues
    ]
    for id, colocar, lado, precio, stop, objetivo in bien:
        r = colocar(id, lado, precio, UNO, stop, objetivo, _ms(M0, 1))
        assert not isinstance(r, Rechazo), (id, r)


def test_sin_ticks_la_cotizacion_es_la_ultima_m1_cerrada() -> None:
    velas = [_vela(M0, 1012, 1015, 1008, 1010)]
    b = _broker([], velas)
    r = b.colocar_limite("vl", "venta", 1005, UNO, 1025, 950, _ms(M0 + 1))
    assert isinstance(r, Rechazo) and r.motivo == MOTIVO_PRECIO_INVALIDO
    assert lado_equivocado(TIPO_LIMITE, "venta", 1005, 1010, 1013)


def test_una_modificacion_que_la_cruza_se_rechaza_y_la_orden_sigue_igual() -> None:
    ticks = [_tick(M0, 0, 1000), _tick(M0 + 1, 0, 1004)]
    b = _broker(ticks)
    b.colocar_limite("vl", "venta", 1005, UNO, 1025, 950, _ms(M0, 1))
    r = b.modificar("vl", _ms(M0 + 1, 1), precio=1002)  # el BID ya esta en 1004
    assert isinstance(r, Rechazo) and r.motivo == MOTIVO_PRECIO_INVALIDO
    o = b.ordenes["vl"]
    assert (o.precio, o.estado) == (1005, COLOCADA)


# ------------------------------------------------------------------------- el stops level


def test_sin_stops_level_una_stop_no_se_coloca_y_la_limite_sigue_como_hoy() -> None:
    ticks = [_tick(M0, 0, 1000)]
    b = _broker(ticks, stops_level=None)
    assert b.stops_level is None
    with pytest.raises(BrokerError, match="A-27") as exc:
        b.colocar_stop("vs", "venta", 995, UNO, 1015, 950, _ms(M0, 1))
    assert "--diagnostico-a27" in str(exc.value) and "firma_stops_level_puntos" in str(exc.value)
    # la limite no mira el stops level mientras no se conozca: a un punto del precio, pasa
    assert not isinstance(
        b.colocar_limite("vl", "venta", 1001, UNO, 1021, 950, _ms(M0, 1)), Rechazo
    )


def test_con_stops_level_en_diagnostico_la_distancia_minima_se_exige() -> None:
    ticks = [_tick(M0, 0, 1000)]
    b = _broker(ticks, stops_level=5)
    cerca = b.colocar_stop("a", "venta", 997, UNO, 1017, 950, _ms(M0, 1))  # a 3 del bid
    assert isinstance(cerca, Rechazo) and cerca.motivo == MOTIVO_STOPS_LEVEL
    justo = b.colocar_stop("b", "venta", 995, UNO, 1015, 950, _ms(M0, 1))  # a 5 del bid
    assert not isinstance(justo, Rechazo)
    stop_cerca = b.colocar_stop("c", "venta", 990, UNO, 993, 950, _ms(M0, 1))  # stop a 3
    assert isinstance(stop_cerca, Rechazo) and stop_cerca.motivo == MOTIVO_STOPS_LEVEL
    limite_cerca = b.colocar_limite("d", "venta", 1002, UNO, 1022, 950, _ms(M0, 1))
    assert isinstance(limite_cerca, Rechazo) and limite_cerca.motivo == MOTIVO_STOPS_LEVEL


def test_un_stops_level_fijado_no_admite_diagnostico() -> None:
    with pytest.raises(BrokerError, match="ya esta fijado"):
        _broker([], stops_level=2, stops_level_puntos=3)
    b = _broker([_tick(M0, 0, 1000)], stops_level=None, stops_level_puntos=3)
    assert b.stops_level == 3


def test_la_etiqueta_de_a27_y_la_cli() -> None:
    from botsito.cli import _diagnostico_de

    diag = Diagnostico(a27=5)
    assert diag.etiquetas == ("DIAGNOSTICO-A27-5",) and diag.activo
    assert nombre_etiquetado(Path("x.txt"), diag.etiquetas) == Path("x.DIAGNOSTICO.a27=5.txt")
    assert Diagnostico().etiquetas == ()
    with pytest.raises(ValueError, match="negativo"):
        Diagnostico(a27=-1)
    with pytest.raises(ValueError, match="--simular"):
        _diagnostico_de(argparse.Namespace(diagnostico_a27=5, simular=False))
    assert _diagnostico_de(argparse.Namespace(diagnostico_a27=5, simular=True)).a27 == 5
