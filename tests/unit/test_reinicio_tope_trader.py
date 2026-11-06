"""El reinicio del tope del trader de sesion en sesion (ADR-0089, sesion 6, S-2): con
`perdida_trader_reinicio = primera_sesion_dia_siguiente` el conteo vuelve a empezar en la apertura
de la primera sesion del dia siguiente con actividad, y la semana en la apertura del primer dia de
la semana con actividad; con `medianoche_huso`, lo de antes. Lo que dijo el trader: «La respuesta
es la C, la primera sesión del día siguiente» (ev-v17-000250-a468bcec) y, del viernes, «se vuelve a
contar desde cero el día lunes … siempre es de sesión en sesión» (ev-v17-000351-331daa6d).

`test_con_el_registro_real_corta_en_la_apertura_y_no_en_la_medianoche` y
`test_por_el_cableado_el_corte_cae_en_la_apertura_de_la_primera_sesion` fallan con el codigo de
`main`: alli no existe el modo y el corte es la medianoche del huso del perfil, SUPUESTO
(ACTIVAR-SESION-06-MOTOR.md, fase 1). Los demas son sinteticos."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from typing import Any
from zoneinfo import ZoneInfo

import pytest

from botsito.config.registro import Registro, cargar_registro
from botsito.domain.ticks import MS_POR_MINUTO, MilisegundoUtc
from botsito.domain.velas import MinutoUtc
from botsito.engine.motor import DatosMercado, DiaDeMercado
from botsito.engine.simulacion import MercadoDia
from botsito.engine.tope_trader import (
    AMBOS,
    DIA,
    MEDIANOCHE_HUSO,
    PORCENTAJE,
    PRIMERA_SESION_DIA_SIGUIENTE,
    REINICIO_DE_SESION,
    SALDO,
    SEMANA,
    SUPUESTO_HUSO,
    SeguidorTope,
    TopeTrader,
    tope_del_registro,
)
from tests.unit import test_cableado as tc

HUSO_PERFIL = ZoneInfo("Europe/Prague")
CAPITAL = Decimal(100_000)


@pytest.fixture(scope="module")
def registro() -> Registro:
    return cargar_registro(tc.RAIZ / "knowledge" / "spec" / "parametros.yaml")


def _tope(reinicio: str) -> TopeTrader:
    """Un tope sintetico de dia y semana en porcentaje, sobre el saldo inicial de cada corte."""
    return TopeTrader(
        AMBOS, SALDO, PORCENTAJE, Decimal("4.5"), Decimal(9), "saldo_inicial_dia",
        "saldo_inicial_semana", HUSO_PERFIL, False, reinicio=reinicio,
    )  # fmt: skip


def _utc(d: date, hora: int, minuto: int = 0) -> datetime:
    return datetime(d.year, d.month, d.day, hora, minuto, tzinfo=UTC)


# 2030-01-14 es lunes; las sesiones del motor abren a las 06:00Z en invierno
LUNES = date(2030, 1, 14)
MARTES = LUNES + timedelta(days=1)
VIERNES = LUNES + timedelta(days=4)
LUNES_SIG = LUNES + timedelta(days=7)
MARTES_SIG = LUNES + timedelta(days=8)


def _dos_dias(reinicio: str, saldo_medianoche: Decimal, saldo_apertura: Decimal) -> SeguidorTope:
    """El lunes abre con CAPITAL; el martes, el saldo vale `saldo_medianoche` al cruzar la
    medianoche del huso y `saldo_apertura` en la apertura de su primera sesion. Asi lo alimenta el
    cableado: `abrir_dia` al empezar cada dia, `avanzar` en cada cierre de M1."""
    s = SeguidorTope(_tope(reinicio), _utc(LUNES, 6) - timedelta(milliseconds=1), CAPITAL)
    s.abrir_dia(LUNES, _utc(LUNES, 6), CAPITAL)
    s.avanzar(_utc(LUNES, 23, 30), saldo_medianoche)  # la medianoche de Praga (23:00Z) ya paso
    s.abrir_dia(MARTES, _utc(MARTES, 6), saldo_apertura)
    s.avanzar(_utc(MARTES, 6, 1), saldo_apertura)
    return s


def test_si_el_saldo_cambia_entre_medianoche_y_apertura_los_dos_modos_dan_bases_distintas() -> None:
    medianoche = _dos_dias(MEDIANOCHE_HUSO, Decimal(99_000), Decimal(98_000))
    sesion = _dos_dias(PRIMERA_SESION_DIA_SIGUIENTE, Decimal(99_000), Decimal(98_000))
    assert medianoche.saldo_corte_dia == Decimal(99_000)  # el de la medianoche
    assert sesion.saldo_corte_dia == Decimal(98_000)  # el de la apertura
    assert medianoche.cortes == [(_utc(LUNES, 23), DIA)]
    assert sesion.cortes == [(_utc(MARTES, 6), DIA)]
    # la misma caida medida desde cada corte
    caida = Decimal(97_000)
    assert (
        medianoche.acumuladores(caida, caida)["perdida_dia"]
        != sesion.acumuladores(caida, caida)["perdida_dia"]
    )


def test_si_el_saldo_no_cambia_entre_la_medianoche_y_la_apertura_dan_la_misma_base() -> None:
    medianoche = _dos_dias(MEDIANOCHE_HUSO, Decimal(99_000), Decimal(99_000))
    sesion = _dos_dias(PRIMERA_SESION_DIA_SIGUIENTE, Decimal(99_000), Decimal(99_000))
    assert medianoche.saldo_corte_dia == sesion.saldo_corte_dia == Decimal(99_000)
    caida = Decimal(97_000)
    assert medianoche.acumuladores(caida, caida) == sesion.acumuladores(caida, caida)
    # el instante del corte sigue siendo distinto: la medianoche frente a la apertura
    assert medianoche.cortes != sesion.cortes


def test_un_viernes_corta_el_lunes_al_abrir_y_la_semana_con_el() -> None:
    s = SeguidorTope(_tope(PRIMERA_SESION_DIA_SIGUIENTE), _utc(VIERNES, 6), CAPITAL)
    s.abrir_dia(VIERNES, _utc(VIERNES, 6), CAPITAL)
    # el sabado y el domingo no corren: el seguidor no corta nada aunque pasen medianoches
    s.avanzar(_utc(VIERNES + timedelta(days=2), 12), Decimal(95_000))
    assert s.cortes == [] and s.saldo_corte_dia == CAPITAL
    s.abrir_dia(LUNES_SIG, _utc(LUNES_SIG, 6), Decimal(95_000))
    assert s.cortes == [(_utc(LUNES_SIG, 6), DIA), (_utc(LUNES_SIG, 6), SEMANA)]
    assert s.saldo_corte_dia == s.saldo_corte_semana == Decimal(95_000)


def test_si_el_lunes_no_tiene_sesiones_la_semana_corta_el_primer_dia_con_actividad() -> None:
    s = SeguidorTope(_tope(PRIMERA_SESION_DIA_SIGUIENTE), _utc(VIERNES, 6), CAPITAL)
    s.abrir_dia(VIERNES, _utc(VIERNES, 6), CAPITAL)
    s.abrir_dia(MARTES_SIG, _utc(MARTES_SIG, 6), Decimal(96_000))
    assert s.cortes == [(_utc(MARTES_SIG, 6), DIA), (_utc(MARTES_SIG, 6), SEMANA)]
    # y dentro de la misma semana solo corta el dia
    s.abrir_dia(MARTES_SIG + timedelta(days=1), _utc(MARTES_SIG + timedelta(days=1), 6), CAPITAL)
    assert s.cortes[-1] == (_utc(MARTES_SIG + timedelta(days=1), 6), DIA)
    assert s.saldo_corte_semana == Decimal(96_000)


def test_el_mismo_dia_otra_vez_no_corta() -> None:
    s = SeguidorTope(_tope(PRIMERA_SESION_DIA_SIGUIENTE), _utc(LUNES, 6), CAPITAL)
    s.abrir_dia(LUNES, _utc(LUNES, 6), CAPITAL)
    s.abrir_dia(LUNES, _utc(LUNES, 6), Decimal(1))
    assert s.cortes == [] and s.saldo_corte_dia == CAPITAL


def test_con_la_medianoche_abrir_dia_no_hace_nada() -> None:
    s = SeguidorTope(_tope(MEDIANOCHE_HUSO), _utc(LUNES, 6), CAPITAL)
    s.abrir_dia(LUNES, _utc(LUNES, 6), CAPITAL)
    s.abrir_dia(MARTES, _utc(MARTES, 6), Decimal(1))
    assert s.cortes == [] and s.saldo_corte_dia == CAPITAL


def test_con_el_registro_real_corta_en_la_apertura_y_no_en_la_medianoche(
    registro: Registro,
) -> None:
    """El registro real (sesion 6, S-2): `perdida_trader_reinicio` CONFIRMED en
    `primera_sesion_dia_siguiente`, sin huso y sin SUPUESTO; el seguidor no corta al cruzar la
    medianoche y si en la apertura del dia siguiente. Falla con el codigo de `main`."""
    t = tope_del_registro(registro, HUSO_PERFIL)
    assert t.reinicio == PRIMERA_SESION_DIA_SIGUIENTE
    assert not t.huso_supuesto
    assert REINICIO_DE_SESION in t.descripcion() and SUPUESTO_HUSO not in t.descripcion()
    s = SeguidorTope(t, _utc(LUNES, 6) - timedelta(milliseconds=1), CAPITAL)
    s.abrir_dia(LUNES, _utc(LUNES, 6), CAPITAL)
    s.avanzar(_utc(MARTES, 1), Decimal(99_000))
    assert s.cortes == []
    s.abrir_dia(MARTES, _utc(MARTES, 6), Decimal(99_000))
    assert s.cortes == [(_utc(MARTES, 6), DIA)]


def test_por_el_cableado_el_corte_cae_en_la_apertura_de_la_primera_sesion(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    """Por el cableado real (`MotorCableado.correr_dia`) y el registro real, dos dias seguidos
    (el mercado sintetico de test_cableado con RUTA_STOP -la orden del dia 1 se llena y salta el
    stop, asi que el saldo baja- y el mismo desplazado un dia, sin orden: la zona sintetica solo se
    liga en el minuto del dia 1): el primer dia no corta; el segundo corta en la apertura de su
    primera sesion (las 06:00Z del 2030-01-16, la sesion 07-11 de Madrid en invierno) con el saldo
    arrastrado del dia 1, distinto del capital, y no en la medianoche de Praga que cae entre los
    dos. Falla con el codigo de `main`. Hasta la respuesta al revisor (a2) el mercado era plano, la
    orden no se llenaba y el saldo no cambiaba: el test no probaba el arrastre."""
    md1 = tc._mercado(tc.RUTA_STOP)
    md2 = MercadoDia(
        "caso-x-2030-01-16",
        DIA_2,
        MinutoUtc(int(md1.desde) + MINUTOS_DIA),
        MinutoUtc(int(md1.hasta) + MINUTOS_DIA),
        md1.escala,
        tuple(replace(v, inicio=MinutoUtc(int(v.inicio) + MINUTOS_DIA)) for v in md1.m1),
        tuple(
            replace(t, instante=MilisegundoUtc(int(t.instante) + MINUTOS_DIA * MS_POR_MINUTO))
            for t in md1.ticks
        ),
        md1.origen_ticks,
        md1.horas_perdidas,
    )
    motor = tc._motor(registro, vocabulario, md1)
    motor.mercados = {tc.DIA.isoformat(): md1, DIA_2.isoformat(): md2}
    motor.tope = tope_del_registro(registro, HUSO_PERFIL)
    motor.correr_dia(tc._dia())
    assert motor.seguidor is not None and motor.cuenta is not None
    assert motor.seguidor.dia_de_sesion == tc.DIA and motor.seguidor.cortes == []
    saldo_fin_dia_1 = motor.cuenta.saldo
    assert saldo_fin_dia_1 < motor.seguidor.saldo_corte_dia  # el stop del dia 1 costo dinero
    motor.correr_dia(DiaDeMercado(DIA_2, tc.HUSO, tc.SESIONES, DatosMercado(tc._h4_alcista())))
    apertura = datetime.fromtimestamp((tc.MINUTO_INI + MINUTOS_DIA) * MS_POR_MINUTO / 1000, UTC)
    assert motor.seguidor.cortes == [(apertura, DIA)]
    assert motor.seguidor.saldo_corte_dia == saldo_fin_dia_1


DIA_2 = tc.DIA + timedelta(days=1)
MINUTOS_DIA = 1440


@pytest.fixture(scope="module")
def vocabulario() -> dict[str, dict[str, Any]]:
    from botsito.spec.modelo import cargar_vocabulario

    return cargar_vocabulario(tc.SPEC)
