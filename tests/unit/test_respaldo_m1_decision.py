"""Z (trabajo/respaldo-m1, ADR-0051 §5 y su NOTA del 2026-10-29): con el respaldo M1 una vela solo
evalua lo que ya estaba decidido cuando EMPEZO. El motor decide en el cierre de la M1 menos 1 ms,
asi que lo que coloca, modifica o mueve en ese cierre no se evalua contra esa vela, cuyos precios
son anteriores a la decision; la vela del stop movido se evalua con el stop ANTERIOR (ADR-0065
§4) y la de una orden modificada, con su version anterior. Con ticks no cambia nada: el tick en
que se decide ya no contaba. Velas y ticks SINTETICOS de 2030; contrato 1 y escala 1.

Los ocho del primer bloque ROMPEN en `main` (que evalua la vela de la decision); los del segundo
pasan en los dos lados: lo que la condicion no puede cambiar."""

from __future__ import annotations

import dataclasses
from datetime import UTC, datetime
from decimal import Decimal
from zoneinfo import ZoneInfo

from botsito.data.velas import a_minuto
from botsito.domain.ticks import MS_POR_MINUTO, MilisegundoUtc, Tick
from botsito.domain.valores import Puntos
from botsito.domain.velas import MinutoUtc, Vela
from botsito.engine.broker import LLENADA, Broker, ReglasBroker
from botsito.engine.llenado import (
    RESPALDO_M1,
    STOP,
    TICKS,
    Configuracion,
    Mercado,
    primer_llenado_limite,
)
from botsito.engine.primitivas_broker import BREAK_EVEN, SALTO_EL_STOP, clasificar_cierre

SPREAD = 3
UNO = Decimal(1)
M0 = int(a_minuto(datetime(2030, 1, 15, 8, 0, tzinfo=UTC)))


def _ms(minuto: int, segundo: int = 0) -> int:
    return minuto * MS_POR_MINUTO + segundo * 1000


def _cierre(minuto: int) -> int:
    """Donde decide el motor: el cierre de la M1 `minuto` menos 1 ms (`cableado.py:297`)."""
    return _ms(minuto + 1) - 1


def _tick(minuto: int, segundo: int, bid: int) -> Tick:
    return Tick(MilisegundoUtc(_ms(minuto, segundo)), Puntos(bid + SPREAD), Puntos(bid), 0, 0)


def _vela(minuto: int, o: int, h: int, low: int, c: int) -> Vela:
    return Vela(MinutoUtc(minuto), Puntos(o), Puntos(h), Puntos(low), Puntos(c), 1)


def _broker(ticks: list[Tick], m1: list[Vela]) -> Broker:
    reglas = ReglasBroker(
        volumen_max_lotes=Decimal(10),
        ordenes_simultaneas_max=10,
        posiciones_dia_max=10,
        huso_corte=ZoneInfo("UTC"),
        comision_por_lote=Decimal(0),
        comision_por_lado=True,
        swap_largo_puntos=Decimal(0),
        swap_corto_puntos=Decimal(0),
    )
    return Broker(
        dataclasses.replace(reglas),
        Configuracion(False, 0, lambda _m: SPREAD),
        Mercado(ticks, m1),
        UNO,
        1,
        stops_level_diagnostico=0,
    )


# ------------------------------------------------ lo que rompe en main: la vela de la decision


def test_una_stop_colocada_en_el_cierre_de_una_m1_sin_ticks_no_se_llena_con_esa_vela() -> None:
    """M0 baja a 990 y M0+1 no baja de 1004: la venta stop en 995, colocada en el cierre de M0, no
    salta. En `main` salta con `respaldo_m1` al fin de M0, con precios de antes de colocarla."""
    b = _broker([], [_vela(M0, 1010, 1011, 990, 1005), _vela(M0 + 1, 1005, 1008, 1004, 1006)])
    b.avanzar(_cierre(M0))
    b.colocar_stop("v", "venta", 995, UNO, 1010, 950, _cierre(M0))
    assert b.avanzar(_ms(M0 + 2)) == []
    assert b.ordenes["v"].estado == "colocada"


def test_una_limite_colocada_en_el_cierre_de_una_m1_sin_ticks_no_se_llena_con_esa_vela() -> None:
    """Lo mismo con una limite de compra en 1000: el ASK de M0 baja a 993, el de M0+1 no de 1007."""
    b = _broker([], [_vela(M0, 1010, 1011, 990, 1005), _vela(M0 + 1, 1005, 1008, 1004, 1006)])
    b.avanzar(_cierre(M0))
    b.colocar_limite("o", "compra", 1000, UNO, 990, 1030, _cierre(M0))
    assert b.avanzar(_ms(M0 + 2)) == []


def test_en_el_borde_de_la_ventana_la_orden_solo_se_evalua_contra_los_ticks_que_siguen() -> None:
    """El minuto M0 no tiene ticks (el borde de la cobertura) y su M1 cruza el nivel; los ticks
    empiezan en M0+1. La orden, colocada en el ultimo milisegundo de M0, se llena con el primer
    tick que lo cruza (M0+1, 20 s), con fuente `ticks`; en `main`, con la M1 de M0 al fin de M0."""
    ticks = [_tick(M0 + 1, 5, 1004), _tick(M0 + 1, 20, 994), _tick(M0 + 1, 40, 998)]
    b = _broker(ticks, [_vela(M0, 1010, 1011, 990, 1005), _vela(M0 + 1, 1004, 1004, 994, 998)])
    b.avanzar(_cierre(M0))
    b.colocar_stop("v", "venta", 995, UNO, 1010, 950, _cierre(M0))
    assert b.avanzar(_ms(M0 + 2)) == [(_ms(M0 + 1, 20), LLENADA, "v", TICKS)]


def test_el_stop_movido_en_el_cierre_de_una_m1_sin_ticks_no_salta_con_esa_vela() -> None:
    """Larga en 1000 con stop 990. La M0 baja a 1000 (la entrada) sin tocar 990, y en su cierre el
    stop pasa a 1000 (el break even, sin ticks: ADR-0065 §5). La M0 se evalua con el stop ANTERIOR
    (no salta) y M0+1 no vuelve a la entrada: la posicion sigue viva. En `main` salta a 1000 al fin
    de M0 con la vela que decidio moverlo (2026-04-06 pos-o12 y 2026-04-07 pos-o29, §0.e)."""
    b = _broker([], [_vela(M0, 1004, 1015, 1000, 1010), _vela(M0 + 1, 1010, 1012, 1005, 1011)])
    b.abrir_conocida("p", "compra", 1000, UNO, 990, 1030, _ms(M0))
    b.avanzar(_cierre(M0))
    b.mover_stop("p", 1000, _cierre(M0))
    b.avanzar(_ms(M0 + 2))
    p = b.posiciones["p"]
    assert p.abierta and p.stop == 1000


def test_la_vela_del_stop_movido_que_toca_el_stop_original_sale_por_el_sin_break_even() -> None:
    """ADR-0065 §4: una M1 que pasa el nivel y toca el stop original sale por el stop original,
    pesimista, y no hay break even. M0 baja a 985 (por debajo de 990) y en su cierre el motor mueve
    el stop a 1000: sale a 990, clasificada como stop entero. En `main` sale a 1000, break even."""
    b = _broker([], [_vela(M0, 1004, 1015, 985, 1010), _vela(M0 + 1, 1010, 1012, 1008, 1011)])
    b.abrir_conocida("p", "compra", 1000, UNO, 990, 1030, _ms(M0))
    b.avanzar(_cierre(M0))
    b.mover_stop("p", 1000, _cierre(M0))
    b.avanzar(_ms(M0 + 2))
    p = b.posiciones["p"]
    assert (p.motivo_cierre, p.precio_cierre, p.cerrada_ms, p.fuente_cierre) == (
        STOP,
        990,
        _ms(M0 + 1),
        RESPALDO_M1,
    )
    movido = p.stop_original is not None
    assert clasificar_cierre(STOP, movido, Decimal(-10)) == SALTO_EL_STOP != BREAK_EVEN


def test_la_vela_de_una_modificacion_se_evalua_con_la_orden_anterior() -> None:
    """Limite de compra en 1000 colocada al empezar M0; en el cierre de M0+1 se modifica a 990. La
    M0+1 lleva el ASK a 998: llena la orden ANTERIOR (1000), a su precio, con su stop y su objetivo,
    al fin de M0+1. En `main` la M0+1 se evalua con 990 y no llena."""
    m1 = [
        _vela(M0, 1010, 1012, 1005, 1010),
        _vela(M0 + 1, 1008, 1010, 995, 1000),
        _vela(M0 + 2, 1000, 1004, 999, 1002),
    ]
    b = _broker([], m1)
    b.colocar_limite("o", "compra", 1000, UNO, 990, 1030, _ms(M0))
    b.avanzar(_cierre(M0 + 1))
    b.modificar("o", _cierre(M0 + 1), precio=995, stop=985, objetivo=1025)
    assert b.avanzar(_ms(M0 + 3)) == [(_ms(M0 + 2), LLENADA, "o", RESPALDO_M1)]
    p = b.posiciones["pos-o"]
    assert (p.entrada, p.stop, p.objetivo, p.abierta_ms) == (1000, 990, 1030, _ms(M0 + 2))


def test_la_vela_de_una_modificacion_no_llena_la_version_nueva() -> None:
    """Al reves: la M0+1 cruza el precio NUEVO (1010) y no el anterior (1000). No se llena en M0+1;
    se llena en M0+2, que tambien lo cruza. En `main`, al fin de M0+1."""
    m1 = [
        _vela(M0, 1012, 1014, 1009, 1012),
        _vela(M0 + 1, 1012, 1013, 1005, 1008),  # ASK minimo 1008: pasa 1010, no 1000
        _vela(M0 + 2, 1008, 1010, 1004, 1006),  # ASK minimo 1007: pasa 1010
    ]
    b = _broker([], m1)
    b.colocar_limite("o", "compra", 1000, UNO, 990, 1030, _ms(M0))
    b.avanzar(_cierre(M0 + 1))
    b.modificar("o", _cierre(M0 + 1), precio=1010, stop=1000, objetivo=1040)
    assert b.avanzar(_ms(M0 + 3)) == [(_ms(M0 + 3), LLENADA, "o", RESPALDO_M1)]
    assert b.posiciones["pos-o"].entrada == 1010


def test_sin_instante_decidido_la_funcion_pura_niega_por_defecto() -> None:
    """`decidido_ms` por defecto es `desde_ms`: con `desde` a media vela, esa vela no cuenta (sus
    precios pueden ser anteriores); con `desde` en el inicio exacto, si."""
    mercado = Mercado([], [_vela(M0, 1010, 1011, 990, 1005)])
    cfg = Configuracion(False, 0, lambda _m: SPREAD)
    assert primer_llenado_limite("compra", 1000, _ms(M0, 30), _ms(M0 + 1), mercado, cfg) is None
    ev = primer_llenado_limite("compra", 1000, _ms(M0), _ms(M0 + 1), mercado, cfg)
    assert ev is not None and ev.fuente == RESPALDO_M1


# ------------------------------------------- lo que no cambia: pasa en main y en la rama


def test_una_pendiente_de_antes_de_una_vela_sin_ticks_se_llena_en_esa_vela() -> None:
    """Colocada en el cierre de M0, sigue pendiente durante M0+1, que la cruza: se llena con la M1
    de M0+1, al fin de M0+1."""
    b = _broker([], [_vela(M0, 1010, 1011, 1005, 1008), _vela(M0 + 1, 1008, 1009, 990, 995)])
    b.avanzar(_cierre(M0))
    b.colocar_stop("v", "venta", 995, UNO, 1010, 950, _cierre(M0))
    assert b.avanzar(_ms(M0 + 2)) == [(_ms(M0 + 2), LLENADA, "v", RESPALDO_M1)]


def test_el_tick_del_ultimo_evento_puede_llenar_otra_pendiente() -> None:
    """«ahora - 1» (`broker.py:743-744`): el tick que llena una orden llena tambien otra que
    estaba pendiente y lo cruza."""
    ticks = [_tick(M0, 10, 1005), _tick(M0, 30, 994)]
    b = _broker(ticks, [])
    b.colocar_stop("a", "venta", 996, UNO, 1010, 950, _ms(M0))
    b.colocar_stop("b", "venta", 995, UNO, 1010, 950, _ms(M0))
    eventos = b.avanzar(_ms(M0 + 1))
    assert [(t, tipo, i) for t, tipo, i, _ in eventos] == [
        (_ms(M0, 30), LLENADA, "a"),
        (_ms(M0, 30), LLENADA, "b"),
    ]


def test_la_salida_tras_un_llenado_del_respaldo_se_mira_desde_la_vela_siguiente() -> None:
    """ADR-0057 §1: la M0+1 llena la orden y toca su stop; la salida no se mira en ella sino en la
    M0+2, que tambien lo toca."""
    m1 = [
        _vela(M0, 1010, 1011, 1005, 1008),
        _vela(M0 + 1, 1008, 1022, 990, 1000),
        _vela(M0 + 2, 1000, 1021, 999, 1018),
    ]
    b = _broker([], m1)
    b.avanzar(_cierre(M0))
    b.colocar_stop("v", "venta", 995, UNO, 1020, 950, _cierre(M0))
    b.avanzar(_ms(M0 + 2))
    p = b.posiciones["pos-v"]
    assert p.abierta and p.abierta_ms == _ms(M0 + 2)
    b.avanzar(_ms(M0 + 3))
    assert (p.motivo_cierre, p.cerrada_ms) == (STOP, _ms(M0 + 3))


def test_con_ticks_el_instante_de_la_decision_ya_no_contaba() -> None:
    """Con ticks no cambia nada: la orden colocada a cierre menos 1 ms se evalua desde el primer
    tick posterior, y un tick anterior a ella que cruzaba el nivel no la llena."""
    ticks = [
        _tick(M0, 30, 990),
        _tick(M0, 50, 1000),
        _tick(M0 + 1, 10, 1001),
        _tick(M0 + 1, 40, 994),
    ]
    b = _broker(ticks, [])
    b.avanzar(_cierre(M0))
    b.colocar_stop("v", "venta", 995, UNO, 1010, 950, _cierre(M0))
    assert b.avanzar(_ms(M0 + 2)) == [(_ms(M0 + 1, 40), LLENADA, "v", TICKS)]
