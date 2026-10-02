"""El freno de peticiones al servidor (rama `feature/freno-peticiones`, ADR-0067), rompiendo la
guardia a proposito: un bucle de 5.000 peticiones, el corte con lo que protege la cuenta, el dia de
la firma frente a la sesion, ninguna posicion sin stop, y el dia normal sin tocar ningun umbral.
Ticks y dias SINTETICOS de 2030; sin cobertura agregada."""

from __future__ import annotations

from datetime import UTC, date, datetime
from decimal import Decimal
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from botsito.config.registro import cargar_registro
from botsito.data.velas import a_minuto
from botsito.domain.ticks import MS_POR_MINUTO, MilisegundoUtc, Tick
from botsito.domain.valores import Puntos
from botsito.engine.broker import (
    PETICION_CANCELAR,
    PETICION_CERRAR,
    PETICION_COLOCAR,
    PETICION_MODIFICAR,
    Broker,
    BrokerError,
    Orden,
    Rechazo,
    ReglasBroker,
)
from botsito.engine.freno import (
    MOTIVO_AVISO,
    MOTIVO_BUCLE,
    MOTIVO_CORTE,
    FrenoError,
    FrenoPeticiones,
    LimitesFreno,
)
from botsito.engine.llenado import Configuracion, Mercado
from botsito.engine.simulacion import limites_freno_de
from tests.unit import test_cableado as tc
from tests.unit import test_escenarios_por_sesion as tes

RAIZ = Path(__file__).resolve().parents[2]
REGISTRO = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
LIMITES = limites_freno_de(REGISTRO)  # los del registro, PROVISIONAL bajo A-54
PRAGA = ZoneInfo("Europe/Prague")  # el reloj de corte del perfil de FTMO (firma_huso_corte)
SPREAD = 3
UNO = Decimal(1)
BID = 1_000_000
M0 = int(a_minuto(datetime(2030, 7, 15, 6, 0, tzinfo=UTC)))  # 08:00 en Praga, en verano


def _ms(minuto: int, segundo: int = 0) -> int:
    return minuto * MS_POR_MINUTO + segundo * 1000


def _broker(limites: LimitesFreno | None = LIMITES, mensajes_dia_max: int = 2000) -> Broker:
    reglas = ReglasBroker(
        volumen_max_lotes=Decimal(10),
        ordenes_simultaneas_max=10_000,
        posiciones_dia_max=10_000,
        huso_corte=PRAGA,
        comision_por_lote=Decimal(0),
        comision_por_lado=False,
        swap_largo_puntos=Decimal(0),
        swap_corto_puntos=Decimal(0),
        mensajes_dia_max=mensajes_dia_max,
        freno=limites,
    )
    tick = Tick(MilisegundoUtc(_ms(M0)), Puntos(BID + SPREAD), Puntos(BID), 0, 0)
    return Broker(reglas, Configuracion(False, 0, lambda _m: SPREAD), Mercado([tick], []), UNO, 1)


def _compra(b: Broker, i: int, instante_ms: int, precio: int | None = None) -> Orden | Rechazo:
    """Una compra limite por debajo del precio, distinta en cada i (salvo que se fije el precio)."""
    p = precio if precio is not None else BID - 1000 - i
    return b.colocar_limite(f"o{i}", "compra", p, UNO, p - 100, p + 300, instante_ms)


def _negadas(b: Broker) -> list[str]:
    return [c.motivo for c in b.traza().cortes if c.motivo != MOTIVO_AVISO]


def test_los_umbrales_del_registro_van_por_debajo_de_las_2000_con_margen() -> None:
    assert LIMITES.aviso is not None and LIMITES.aviso < LIMITES.corte
    assert LIMITES.corte < REGISTRO.entero("firma_mensajes_dia_max")
    assert LIMITES.bucle_repeticiones is not None and LIMITES.bucle_ms is not None
    for nombre in (
        "freno_peticiones_aviso",
        "freno_peticiones_corte",
        "freno_bucle_repeticiones",
        "freno_bucle_minutos",
    ):
        assert REGISTRO.parametros[nombre].ambiguedad_id == "A-54"  # PROVISIONAL


# ------------------------------------------------------------------ un bucle de 5.000 peticiones


def test_un_bucle_de_5000_peticiones_distintas_no_pasa_del_corte() -> None:
    """5.000 compras distintas, una por segundo: salen tantas como el corte, el resto se niega
    -sin llegar al servidor ni contarse- y el dia queda con un aviso y 5.000 - corte negadas."""
    b = _broker()
    for i in range(5000):
        _compra(b, i, _ms(M0, 1) + i * 1000)
    traza = b.traza()
    assert len(traza.peticiones) == LIMITES.corte
    assert _negadas(b) == [MOTIVO_CORTE] * (5000 - LIMITES.corte)
    assert [c.motivo for c in traza.cortes].count(MOTIVO_AVISO) == 1
    assert len(b.ordenes) == LIMITES.corte  # las negadas no existen


def test_un_bucle_de_5000_peticiones_iguales_lo_para_el_freno_de_bucles() -> None:
    """5.000 veces la MISMA compra (ids nuevos), seguidas: el freno de bucles corta en la
    repeticion N, mucho antes del corte del dia, y no sale ni una mas ese dia."""
    b = _broker()
    n = LIMITES.bucle_repeticiones
    assert n is not None
    for i in range(5000):
        _compra(b, i, _ms(M0, 1) + i * 100, precio=BID - 1000)
    assert len(b.traza().peticiones) == n - 1
    assert _negadas(b) == [MOTIVO_BUCLE] * (5000 - (n - 1))


def test_el_bucle_cuenta_las_iguales_aunque_haya_otras_en_medio_y_solo_en_su_ventana() -> None:
    """La reubicacion alterna cancelar y colocar: colocar la misma orden con cancelar en medio es
    un bucle. Las mismas iguales, espaciadas mas que la ventana, no lo son."""
    n, ventana = LIMITES.bucle_repeticiones, LIMITES.bucle_ms
    assert n is not None and ventana is not None
    b = _broker()
    for i in range(n):
        orden = _compra(b, i, _ms(M0, 1) + i * 1000, precio=BID - 1000)
        if isinstance(orden, Orden):
            b.cancelar(orden.id, _ms(M0, 1) + i * 1000 + 500)
    assert _negadas(b) == [MOTIVO_BUCLE]
    espaciado = _broker()
    for i in range(n * 3):
        _compra(espaciado, i, _ms(M0, 1) + i * ventana, precio=BID - 1000)
    assert _negadas(espaciado) == []


# --------------------------------------------------------------------- lo que protege, sale


def test_al_llegar_al_corte_cancelar_cerrar_y_el_break_even_salen_y_cuentan() -> None:
    corte = LimitesFreno(corte=3)
    b = _broker(corte)
    pendiente = _compra(b, 0, _ms(M0, 1))
    assert isinstance(pendiente, Orden)
    pos = b.abrir_conocida("p1", "compra", BID, UNO, BID - 200, BID + 600, _ms(M0, 2))
    _compra(b, 1, _ms(M0, 3))
    _compra(b, 2, _ms(M0, 4))
    assert isinstance(_compra(b, 3, _ms(M0, 5)), Rechazo)  # el corte: 3 enviadas
    assert b.freno is not None and b.freno.cortado() == MOTIVO_CORTE
    b.cancelar(pendiente.id, _ms(M0, 6))
    b.mover_stop(pos.id, BID, _ms(M0, 7))  # el break even: hacia el lado que reduce el riesgo
    b.cerrar_a_mercado(pos.id, _ms(M0, 8))
    tipos = [p.tipo for p in b.traza().peticiones]
    assert tipos[-3:] == [PETICION_CANCELAR, PETICION_MODIFICAR, PETICION_CERRAR]
    assert len(tipos) == 6  # las tres que protegen CUENTAN, por encima del corte
    assert pendiente.estado == "cancelada" and not pos.abierta and pos.stop_original is not None


# ------------------------------------------------------------- el dia de la firma, no la sesion


def test_el_contador_vuelve_a_cero_con_el_dia_de_la_firma_no_con_la_sesion() -> None:
    """Con el corte en 2: en verano, en Praga, el dia 15 acaba a las 22:00Z. Cruzar el cambio de
    sesion (las 11:00 de Madrid, 09:00Z) no lo vuelve a cero; cruzar la medianoche de la firma,
    si."""
    b = _broker(LimitesFreno(corte=2))
    manana = int(a_minuto(datetime(2030, 7, 15, 8, 58, tzinfo=UTC)))
    _compra(b, 0, _ms(manana))
    _compra(b, 1, _ms(manana + 1))
    tarde = int(a_minuto(datetime(2030, 7, 15, 9, 1, tzinfo=UTC)))  # ya en la sesion de la tarde
    assert isinstance(_compra(b, 2, _ms(tarde)), Rechazo)
    fin = int(a_minuto(datetime(2030, 7, 15, 21, 59, tzinfo=UTC)))
    assert isinstance(_compra(b, 3, _ms(fin, 59)), Rechazo)  # 23:59:59 en Praga: aun el 15
    nuevo = int(a_minuto(datetime(2030, 7, 15, 22, 0, tzinfo=UTC)))  # 00:00 en Praga: el 16
    assert isinstance(_compra(b, 4, _ms(nuevo)), Orden)
    assert b.freno is not None and b.freno.total() == 1 and b.freno.cortado() is None


def test_el_dia_lo_da_el_broker_y_el_freno_no_lo_supone() -> None:
    f = FrenoPeticiones(LimitesFreno(corte=1))
    assert f.admitir(date(2030, 7, 15), 0, PETICION_COLOCAR, "a", ("x",), False) is None
    assert f.admitir(date(2030, 7, 15), 1, PETICION_COLOCAR, "b", ("y",), False) == MOTIVO_CORTE
    assert f.admitir(date(2030, 7, 16), 2, PETICION_COLOCAR, "c", ("z",), False) is None


# ---------------------------------------------------------------- ninguna posicion sin stop


def test_ninguna_posicion_queda_sin_stop_por_el_freno() -> None:
    """Con el dia cortado: un stop hacia FUERA se niega y la posicion conserva el suyo; el break
    even sale; una orden negada no existe y no puede llenarse sin stop. Todas las posiciones
    tienen siempre stop, del lado correcto."""
    b = _broker(LimitesFreno(corte=1))
    larga = b.abrir_conocida("p1", "compra", BID, UNO, BID - 200, BID + 600, _ms(M0, 1))
    corta = b.abrir_conocida("p2", "venta", BID, UNO, BID + 200, BID - 600, _ms(M0, 1))
    _compra(b, 0, _ms(M0, 2))  # la unica que sale: el dia queda cortado
    assert isinstance(_compra(b, 1, _ms(M0, 3)), Rechazo)
    b.mover_stop(larga.id, BID - 500, _ms(M0, 4))  # hacia fuera: negado
    b.mover_stop(corta.id, BID + 500, _ms(M0, 5))  # hacia fuera: negado
    assert (larga.stop, corta.stop) == (BID - 200, BID + 200)
    b.mover_stop(corta.id, BID, _ms(M0, 6))  # el break even: sale
    assert corta.stop == BID
    assert "o1" not in b.ordenes
    for p in b.posiciones.values():
        assert p.stop is not None
        assert p.stop <= p.entrada if p.lado == "compra" else p.stop >= p.entrada
    assert _negadas(b) == [MOTIVO_CORTE] * 3


# --------------------------------------------------------------------- el dia normal


def test_el_dia_de_cinco_escenarios_no_toca_ningun_umbral(tmp_path: Path) -> None:
    """El dia sintetico de cinco escenarios de `feature/escenarios-por-sesion` (10 peticiones) por
    el cableado real, con los umbrales del registro: ni aviso ni nada negado."""
    reg = tes._registro(tmp_path)
    motor = tes._motor_dos_tomas(reg, tes.CINCO_TOMAS)
    motor.correr_dia(tes._dia_dos_tomas(tes.CINCO_TOMAS))
    assert motor.reglas_broker.freno == LIMITES
    tb = motor.trazas_broker[tc.DIA.isoformat()]
    assert len(tb.peticiones) == 2 * len(tes.CINCO_TOMAS)
    assert tb.cortes == []


@pytest.mark.parametrize("n", [10, 13])
def test_un_dia_de_10_a_13_peticiones_no_toca_ningun_umbral(n: int) -> None:
    """Los dias de desarrollo medidos daban 10 y 13 peticiones (ESCENARIOS-POR-SESION.md §6.4):
    colocar, cancelar y reubicar a precios distintos, a lo largo de la manana."""
    b = _broker()
    for i in range(n):
        orden = _compra(b, i, _ms(M0 + 10 * i, 1))
        if isinstance(orden, Orden) and i % 2:
            b.cancelar(orden.id, _ms(M0 + 10 * i, 30))
    assert b.traza().cortes == ()
    assert b.freno is not None and b.freno.total() < (LIMITES.aviso or 0)


# ----------------------------------------------------------------- los umbrales, sanos


def test_unos_umbrales_sin_sentido_no_arman_el_freno() -> None:
    with pytest.raises(FrenoError):
        LimitesFreno(corte=0)
    with pytest.raises(FrenoError):
        LimitesFreno(corte=10, aviso=10)
    with pytest.raises(FrenoError):
        LimitesFreno(corte=10, bucle_repeticiones=3)
    with pytest.raises(BrokerError, match="pasa del limite de la firma"):
        _broker(LimitesFreno(corte=2001))
