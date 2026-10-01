"""El break even de RN-014 AL TICK (rama feature/be-al-tick, ADR-0065) sobre ticks SINTETICOS de
2030: el stop pasa a la entrada en el primer tick cuyo BID pasa el nivel de activacion, no en el
cierre de la M1; el nivel es el mismo de siempre; sin ticks se queda en el cierre de la M1, que es
el respaldo pesimista, y la traza lo dice; y mover el stop es una peticion al servidor que el
contador suma, una sola vez aunque el motor lo vuelva a pedir al cierre."""

from __future__ import annotations

import dataclasses
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import pytest

from botsito.config.registro import Registro, cargar_registro
from botsito.data.velas import a_minuto
from botsito.domain.estructura_m1 import (
    COMPRA,
    MECHA,
    nivel_de_activacion_posterior,
    zona_posterior_completada,
)
from botsito.domain.ticks import MS_POR_MINUTO, MilisegundoUtc, Tick
from botsito.domain.valores import Puntos
from botsito.domain.velas import MinutoUtc, Vela
from botsito.engine.broker import (
    CIERRE_M1,
    PETICION_MODIFICAR,
    STOP_MOVIDO,
    Broker,
    ReglasBroker,
)
from botsito.engine.llenado import OBJETIVO, RESPALDO_M1, STOP, TICKS, Configuracion, Mercado
from botsito.engine.motor import DatosMercado, DiaDeMercado
from botsito.engine.primitivas_broker import BREAK_EVEN, clasificar_cierre

from . import test_cableado as tc

SPREAD = 3
UNO = Decimal(1)
M0 = int(a_minuto(datetime(2030, 1, 15, 8, 0, tzinfo=UTC)))
ENTRADA, STOP_INICIAL, OBJ = 1000, 984, 1060
NIVEL = 1021  # el punto alto que la zona de control posterior dejo


def _ms(minuto: int, segundo: int = 0) -> int:
    return minuto * MS_POR_MINUTO + segundo * 1000


def _tick(minuto: int, segundo: int, bid: int) -> Tick:
    return Tick(MilisegundoUtc(_ms(minuto, segundo)), Puntos(bid + SPREAD), Puntos(bid), 0, 0)


def _vela(minuto: int, o: int, h: int, lo: int, c: int) -> Vela:
    return Vela(MinutoUtc(minuto), Puntos(o), Puntos(h), Puntos(lo), Puntos(c), 1)


def _broker(ticks: list[Tick], m1: list[Vela] | None = None) -> Broker:
    reglas = ReglasBroker(
        volumen_max_lotes=Decimal(10),
        ordenes_simultaneas_max=5,
        posiciones_dia_max=5,
        huso_corte=ZoneInfo("Europe/Prague"),
        comision_por_lote=Decimal(0),
        comision_por_lado=False,
        swap_largo_puntos=Decimal(0),
        swap_corto_puntos=Decimal(0),
        mensajes_dia_max=2000,
    )
    config = Configuracion(False, 0, lambda _m: SPREAD)
    return Broker(reglas, config, Mercado(ticks, m1 or []), UNO, 1)


# en M0+2 el BID pasa el nivel a los 20 s, vuelve por debajo de la entrada a los 30 s y llega al
# stop inicial a los 40 s: todo DENTRO de la misma M1
TOCA_Y_VUELVE = [
    _tick(M0, 10, 1001),
    _tick(M0 + 1, 0, 1012),
    _tick(M0 + 2, 0, 1014),
    _tick(M0 + 2, 20, 1025),
    _tick(M0 + 2, 30, 997),
    _tick(M0 + 2, 40, 983),
    _tick(M0 + 3, 0, 983),
]


def _abierta(b: Broker) -> str:
    b.abrir_conocida("p", "compra", ENTRADA, UNO, STOP_INICIAL, OBJ, _ms(M0, 5))
    return "p"


def test_un_tick_que_pasa_el_nivel_y_vuelve_en_la_misma_m1_pone_el_break_even() -> None:
    """Lo que cambia: ANTES el stop se movia en el cierre de la M1 que pasa el nivel, asi que una
    M1 que lo pasa y vuelve al stop inicial antes de cerrar salia por el stop entero. AHORA el stop
    va a la entrada en el tick que pasa el nivel y la posicion sale por break even."""
    # ahora: vigilado desde el cierre de M0+1
    b = _broker(TOCA_Y_VUELVE)
    pid = _abierta(b)
    b.vigilar_break_even(pid, NIVEL, _ms(M0 + 2) - 1)
    b.avanzar(_ms(M0 + 3) - 1)
    p = b.posiciones[pid]
    assert (p.stop, p.stop_original, p.stop_movido_ms) == (ENTRADA, STOP_INICIAL, _ms(M0 + 2, 20))
    # el stop nuevo salta en el tick SIGUIENTE (30 s), al precio de ese tick
    assert (p.motivo_cierre, p.cerrada_ms, p.precio_cierre) == (STOP, _ms(M0 + 2, 30), 997)
    assert clasificar_cierre(STOP, p.stop_original is not None, Decimal(-3)) == BREAK_EVEN
    eventos = [(t, f) for _, t, _, f in b.traza().eventos]
    assert eventos == [("llenada", "conocida"), (STOP_MOVIDO, TICKS), (STOP, TICKS)]

    # antes (sin vigilar al tick): la misma M1 lleva la posicion al stop inicial
    a = _broker(TOCA_Y_VUELVE)
    qid = _abierta(a)
    a.avanzar(_ms(M0 + 3) - 1)
    q = a.posiciones[qid]
    assert (q.stop_original, q.motivo_cierre, q.precio_cierre) == (None, STOP, 983)
    assert clasificar_cierre(STOP, q.stop_original is not None, Decimal(-17)) != BREAK_EVEN


def test_el_paso_del_stop_es_una_peticion_y_el_cierre_de_la_m1_no_la_repite() -> None:
    """Mover el stop es una peticion `modificar` (R13), en el instante del tick. Vigilar no lo es.
    Si el motor vuelve a pedir la entrada en el cierre de la M1, el stop ya esta ahi: nada."""
    ticks = [_tick(M0, 10, 1001), _tick(M0 + 1, 0, 1012), _tick(M0 + 2, 20, 1025)]
    ticks += [_tick(M0 + 2, 50, 1030), _tick(M0 + 3, 0, 1030)]
    b = _broker(ticks)
    pid = _abierta(b)
    b.vigilar_break_even(pid, NIVEL, _ms(M0 + 2) - 1)
    assert not b.traza().peticiones, "vigilar no es una peticion"
    b.avanzar(_ms(M0 + 3) - 1)
    b.mover_stop(pid, ENTRADA, _ms(M0 + 3) - 1)  # lo que pide RN-014 al cierre de M0+2
    peticiones = [(p.tipo, p.instante_ms, p.aceptada) for p in b.traza().peticiones]
    assert peticiones == [(PETICION_MODIFICAR, _ms(M0 + 2, 20), True)]
    assert [t for _, t, _, _ in b.traza().eventos].count(STOP_MOVIDO) == 1


def test_sin_ticks_el_respaldo_m1_sigue_siendo_pesimista_y_la_traza_lo_marca() -> None:
    """Sin ticks no hay instante al tick: vigilar no hace nada y el break even se queda en el
    cierre de la M1, marcado `respaldo_m1`. Y una M1 que pasa el nivel Y toca el stop inicial sale
    por el stop: el respaldo pone el stop primero, como siempre (ADR-0051 §3)."""
    m1 = [
        _vela(M0, 1000, 1002, 999, 1001),
        _vela(M0 + 1, 1001, 1013, 1000, 1012),
        _vela(M0 + 2, 1012, 1026, 1011, 1025),  # pasa el nivel sin tocar el stop
        _vela(M0 + 3, 1025, 1026, 1024, 1025),
    ]
    b = _broker([], m1)
    pid = _abierta(b)
    b.vigilar_break_even(pid, NIVEL, _ms(M0 + 2) - 1)
    b.avanzar(_ms(M0 + 3) - 1)
    assert b.posiciones[pid].stop == STOP_INICIAL, "sin ticks, nada se mueve dentro de la M1"
    b.mover_stop(pid, ENTRADA, _ms(M0 + 3) - 1)  # RN-014 en el cierre de la M1
    movido = [(t, f) for _, t, _, f in b.traza().eventos if t == STOP_MOVIDO]
    assert movido == [(STOP_MOVIDO, RESPALDO_M1)]
    assert [p.tipo for p in b.traza().peticiones] == [PETICION_MODIFICAR]

    # pesimista: la M1 pasa el nivel y toca el stop inicial; sale por el stop entero
    peor = [m1[0], m1[1], _vela(M0 + 2, 1012, 1026, 983, 990), m1[3]]
    c = _broker([], peor)
    qid = _abierta(c)
    c.vigilar_break_even(qid, NIVEL, _ms(M0 + 2) - 1)
    c.avanzar(_ms(M0 + 3) + 1)
    q = c.posiciones[qid]
    assert (q.motivo_cierre, q.precio_cierre, q.stop_original) == (STOP, STOP_INICIAL, None)


def test_en_el_mismo_tick_manda_lo_que_ya_hay_y_el_stop_nuevo_cuenta_despues() -> None:
    """ADR-0065 §3. Un tick que pasa el objetivo Y el nivel cierra por objetivo: no se mueve nada.
    Y un nivel por debajo de la entrada (la racha a favor no llego a ella) mueve el stop por
    encima del precio: salta en el tick SIGUIENTE, nunca en el que lo movio."""
    b = _broker([_tick(M0, 10, 1001), _tick(M0 + 2, 0, 1070), _tick(M0 + 2, 10, 1070)])
    pid = _abierta(b)
    b.vigilar_break_even(pid, 1065, _ms(M0 + 1))
    b.avanzar(_ms(M0 + 3) - 1)
    p = b.posiciones[pid]
    assert (p.motivo_cierre, p.cerrada_ms, p.stop_original) == (OBJETIVO, _ms(M0 + 2), None)
    assert not b.traza().peticiones

    c = _broker([_tick(M0, 10, 1001), _tick(M0 + 2, 0, 996), _tick(M0 + 2, 10, 997)])
    qid = _abierta(c)
    c.vigilar_break_even(qid, 995, _ms(M0 + 1))
    c.avanzar(_ms(M0 + 3) - 1)
    q = c.posiciones[qid]
    assert q.stop_movido_ms == _ms(M0 + 2) and q.stop == ENTRADA
    assert (q.motivo_cierre, q.cerrada_ms, q.precio_cierre) == (STOP, _ms(M0 + 2, 10), 997)


def test_el_nivel_vigilado_es_el_mismo_punto_que_completa_la_zona() -> None:
    """El break even al tick cambia el instante, no el nivel: el que se vigila es el extremo que
    `zona_posterior_completada` mira, y deja de haberlo en cuanto la zona se completa."""
    m1 = [
        _vela(M0, 1000, 1011, 999, 1010),  # verde
        _vela(M0 + 1, 1010, 1021, 1009, 1020),  # verde: la racha llega a 1021
        _vela(M0 + 2, 1020, 1020, 1013, 1014),  # roja: deja el punto alto en 1021
    ]
    assert zona_posterior_completada(m1, COMPRA, MECHA) is None
    assert nivel_de_activacion_posterior(m1, COMPRA, MECHA) == 1021
    pasa = [*m1, _vela(M0 + 3, 1014, 1022, 1013, 1015)]
    assert zona_posterior_completada(pasa, COMPRA, MECHA) == 3
    assert nivel_de_activacion_posterior(pasa, COMPRA, MECHA) is None
    assert nivel_de_activacion_posterior(m1[:2], COMPRA, MECHA) is None  # sin roja, sin zona


# ------------------------------------------------------------- de punta a punta, por el motor


def _registro_con_break_even(tmp_path: Path, valor: str) -> Registro:
    texto = (tc.RAIZ / "knowledge" / "spec" / "parametros.yaml").read_text(encoding="utf-8")
    viejo = '    valor: "tocar"\n'
    assert texto.count(viejo) == 1
    ruta = tmp_path / "parametros.yaml"
    ruta.write_text(texto.replace(viejo, f'    valor: "{valor}"\n'), encoding="utf-8")
    return cargar_registro(ruta)


def _toca_y_vuelve_en_el_motor() -> Any:
    """La ruta de RN-014 de `test_cableado`, con la M1 que pasa el punto alto (ENTRADA+21)
    rehecha: a los 20 s pasa, a los 30 s baja de la entrada y a los 40 s toca el stop inicial."""
    base = tc._mercado(tc.RUTA_BREAK_EVEN)
    m = tc.MINUTO_ZONA + 7
    e = tc.ENTRADA
    nuevos = [
        Tick(MilisegundoUtc(_ms(m, s)), Puntos(b + tc.SPREAD), Puntos(b), 0, 0)
        for s, b in ((0, e + 14), (20, e + 25), (30, e - 3), (40, e - 17))
    ]
    ticks = sorted(
        [t for t in base.ticks if int(t.instante) // MS_POR_MINUTO != m] + nuevos,
        key=lambda t: int(t.instante),
    )
    m1 = tuple(
        _vela(m, e + 14, e + 25, e - 17, e - 17) if int(v.inicio) == m else v for v in base.m1
    )
    return dataclasses.replace(base, ticks=tuple(ticks), m1=m1)


@pytest.mark.parametrize(
    ("valor", "cierre", "movido"),
    [("tocar", -3, True), ("cierre", -16, False)],
)
def test_por_el_motor_el_break_even_al_tocar_salva_la_m1_que_toca_y_vuelve(
    registro: Registro,
    vocabulario: dict[str, dict[str, Any]],
    tmp_path: Path,
    valor: str,
    cierre: int,
    movido: bool,
) -> None:
    """Con `break_even_condicion` = `tocar` (el valor CONFIRMED) el motor vigila el punto alto
    desde el cierre de la roja y el stop va a la entrada en el tick que lo pasa: la posicion sale
    a la entrada. Con `cierre`, lo de antes: la M1 llega al stop inicial antes de cerrar."""
    reg = registro if valor == "tocar" else _registro_con_break_even(tmp_path, valor)
    assert reg.opcion("break_even_condicion") == valor
    mercado = _toca_y_vuelve_en_el_motor()
    motor = tc._motor(reg, vocabulario, mercado)
    predicados, _ = tc._sinteticas()
    del predicados["se_completa_zona_de_control"]
    motor.primitivas_extra = predicados
    datos = DatosMercado(tc._h4_alcista(), velas_m1=list(mercado.m1))
    motor.correr_dia(DiaDeMercado(tc.DIA, tc.HUSO, tc.SESIONES, datos))
    p = next(iter(motor.brokers[tc.DIA.isoformat()].posiciones.values()))
    assert p.motivo_cierre == STOP
    assert (p.stop_original is not None) is movido
    m = tc.MINUTO_ZONA + 7
    if movido:
        assert p.stop_movido_ms == _ms(m, 20) and p.precio_cierre == tc.ENTRADA + cierre
        peticiones = motor.brokers[tc.DIA.isoformat()].traza().peticiones
        assert [(x.tipo, x.instante_ms) for x in peticiones if x.tipo == PETICION_MODIFICAR] == [
            (PETICION_MODIFICAR, _ms(m, 20))
        ]
    else:
        assert p.precio_cierre == tc.ENTRADA + cierre - 1  # el tick de 40 s, un punto mas alla


@pytest.fixture(scope="module")
def registro() -> Registro:
    return cargar_registro(tc.RAIZ / "knowledge" / "spec" / "parametros.yaml")


@pytest.fixture(scope="module")
def vocabulario() -> dict[str, dict[str, Any]]:
    from botsito.spec.modelo import cargar_vocabulario

    return cargar_vocabulario(tc.SPEC)


def test_la_fuente_de_un_stop_movido_en_el_cierre_con_ticks_es_cierre_m1() -> None:
    """El motor tambien puede mover el stop en el cierre de una M1 CON ticks (con `cierre`, o con
    el criterio `cuerpo`, que no se ve en un tick): la traza lo dice `cierre_m1`."""
    b = _broker([_tick(M0, 10, 1001), _tick(M0 + 1, 0, 1012)])
    pid = _abierta(b)
    b.mover_stop(pid, ENTRADA, _ms(M0 + 1, 30))
    assert [(t, f) for _, t, _, f in b.traza().eventos if t == STOP_MOVIDO] == [
        (STOP_MOVIDO, CIERRE_M1)
    ]
