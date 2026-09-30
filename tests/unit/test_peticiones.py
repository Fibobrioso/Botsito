"""Las peticiones al servidor del broker simulado (R13, `firma_mensajes_dia_max`; rama
`feature/contador-peticiones`) sobre ticks SINTETICOS de 2030: cuenta colocar, modificar, cancelar
y cerrar, aceptadas o rechazadas; no cuenta lo que el servidor hace solo -llenar, expirar, saltar
el stop o el objetivo- ni `abrir_conocida`; y el dia se corta a medianoche CE(S)T, con su horario
de verano, como el dia de riesgo (ADR-0027). Solo se mide: nada frena."""

from __future__ import annotations

import dataclasses
from datetime import UTC, date, datetime
from decimal import Decimal
from pathlib import Path
from zoneinfo import ZoneInfo

from botsito.data.velas import a_minuto
from botsito.domain.ticks import MS_POR_MINUTO, MilisegundoUtc, Tick
from botsito.domain.valores import Puntos
from botsito.engine.broker import (
    PETICION_CANCELAR,
    PETICION_CERRAR,
    PETICION_COLOCAR,
    PETICION_MODIFICAR,
    Broker,
    Peticion,
    Rechazo,
    ReglasBroker,
    peticiones_por_dia,
)
from botsito.engine.llenado import Configuracion, Mercado
from botsito.engine.perfil_cuenta import cargar_perfil
from botsito.engine.simulacion import reglas_broker_de

PERFIL = (
    Path(__file__).resolve().parents[2] / "knowledge" / "cuentas" / "ftmo-2step-swing-100k.yaml"
)
SPREAD = 3
UNO = Decimal(1)
CEST = ZoneInfo("Europe/Prague")
M0 = int(a_minuto(datetime(2030, 1, 15, 8, 0, tzinfo=UTC)))


def _ms(minuto: int, segundo: int = 0) -> int:
    return minuto * MS_POR_MINUTO + segundo * 1000


def _tick(minuto: int, segundo: int, bid: int) -> Tick:
    return Tick(MilisegundoUtc(_ms(minuto, segundo)), Puntos(bid + SPREAD), Puntos(bid), 0, 0)


def _broker(ticks: list[Tick], **cambios: object) -> Broker:
    reglas = ReglasBroker(
        volumen_max_lotes=Decimal(10),
        ordenes_simultaneas_max=5,
        posiciones_dia_max=5,
        huso_corte=CEST,
        comision_por_lote=Decimal(0),
        comision_por_lado=False,
        swap_largo_puntos=Decimal(0),
        swap_corto_puntos=Decimal(0),
        mensajes_dia_max=2000,
    )
    reglas = dataclasses.replace(reglas, **cambios)  # type: ignore[arg-type]
    return Broker(reglas, Configuracion(False, 0, lambda _m: SPREAD), Mercado(ticks, []), UNO, 1)


def _tipos(b: Broker) -> list[tuple[str, str, bool]]:
    return [(p.tipo, p.id, p.aceptada) for p in b.traza().peticiones]


def test_cuenta_cada_peticion_aceptada_o_rechazada_y_nada_de_lo_que_hace_el_servidor() -> None:
    # BID 1000 en el minuto 0; baja a 995 en el 1 (llena la compra limite en 1000) y sube a 1021
    # en el 3 (salta su objetivo en 1020): el llenado y el objetivo no son peticiones
    ticks = [
        _tick(M0, 10, 1000),
        _tick(M0 + 1, 5, 995),
        _tick(M0 + 2, 0, 1010),
        _tick(M0 + 3, 0, 1021),
        _tick(M0 + 5, 0, 1010),
    ]
    b = _broker(ticks)
    assert not isinstance(
        b.colocar_limite("a", "compra", 998, UNO, 990, 1020, _ms(M0, 20)), Rechazo
    )
    # modificar aceptada; y rechazada, con el precio del lado equivocado (una compra limite por
    # encima del ask): la orden sigue como estaba, pero la peticion cuenta
    assert not isinstance(b.modificar("a", _ms(M0, 30), precio=1000), Rechazo)
    assert isinstance(b.modificar("a", _ms(M0, 40), precio=1010), Rechazo)
    # rechazada por el perfil (volumen): cuenta
    assert isinstance(
        b.colocar_limite("b", "compra", 990, Decimal(11), 980, 1020, _ms(M0, 50)), Rechazo
    )
    b.avanzar(_ms(M0 + 4))  # llena "a" y salta su objetivo: nada de eso es una peticion
    assert not isinstance(
        b.colocar_limite("c", "compra", 990, UNO, 980, 1030, _ms(M0 + 4)), Rechazo
    )
    b.cancelar("c", _ms(M0 + 4, 10))
    # abrir_conocida repite una operacion del trader: no la emite el bot
    b.abrir_conocida("t", "compra", 1013, UNO, 1000, 1040, _ms(M0 + 5, 1))
    b.mover_stop("t", 1005, _ms(M0 + 5, 2))
    b.cerrar_a_mercado("t", _ms(M0 + 5, 3))
    assert _tipos(b) == [
        (PETICION_COLOCAR, "a", True),
        (PETICION_MODIFICAR, "a", True),
        (PETICION_MODIFICAR, "a", False),
        (PETICION_COLOCAR, "b", False),
        (PETICION_COLOCAR, "c", True),
        (PETICION_CANCELAR, "c", True),
        (PETICION_MODIFICAR, "t", True),
        (PETICION_CERRAR, "t", True),
    ]
    assert peticiones_por_dia(b.traza().peticiones, CEST) == {
        date(2030, 1, 15): {
            PETICION_COLOCAR: 3,
            PETICION_MODIFICAR: 3,
            PETICION_CANCELAR: 1,
            PETICION_CERRAR: 1,
            "total": 8,
            "rechazadas": 2,
        }
    }


def test_nada_frena_aunque_se_pase_del_limite() -> None:
    # con el limite en 1, la segunda, la tercera y la cuarta peticion se aceptan igual
    b = _broker([_tick(M0, 0, 1000)], mensajes_dia_max=1)
    for i in range(3):
        orden = b.colocar_limite(f"o{i}", "compra", 990 - i, UNO, 980, 1020, _ms(M0, 10 + i))
        assert not isinstance(orden, Rechazo)
    b.cancelar("o0", _ms(M0, 20))
    assert [p.aceptada for p in b.traza().peticiones] == [True] * 4


def _en(instante: datetime) -> Peticion:
    ms = int((instante - datetime(1970, 1, 1, tzinfo=UTC)).total_seconds() * 1000)
    return Peticion(ms, PETICION_COLOCAR, "x", True)


def test_el_dia_se_corta_a_medianoche_cest_con_su_horario_de_verano() -> None:
    # invierno, CET = UTC+1: 22:59:59Z es el dia 15 y 23:00Z ya es el 16
    invierno = [
        _en(datetime(2030, 1, 15, 22, 59, 59, tzinfo=UTC)),
        _en(datetime(2030, 1, 15, 23, 0, tzinfo=UTC)),
    ]
    # verano, CEST = UTC+2: 21:59:59Z es el dia 15 y 22:00Z ya es el 16
    verano = [
        _en(datetime(2030, 7, 15, 21, 59, 59, tzinfo=UTC)),
        _en(datetime(2030, 7, 15, 22, 0, tzinfo=UTC)),
    ]
    assert [(d, n["total"]) for d, n in peticiones_por_dia(invierno, CEST).items()] == [
        (date(2030, 1, 15), 1),
        (date(2030, 1, 16), 1),
    ]
    assert [(d, n["total"]) for d, n in peticiones_por_dia(verano, CEST).items()] == [
        (date(2030, 7, 15), 1),
        (date(2030, 7, 16), 1),
    ]


def test_el_perfil_da_el_corte_cest_y_el_limite_de_r13() -> None:
    reglas = reglas_broker_de(cargar_perfil(PERFIL))
    assert reglas.huso_corte.key == "Europe/Prague"
    assert reglas.mensajes_dia_max == 2000
