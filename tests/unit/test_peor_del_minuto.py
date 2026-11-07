"""(e2) de la entrada H (trabajo/sello-respaldo-m1, SELLO-RESPALDO-M1.md): sin ticks,
`Broker._peor_del_minuto` marca una vela solo si EMPIEZA antes del instante hasta el que se avanza
(le queda al menos 1 ms dentro). En `main` aceptaba toda vela que empezara en o antes de ese
instante, asi que al avanzar hasta un instante REDONDO -el sello de un evento del respaldo, una
expiracion, el inicio de una ventana de ADR-0068- marcaba entera la vela que empieza en el: la
peor marca de un minuto que aun no habia transcurrido, y, si la posicion cerraba en ese instante,
dentro de la operacion. Velas SINTETICAS de 2030; contrato 1 y escala 1.

Los dos primeros ROMPEN en `main` (la sonda 5 de `anexos/RESPALDO-M1/sonda_z.py` y la S7b del
diagnostico de H, `anexos/SELLO-RESPALDO-M1/sondas_h.py`); los otros dos pasan en los dos lados: la
vela ya empezada se sigue marcando, en un instante a media vela y en el cierre menos 1 ms en que
decide el motor."""

from __future__ import annotations

import dataclasses
from datetime import UTC, datetime
from decimal import Decimal
from zoneinfo import ZoneInfo

from botsito.data.velas import a_minuto
from botsito.domain.ticks import MS_POR_MINUTO
from botsito.domain.valores import Puntos
from botsito.domain.velas import MinutoUtc, Vela
from botsito.engine.broker import Broker, ReglasBroker
from botsito.engine.llenado import RESPALDO_M1, STOP, Configuracion, Mercado

SPREAD = 3
UNO = Decimal(1)
M0 = int(a_minuto(datetime(2030, 1, 15, 8, 0, tzinfo=UTC)))


def _ms(minuto: int, segundo: int = 0) -> int:
    return minuto * MS_POR_MINUTO + segundo * 1000


def _vela(minuto: int, o: int, h: int, low: int, c: int) -> Vela:
    return Vela(MinutoUtc(minuto), Puntos(o), Puntos(h), Puntos(low), Puntos(c), 1)


def _broker(m1: list[Vela]) -> Broker:
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
        Mercado((), m1),
        UNO,
        1,
        stops_level_diagnostico=0,
    )


# -------------------------------------------- lo que rompe en main: la marca de la vela siguiente


def test_avanzar_a_un_instante_redondo_no_marca_la_vela_que_empieza_en_el() -> None:
    """La sonda 5: una larga en 1000 con stop 990 salta por el respaldo en el sello de M0 (M0 baja
    a 989). M0+1 baja a 900, pero empieza en el instante redondo hasta el que se avanza: no se ha
    visto nada de ella. En `main` su minima entraba como marca en el fin de M0 y, como la posicion
    cerraba ahi, dentro de la operacion. Desde ADR-0091 el stop se sella en el ultimo milisegundo de
    M0 (antes, en su fin)."""
    b = _broker([_vela(M0, 1000, 1001, 989, 1000), _vela(M0 + 1, 1000, 1001, 900, 950)])
    b.abrir_conocida("p", "compra", 1000, UNO, 990, 1030, _ms(M0))
    b.avanzar(_ms(M0 + 1))
    p = b.posiciones["p"]
    sello = _ms(M0 + 1) - 1
    assert (p.motivo_cierre, p.fuente_cierre, p.cerrada_ms) == (STOP, RESPALDO_M1, sello)
    assert p.marcas == [(_ms(M0 + 1) - 1, 989)]
    assert [int(m.precio) for m in b.operaciones_cerradas()[0].marcas] == [989]


def test_una_expiracion_en_un_instante_redondo_no_marca_la_vela_siguiente() -> None:
    """La S7b del diagnostico de H: una pendiente expira en el inicio de M0+1 y el broker se para
    ahi; la larga viva no recibe la minima de M0+1 (900) en ese instante, sino al cierre de M0+1."""
    b = _broker(
        [
            _vela(M0, 1000, 1001, 995, 1000),
            _vela(M0 + 1, 1000, 1001, 900, 950),
            _vela(M0 + 2, 950, 951, 949, 950),
        ]
    )
    b.abrir_conocida("p", "compra", 1000, UNO, 800, 1100, _ms(M0))
    b.colocar_limite("x", "compra", 700, UNO, 690, 1100, _ms(M0), expira_ms=_ms(M0 + 1))
    b.avanzar(_ms(M0 + 2) - 1)
    assert b.ordenes["x"].estado == "expirada"
    assert b.posiciones["p"].marcas == [(_ms(M0 + 1) - 1, 995), (_ms(M0 + 2) - 1, 900)]


# ------------------------------------------------ lo que no cambia: la vela ya empezada se marca


def test_a_media_vela_se_marca_la_vela_en_curso() -> None:
    """A media vela, sin ticks, la vela en curso SI se marca, con toda su minima: es la lectura
    del respaldo, que no sabe nada de dentro del minuto (ADR-0051 §5)."""
    b = _broker([_vela(M0, 1000, 1001, 995, 1000), _vela(M0 + 1, 1000, 1001, 900, 950)])
    b.abrir_conocida("p", "compra", 1000, UNO, 800, 1100, _ms(M0))
    b.avanzar(_ms(M0, 30))
    assert b.posiciones["p"].marcas == [(_ms(M0, 30), 995)]


def test_en_el_cierre_menos_1_ms_se_marca_la_vela_que_cierra() -> None:
    """Donde decide el motor (el cierre de la M1 menos 1 ms, `cableado.py:302`): la vela que
    cierra se marca entera y la siguiente no."""
    b = _broker([_vela(M0, 1000, 1001, 995, 1000), _vela(M0 + 1, 1000, 1001, 900, 950)])
    b.abrir_conocida("p", "compra", 1000, UNO, 800, 1100, _ms(M0))
    b.avanzar(_ms(M0 + 1) - 1)
    assert b.posiciones["p"].marcas == [(_ms(M0 + 1) - 1, 995)]
