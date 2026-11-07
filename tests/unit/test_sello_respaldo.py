"""ADR-0091 (`trabajo/sello-respaldo-m1`, H de la Next Action, R3.6): el evento del respaldo M1 se
sella en el ULTIMO milisegundo de su vela (k fin - 1 ms), el instante en que decide el motor en su
cierre, y no en k fin. El `avanzar` de ese cierre evalua la vela k ANTES de que el motor decida.

ROMPEN en `main` (que sellaba en k fin): la vela en cuyo cierre el motor cancela una orden la
llena (S6 del diagnostico de H); el fin del dia evalua la ultima vela (S4); un llenado en la vela
que acaba en el inicio de una ventana de ADR-0068 se sella fuera de ella (S5); un llenado en la
ultima vela antes del corte se sella en el corte menos 1 ms y sigue sin pagar ese swap ni cambiar
de dia (S9); y ADR-0083 D2 por el cableado: el punto se libera, y se vuelve a colocar, en el
cierre de la vela del stop (no en el siguiente), y un rechazo al llenar lo gasta en el cierre de
la vela del llenado.

Pasan en los dos lados: la marca de la vela del llenado no se toma (S1, la neutralidad de
`minuto_de_apertura`, ADR-0091 §2). Velas SINTETICAS de 2030; las del bróker con contrato 1 y escala
1, las del cableado las de `test_cableado` y `test_punto_usado`, sin ticks (`depuracion`)."""

from __future__ import annotations

import dataclasses
from collections.abc import Mapping
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any
from zoneinfo import ZoneInfo

import pytest

from botsito.config.registro import Registro, cargar_registro
from botsito.data.velas import a_minuto
from botsito.domain.cierres import CalendarioCierres, Cierre, ReglasCierres
from botsito.domain.ticks import MS_POR_MINUTO
from botsito.domain.valores import Puntos
from botsito.domain.velas import MinutoUtc, Vela
from botsito.engine import primitivas_broker, zonas
from botsito.engine.broker import (
    CANCELADA,
    LLENADA,
    MOTIVO_MARGEN_LIBRE,
    RECHAZADA,
    Broker,
    ReglasBroker,
)
from botsito.engine.entrada import STOP_EN_RUPTURA
from botsito.engine.interprete import EstadoDia, Momento, Resultado, Tri
from botsito.engine.llenado import RESPALDO_M1, STOP, Configuracion, Mercado
from botsito.engine.motor import DiaDeMercado
from botsito.spec.modelo import cargar_vocabulario
from tests.unit import test_cableado as tc
from tests.unit import test_punto_usado as tu

SPREAD = 3
UNO = Decimal(1)
M0 = int(a_minuto(datetime(2030, 1, 15, 8, 0, tzinfo=UTC)))
HORA = 60 * MS_POR_MINUTO


def _ms(minuto: int, segundo: int = 0) -> int:
    return minuto * MS_POR_MINUTO + segundo * 1000


def _cierre(minuto: int) -> int:
    """Donde decide el motor en el cierre de la M1 `minuto`: su fin menos 1 ms (`cableado.py`)."""
    return _ms(minuto + 1) - 1


def _vela(minuto: int, o: int, h: int, low: int, c: int) -> Vela:
    return Vela(MinutoUtc(minuto), Puntos(o), Puntos(h), Puntos(low), Puntos(c), 1)


def _broker(m1: list[Vela], cierres: ReglasCierres | None = None, **reglas: Any) -> Broker:
    base = ReglasBroker(
        volumen_max_lotes=Decimal(10),
        ordenes_simultaneas_max=10,
        posiciones_dia_max=10,
        huso_corte=ZoneInfo("UTC"),
        comision_por_lote=Decimal(0),
        comision_por_lado=True,
        swap_largo_puntos=Decimal(0),
        swap_corto_puntos=Decimal(0),
        cierres=cierres,
    )
    return Broker(
        dataclasses.replace(base, **reglas),
        Configuracion(False, 0, lambda _m: SPREAD),
        Mercado((), m1),
        UNO,
        1,
        stops_level_diagnostico=0,
    )


# ------------------------------------------------------------- en el broker: rompen en main


def test_la_vela_en_cuyo_cierre_el_motor_cancela_la_orden_la_llena_antes() -> None:
    """S6 (las cancelaciones del censo, SELLO-RESPALDO-M1.md §0.c): una venta stop en 995 viva
    desde el inicio de M0; la M0+1, sin ticks, baja a 990. El motor la cancelaria en el cierre de
    M0+1, pero el `avanzar` de ese cierre ya evaluo la M0+1: la orden esta LLENA en su ultimo
    milisegundo. En `main` seguia pendiente y la cancelacion la dejaba sin evaluar contra la vela
    en que vivia."""
    b = _broker([_vela(M0, 1010, 1011, 1005, 1008), _vela(M0 + 1, 1008, 1009, 990, 995)])
    b.colocar_stop("v", "venta", 995, UNO, 1010, 950, _ms(M0))
    b.avanzar(_cierre(M0))
    assert b.avanzar(_cierre(M0 + 1)) == [(_cierre(M0 + 1), LLENADA, "v", RESPALDO_M1)]
    assert b.ordenes["v"].estado == LLENADA


def test_el_fin_del_dia_evalua_la_ultima_vela_antes_de_cerrar_y_cancelar() -> None:
    """S4 (ADR-0091 §5): el fin del dia del cableado (`fin_ms = ultimo * 60000 - 1`, `avanzar`,
    cerrar lo vivo a mercado y cancelar lo pendiente). La ultima vela (M0+1) cruza la limite en 995
    y el stop 988 de la posicion: la limite se llena y la posicion sale por su stop, los dos en el
    ultimo milisegundo de la vela. En `main` la ultima vela no se evaluaba: la limite se cancelaba
    y la posicion se cerraba a mercado."""
    m1 = [_vela(M0, 1010, 1011, 1005, 1008), _vela(M0 + 1, 1008, 1009, 985, 990)]
    m1 += [_vela(M0 + 2, 990, 991, 989, 990)]
    b = _broker(m1)
    b.colocar_limite("o", "compra", 995, UNO, 980, 1030, _ms(M0))
    b.abrir_conocida("p", "compra", 1005, UNO, 988, 1030, _ms(M0))
    b.avanzar(_cierre(M0))
    fin_ms = _cierre(M0 + 1)
    b.avanzar(fin_ms)
    for p in list(b.posiciones.values()):
        if p.abierta:
            b.cerrar_a_mercado(p.id, fin_ms)
    for o in list(b.ordenes.values()):
        if o.estado in ("colocada", "modificada"):
            b.cancelar(o.id, fin_ms)
    b.avanzar(fin_ms)
    assert b.ordenes["o"].estado == LLENADA
    p = b.posiciones["p"]
    assert (p.motivo_cierre, p.precio_cierre, p.cerrada_ms) == (STOP, 988, fin_ms)


def test_un_llenado_en_la_vela_que_acaba_en_la_ventana_se_sella_fuera_de_ella() -> None:
    """S5 (ADR-0091 §5, recuadro en ADR-0068 §2): una ventana prohibida empieza en W = el inicio de
    M0+2. La limite en 1000, colocada al empezar M0; la M0+1, que acaba en W, la cruza: se llena en
    W - 1 ms, fuera de la ventana, y no hay cancelacion. En `main` se sellaba en W y la cancelacion
    al empezar la ventana iba antes: la orden se cancelaba sin llenarse."""
    w = _ms(M0 + 2)
    margen = 120 * MS_POR_MINUTO
    calendario = CalendarioCierres(
        (Cierre(w + margen, w + margen + 3 * HORA, "sintetico"),), _ms(M0 - 600), _ms(M0 + 6000)
    )
    m1 = [_vela(M0, 1010, 1011, 1005, 1008), _vela(M0 + 1, 1008, 1009, 990, 995)]
    m1 += [_vela(M0 + 2, 995, 996, 990, 995), _vela(M0 + 3, 995, 996, 990, 995)]
    b = _broker(m1, ReglasCierres(calendario, margen, 120 * MS_POR_MINUTO, True))
    b.colocar_limite("o", "compra", 1000, UNO, 960, 1030, _ms(M0))
    b.avanzar(_cierre(M0 + 1))
    b.avanzar(_cierre(M0 + 2))
    assert b.ordenes["o"].estado == LLENADA
    assert b.posiciones["pos-o"].abierta_ms == w - 1
    assert not b.traza().cierres  # ninguna cancelacion por la ventana


def test_un_llenado_en_la_ultima_vela_antes_del_corte_no_paga_ese_swap_ni_cambia_de_dia() -> None:
    """S9 (ADR-0091 §2): la limite se llena con la ultima vela antes de la medianoche del corte
    (huso UTC). El llenado se sella en la medianoche menos 1 ms, pero la posicion sigue siendo del
    minuto siguiente: no paga el swap de esa medianoche y cuenta para `posiciones_dia_max` en el
    dia siguiente (una segunda posicion ese dia se rechaza con un maximo de 1). En `main` se
    sellaba en la medianoche."""
    n = int(a_minuto(datetime(2030, 1, 16, 0, 0, tzinfo=UTC)))
    m1 = [_vela(n - 2, 1010, 1011, 1005, 1008), _vela(n - 1, 1008, 1009, 990, 1002)]
    m1 += [_vela(n, 1002, 1005, 1000, 1003), _vela(n + 1, 1003, 1005, 1001, 1004)]
    b = _broker(m1, swap_largo_puntos=Decimal(1), posiciones_dia_max=1)
    b.colocar_limite("o", "compra", 1000, UNO, 980, 1030, _ms(n - 2))
    for k in (n - 2, n - 1, n):
        b.avanzar(_cierre(k))
    p = b.posiciones["pos-o"]
    assert p.abierta_ms == _ms(n) - 1
    assert p.swaps == []  # la medianoche del llenado no se cobra
    b.colocar_limite("x", "compra", 990, UNO, 980, 1030, _cierre(n))
    assert b.ordenes["x"].estado == RECHAZADA  # posiciones_dia_max: la posicion es del dia 16
    assert b.traza().rechazos[-1].motivo == "posiciones_dia_max"


# ------------------------------------------------------------- en el broker: pasan en los dos


def test_la_marca_de_la_vela_del_llenado_no_se_toma() -> None:
    """S1 (ADR-0091 §2, la neutralidad de `minuto_de_apertura`): la limite en 1000 se llena con M0,
    que baja a 970, por debajo del stop 990. Ninguna marca de M0 (sus precios pueden ser anteriores
    al llenado): la primera es la de M0+1, en su cierre menos 1 ms. Pasa en `main` y en la rama."""
    b = _broker([_vela(M0, 1010, 1012, 970, 1004), _vela(M0 + 1, 1004, 1006, 1000, 1005)])
    b.colocar_limite("o", "compra", 1000, UNO, 990, 1030, _ms(M0))
    b.avanzar(_cierre(M0))
    b.avanzar(_cierre(M0 + 1))
    p = b.posiciones["pos-o"]
    assert p.abierta and p.marcas == [(_cierre(M0 + 1), 1000)]


# --------------------------------------------- ADR-0083 D2 por el cableado, sin ticks: rompen


@pytest.fixture(scope="module")
def registro() -> Registro:
    return cargar_registro(tc.RAIZ / "knowledge" / "spec" / "parametros.yaml")


def _correr_sin_ticks(
    registro: Registro,
    ruta: Mapping[int, int],
    plan: Mapping[int, int],
    monkeypatch: pytest.MonkeyPatch,
    hueco: Mapping[int, int] | None = None,
) -> Any:
    """`test_punto_usado._correr` con el mercado SIN ticks (respaldo M1 en todo el dia, con
    `depuracion`): el mismo productor real de la zona y la misma geometria sintetica. `hueco`:
    minuto -> la APERTURA de esa vela (un hueco desde el cierre anterior), para que el respaldo
    llene una stop a la apertura (ADR-0057 §1)."""
    vocabulario = cargar_vocabulario(tc.SPEC)
    mercado = tc._mercado(ruta, con_ticks=False)
    if hueco:
        m1 = tuple(
            dataclasses.replace(
                v,
                abierta=Puntos(hueco[int(v.inicio)]),
                maxima=Puntos(max(int(v.maxima), hueco[int(v.inicio)] + 1)),
            )
            if int(v.inicio) in hueco
            else v
            for v in mercado.m1
        )
        mercado = dataclasses.replace(mercado, m1=m1)
    motor = tc._motor(registro, vocabulario, mercado, depuracion=True)
    motor.limpia = "solo_una_zona_de_control"
    motor.tipo_orden = STOP_EN_RUPTURA
    motor.zonas_de = None
    predicados, acumuladores = tc._sinteticas()
    for real in ("toca_colocar_orden_limite", "se_completa_zona_de_control"):
        del predicados[real]
    del acumuladores["cartuchos"]

    def toma(args: Mapping[str, Any], momento: Momento, estado: EstadoDia) -> Any:
        return Resultado(Tri.SI if int(momento.instante) == tu.TOMA else Tri.NO)

    def si(args: Mapping[str, Any], momento: Momento, estado: EstadoDia) -> Any:
        return Resultado(Tri.SI)

    predicados.update({"alcanza_nivel": toma, "cruza": toma, "la_toma_es_de_la_sesion": si})
    motor.primitivas_extra = predicados
    motor.acumuladores_extra = acumuladores
    geometria = tu._geometria(plan)
    monkeypatch.setattr(zonas, "zona_del_punto", geometria)
    monkeypatch.setattr(primitivas_broker, "zona_del_punto", geometria)
    datos = tu._Datos(tc._h4_alcista(), list(mercado.m1))
    motor.correr_dia(DiaDeMercado(tc.DIA, tc.HUSO, tc.SESIONES, datos))
    return motor


def test_sin_ticks_el_punto_se_libera_y_se_vuelve_a_colocar_en_el_cierre_de_la_vela_del_stop(
    registro: Registro, monkeypatch: pytest.MonkeyPatch
) -> None:
    """ADR-0083 D2 con ADR-0091 §4 (la ruta de D3a de `test_punto_usado`, sin ticks): o1 se llena
    con la vela que rompe el punto y su stop salta con la vela Z+6. El stop se sella en el ultimo
    milisegundo de Z+6, el `avanzar` del cierre de Z+6 lo pasa a la cuenta y libera la zona, y en
    ESE cierre o2 vuelve al mismo punto con la misma caja. En `main` el stop se sellaba en el fin
    de Z+6, lo veia el cierre de Z+7 y o2 se colocaba un cierre despues."""
    z, e = tu.Z, tu.E
    ruta = {**tu.ANTES, z + 3: tu.ROMPE, z + 6: tu.PIERDE, z + 9: tu.ROMPE, z + 12: tu.GANA}
    motor = _correr_sin_ticks(registro, ruta, {z: tu.CAJA}, monkeypatch)
    ordenes = motor.brokers[tu.DIA].ordenes
    assert list(ordenes)[:2] == ["o1", "o2"], list(ordenes)
    p1 = motor.brokers[tu.DIA].posiciones["pos-o1"]
    assert (p1.motivo_cierre, p1.fuente_cierre, p1.cerrada_ms) == (
        STOP,
        RESPALDO_M1,
        _cierre(z + 6),
    )
    o2 = ordenes["o2"]
    assert (o2.precio, o2.stop, o2.objetivo) == (e, e - 16, e + 60)  # la misma caja
    assert o2.colocada_ms == _cierre(z + 6)  # en el cierre de la vela del stop


def test_sin_ticks_un_rechazo_al_llenar_gasta_el_punto_en_el_cierre_de_la_vela_del_llenado(
    registro: Registro, monkeypatch: pytest.MonkeyPatch
) -> None:
    """ADR-0083 D2 con ADR-0091 §4 (la ruta de D3b de `test_punto_usado`, sin ticks): la vela Z+3
    ABRE con un salto (el hueco que el respaldo llena a la apertura, ADR-0057 §1) y el llenado de
    o1 pide mas margen del que hay. El bróker la rechaza al llenar en el ultimo milisegundo de Z+3,
    el cierre de Z+3 lo ve y el punto queda gastado: la otra caja, que se ve desde Z+4, no se
    coloca. En `main` el llenado se sellaba en el fin de Z+3, y el motor ya habia cancelado la
    orden en el cierre de Z+3: la vela no llegaba a evaluarse para ella (el caso de las
    cancelaciones del censo, SELLO-RESPALDO-M1.md §0.c)."""
    z = tu.Z
    ruta = {**tu.ANTES, z + 3: tu.SALTO, z + 5: tu.E - 10}
    motor = _correr_sin_ticks(
        registro, ruta, {z: tu.CAJA, z + 4: tu.OTRA_CAJA}, monkeypatch, hueco={z + 3: tu.SALTO}
    )
    broker = motor.brokers[tu.DIA]
    o1 = broker.ordenes["o1"]
    assert (o1.estado, o1.ultimo_cambio_ms) == (RECHAZADA, _cierre(z + 3))
    assert broker.traza().rechazos[0].motivo == MOTIVO_MARGEN_LIBRE
    assert zonas.punto_rechazado(motor.estados[tu.DIA], tu.SESION, "zona:1")
    assert list(broker.ordenes) == ["o1"]
    assert all(o.estado != CANCELADA for o in broker.ordenes.values())
