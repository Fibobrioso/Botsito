"""RN-036, la racha de perdidas seguidas del trader (A-51 RESUELTA en la sesion 4, S-8; ADR-0077):
nueve perdidas con un break even en medio detienen hasta el dia siguiente; una ganadora a la
octava la pone a cero; la racha cruza un fin de semana; la orden pendiente se retira en la novena;
las opciones sin contrato se niegan; y el cableado, nueve dias seguidos con `tope=None` (sin A-44 y
sin --diagnostico-a44), deja de colocar el noveno y vuelve a operar el decimo. Todo sintetico; el
dia es de 2030 y no hay ninguna fecha real."""

from __future__ import annotations

import dataclasses
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest

from botsito.config.registro import Registro, cargar_registro
from botsito.domain.ticks import MS_POR_MINUTO, MilisegundoUtc, Tick
from botsito.domain.velas import MinutoUtc
from botsito.engine import cableado, racha
from botsito.engine.broker import CANCELADA, PETICION_CANCELAR, Broker, Rechazo
from botsito.engine.cuenta import CuentaViva, reglas_de_fase
from botsito.engine.interprete import EstadoDia, Momento, NoImplementada, Resultado, Tri
from botsito.engine.llenado import Configuracion
from botsito.engine.motor import DatosMercado, DiaDeMercado
from botsito.engine.perfil_cuenta import cargar_perfil
from botsito.engine.primitivas_broker import ContextoDia, primitivas_cableadas
from botsito.engine.racha import (
    SeguidorRacha,
    cuenta_como_perdida,
    seguidor_del_registro,
)
from botsito.engine.relojes import reloj_de_las_sesiones
from botsito.engine.simulacion import reglas_broker_de
from tests.unit import test_cableado as tc

RAIZ = Path(__file__).resolve().parents[2]
TOPE = 9
# 2030-01-15 es martes (test_cableado): nueve dias de mercado seguidos, saltando los dos fines de
# semana, y el decimo
DIAS = [
    date(2030, 1, 15), date(2030, 1, 16), date(2030, 1, 17), date(2030, 1, 18),
    date(2030, 1, 21), date(2030, 1, 22), date(2030, 1, 23), date(2030, 1, 24), date(2030, 1, 25),
    date(2030, 1, 28),
]  # fmt: skip


@pytest.fixture(scope="module")
def registro() -> Registro:
    return cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")


@pytest.fixture(scope="module")
def vocabulario() -> dict[str, dict[str, Any]]:
    from botsito.spec.modelo import cargar_vocabulario

    return cargar_vocabulario(tc.SPEC)


def _ms(dia: date, hora_utc: int) -> int:
    """Un instante UTC del dia, en milisegundos, dentro de la ventana (las 8 UTC es la manana)."""
    from datetime import UTC, datetime

    return int(datetime(dia.year, dia.month, dia.day, hora_utc, tzinfo=UTC).timestamp() * 1000)


def _seguidor(registro: Registro) -> SeguidorRacha:
    return seguidor_del_registro(registro)


# -------------------------------------------------------------------- el registro y el criterio


def test_los_cuatro_parametros_son_del_trader_y_estan_confirmados(registro: Registro) -> None:
    """A-51 RESUELTA (sesion 4, S-8): los valores, con su fuente de feedback."""
    assert registro.entero(racha.P_MAX) == TOPE
    assert registro.opcion(racha.P_CORTE) == racha.CORTE_GANADORA
    assert registro.opcion(racha.P_REINICIO) == racha.REINICIO_NUNCA
    assert registro.opcion(racha.P_REANUDACION) == racha.REANUDACION_DIA_SIGUIENTE
    for nombre in (racha.P_MAX, racha.P_CORTE, racha.P_REINICIO, racha.P_REANUDACION):
        p = registro.parametros[nombre]
        assert p.estado.value == "CONFIRMED" and p.categoria == "estrategia", nombre
        assert p.fuente is not None and p.fuente.tipo == "feedback", nombre


def test_una_perdida_es_lo_que_gasta_un_cartucho_en_rn016() -> None:
    """La misma definicion que RN-016 (ADR-0077 §2): salto el stop por cualquier activacion, o
    perdida de un esquema; un break even, una ganancia o la salida en rojo sin stop de una
    activacion sin ruptura, no."""
    criterio = "solo_perdida"
    assert cuenta_como_perdida(criterio, "salto_el_stop", "activacion_sin_ruptura")
    assert cuenta_como_perdida(criterio, "salto_el_stop", "primer_esquema")
    assert cuenta_como_perdida(criterio, "perdida", "segundo_esquema")
    assert not cuenta_como_perdida(criterio, "perdida", "activacion_sin_ruptura")
    assert not cuenta_como_perdida(criterio, "break_even", "primer_esquema")
    assert not cuenta_como_perdida(criterio, "ganancia", "primer_esquema")
    assert cuenta_como_perdida("todo_intento", "break_even", None)
    with pytest.raises(racha.RachaError, match="cartucho_criterio"):
        cuenta_como_perdida("a_ojo", "perdida", None)


def test_las_opciones_sin_contrato_se_niegan(registro: Registro) -> None:
    reloj = reloj_de_las_sesiones(registro)
    for corte, reinicio, reanudacion, texto in (
        ("a_ojo", "nunca", "dia_siguiente", "racha_perdidas_corte"),
        ("ganadora", "fin_de_dia", "dia_siguiente", "racha_perdidas_reinicio"),
        ("ganadora", "nunca", "semana_siguiente", "racha_perdidas_reanudacion"),
    ):
        with pytest.raises(racha.RachaError, match=texto):
            SeguidorRacha(reloj, "solo_perdida", corte, reinicio, reanudacion)


# ------------------------------------------------------------------------------ el seguidor


def test_nueve_perdidas_con_un_break_even_en_medio_detienen_hasta_el_dia_siguiente(
    registro: Registro,
) -> None:
    s = _seguidor(registro)
    dia = DIAS[0]
    for k in range(7):
        s.registrar(_ms(dia, 8) + k * MS_POR_MINUTO, "salto_el_stop", "primer_esquema")
    assert s.racha == 7 and not s.detenido(_ms(dia, 9), TOPE)
    s.registrar(_ms(dia, 9), "break_even", "primer_esquema")  # «no corta la racha»
    assert s.racha == 7 and not s.detenido(_ms(dia, 9), TOPE)
    s.registrar(_ms(dia, 10), "perdida", "segundo_esquema")  # «nuevamente lo contamos»
    assert s.racha == 8 and not s.detenido(_ms(dia, 10), TOPE)
    s.registrar(_ms(dia, 11), "salto_el_stop", "activacion_sin_ruptura")  # la novena
    assert s.racha == 9 and s.detenido(_ms(dia, 11), TOPE) and s.detenido(_ms(dia, 13), TOPE)
    # el dia siguiente se vuelve, con la racha intacta: `reinicio` = nunca
    assert not s.detenido(_ms(DIAS[1], 8), TOPE) and s.racha == 9
    # y la decima vuelve a detener el dia en que cae (ADR-0077 §5)
    s.registrar(_ms(DIAS[1], 9), "salto_el_stop", "primer_esquema")
    assert (
        s.racha == 10
        and s.detenido(_ms(DIAS[1], 10), TOPE)
        and not s.detenido(_ms(DIAS[2], 8), TOPE)
    )


def test_una_ganadora_a_la_octava_pone_la_racha_a_cero(registro: Registro) -> None:
    s = _seguidor(registro)
    dia = DIAS[0]
    for k in range(7):
        s.registrar(_ms(dia, 8) + k * MS_POR_MINUTO, "salto_el_stop", "primer_esquema")
    s.registrar(_ms(dia, 9), "ganancia", "primer_esquema")
    assert s.racha == 0 and not s.detenido(_ms(dia, 9), TOPE)
    for k in range(8):
        s.registrar(_ms(dia, 10) + k * MS_POR_MINUTO, "salto_el_stop", "primer_esquema")
    assert s.racha == 8 and not s.detenido(_ms(dia, 11), TOPE)


def test_la_racha_cruza_un_fin_de_semana(registro: Registro) -> None:
    """«la racha sigue de un día a otro y una semana otra»: cinco perdidas el viernes y cuatro el
    lunes son nueve, y detienen el lunes."""
    s = _seguidor(registro)
    viernes, lunes = DIAS[3], DIAS[4]
    assert viernes.isoweekday() == 5 and lunes.isoweekday() == 1
    for k in range(5):
        s.registrar(_ms(viernes, 8) + k * MS_POR_MINUTO, "salto_el_stop", "primer_esquema")
    for k in range(3):
        s.registrar(_ms(lunes, 8) + k * MS_POR_MINUTO, "salto_el_stop", "primer_esquema")
    assert s.racha == 8 and not s.detenido(_ms(lunes, 9), TOPE)
    s.registrar(_ms(lunes, 9), "salto_el_stop", "primer_esquema")
    assert (
        s.racha == 9 and s.detenido(_ms(lunes, 10), TOPE) and not s.detenido(_ms(DIAS[5], 8), TOPE)
    )


def test_el_dia_de_la_detencion_es_el_operativo_del_reloj_de_las_sesiones(
    registro: Registro,
) -> None:
    s = _seguidor(registro)
    dia = DIAS[0]
    assert s.dia_operativo(_ms(dia, 8)) == dia  # las 8 UTC: la manana del martes, en la rejilla
    assert s.dia_operativo(_ms(dia, 13)) == dia  # y la tarde


# ------------------------------------------------------------------- el acumulador y la accion


def _contexto(registro: Registro) -> tuple[ContextoDia, Broker]:
    perfil = cargar_perfil(tc.PERFIL)
    md = tc._mercado({})
    broker = Broker(
        reglas_broker_de(perfil, registro),
        Configuracion(False, 0, lambda _m: tc.SPREAD),
        md.mercado(),
        registro.decimal("instrumento_contrato"),
        md.escala,
    )
    cuenta = CuentaViva(
        reglas_de_fase(perfil, "reto"),
        registro.decimal("instrumento_contrato"),
        tc.MINUTO_INI * MS_POR_MINUTO - 1,
    )
    ctx = ContextoDia(broker, cuenta, registro.decimal("instrumento_contrato"), md.escala)
    return ctx, broker


def test_la_orden_pendiente_se_retira_en_la_novena(registro: Registro) -> None:
    """La accion de RN-036 (`retirar_ordenes_pendientes`, decision del consultor, ADR-0077 §3):
    con una limite pendiente la cancela y refresca los hechos del broker; sin ninguna, no hace
    nada (idempotente)."""
    ctx, broker = _contexto(registro)
    ms = tc.MINUTO_ZONA * MS_POR_MINUTO - 1
    o = broker.colocar_limite("o1", "compra", tc.ENTRADA, Decimal("0.1"), tc.EXTREMO + 4,
                              tc.ENTRADA + 60, ms)  # fmt: skip
    assert not isinstance(o, Rechazo), o  # aceptada
    ctx.instante_ms = ms + MS_POR_MINUTO
    estado = EstadoDia(broker=broker.hechos())
    assert estado.broker["orden_limite_pendiente"] is True
    primitivas = primitivas_cableadas(registro, ctx)
    accion = primitivas.acciones["retirar_ordenes_pendientes"]
    momento = Momento(MinutoUtc(tc.MINUTO_ZONA + 1), "07-11", False, None)
    assert accion({}, {}, momento, estado) == []
    assert broker.ordenes["o1"].estado == CANCELADA
    assert estado.broker["orden_limite_pendiente"] is False
    assert [p.tipo for p in broker.traza().peticiones][-1] == PETICION_CANCELAR
    n = len(broker.traza().peticiones)
    assert accion({}, {}, momento, estado) == [] and len(broker.traza().peticiones) == n


def test_el_acumulador_lee_el_seguidor_y_sin_seguidor_es_hueco(registro: Registro) -> None:
    ctx, _ = _contexto(registro)
    primitivas = primitivas_cableadas(registro, ctx)
    leer = primitivas.acumuladores["racha_perdidas"]
    args = {"acumulador": "racha_perdidas", "tope": "racha_perdidas_max"}
    momento = Momento(MinutoUtc(tc.MINUTO_ZONA), "07-11", False, None)
    r = leer(args, momento, EstadoDia())
    assert isinstance(r, NoImplementada) and r.id == "acumulador:racha_perdidas"
    ctx.racha = _seguidor(registro)
    assert leer(args, momento, EstadoDia()) == Resultado(Tri.NO)
    for k in range(TOPE):
        ctx.racha.registrar(tc.MINUTO_ZONA * MS_POR_MINUTO + k, "salto_el_stop", "primer_esquema")
    assert leer(args, momento, EstadoDia()) == Resultado(Tri.SI)
    manana = Momento(MinutoUtc(tc.MINUTO_ZONA + 1440), "07-11", False, None)
    assert leer(args, manana, EstadoDia()) == Resultado(Tri.NO)


# ---------------------------------------------------------------------- el cableado, nueve dias


def _mercado_del_dia(dia: date, ruta: dict[int, int]) -> Any:
    # la ruta se aplica sobre el dia sintetico y DESPUES se desplaza entera (como el test de dos
    # dias de test_cableado): `_mercado` solo recorre los minutos del dia 2030-01-15
    salto = (dia - tc.DIA).days * 1440
    m = tc._mercado(ruta)
    return dataclasses.replace(
        m,
        caso=f"caso-x-{dia.isoformat()}",
        dia=dia,
        desde=MinutoUtc(tc.MINUTO_INI + salto),
        hasta=MinutoUtc(tc.MINUTO_FIN + salto),
        m1=tuple(dataclasses.replace(v, inicio=MinutoUtc(int(v.inicio) + salto)) for v in m.m1),
        ticks=tuple(
            Tick(
                MilisegundoUtc(int(k.instante) + salto * MS_POR_MINUTO),
                k.ask,
                k.bid,
                k.volumen_ask,
                k.volumen_bid,
            )  # fmt: skip
            for k in m.ticks
        ),
    )


def _sinteticas_dos_zonas(minuto_zona: int) -> tuple[dict[str, Any], dict[str, Any]]:
    """La estrategia sintetica de test_cableado con una SEGUNDA zona, lejos del precio (no se
    llena), diez minutos despues de la primera: si RN-036 ha detenido el dia, no se coloca."""
    predicados, acumuladores = tc._sinteticas(minuto_zona)
    puestas: set[int] = set()

    def toca(args: Any, momento: Momento, estado: EstadoDia) -> Resultado:
        t = int(momento.instante)
        if t == minuto_zona and t not in puestas:
            puestas.add(t)
            return Resultado(Tri.SI, {"Z": "zona:1"})
        if t == minuto_zona + 10 and t not in puestas:
            puestas.add(t)
            return Resultado(Tri.SI, {"Z": "zona:2"})
        return Resultado(Tri.NO)

    predicados["toca_colocar_orden_limite"] = toca
    return predicados, acumuladores


def test_el_cableado_detiene_el_noveno_dia_y_vuelve_a_operar_el_decimo(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    """Nueve dias con una perdida cada uno (RUTA_STOP), con `tope=None`: RN-036 corre sin A-44 y
    sin --diagnostico-a44. Los ocho primeros dias colocan la segunda orden (lejos, pendiente, que
    RN-035 retira al abrir la tarde); el noveno, tras la novena perdida, RN-036 dispara, fija
    `detenido_por_racha`, la segunda colocacion queda prohibida y no hay ninguna pendiente que el
    cableado cancele al fin del dia; el decimo dia vuelve a operar con la racha en 9, y su perdida
    -la decima- vuelve a detener."""
    motor = tc._motor(registro, vocabulario, tc._mercado(tc.RUTA_STOP))
    assert motor.tope is None
    motor.mercados = {d.isoformat(): _mercado_del_dia(d, tc.RUTA_STOP) for d in DIAS}
    zona_lejos = cableado.zona_sintetica(
        "zona:2", "compra", tc.ENTRADA - 400, tc.ENTRADA - 420, "primer_esquema"
    )
    zona = cableado.zona_sintetica("zona:1", "compra", tc.ENTRADA, tc.EXTREMO, "primer_esquema")
    motor.zonas_de = lambda md: {"zona:1": zona, "zona:2": zona_lejos}
    resultados = []
    for dia in DIAS:
        salto = (dia - tc.DIA).days * 1440
        predicados, acumuladores = _sinteticas_dos_zonas(tc.MINUTO_ZONA + salto)
        motor.primitivas_extra = predicados
        # los acumuladores de A-44 responden NO en sintetico, como en test_cableado (RN-020 sigue
        # siendo hueco con tope=None); `racha_perdidas` es el REAL del cableado
        motor.acumuladores_extra = acumuladores
        resultados.append(
            motor.correr_dia(
                DiaDeMercado(dia, tc.HUSO, tc.SESIONES, DatosMercado(tc._h4_alcista()))
            )
        )
    assert motor.racha is not None
    for k, (dia, r) in enumerate(zip(DIAS, resultados, strict=True), start=1):
        traza = r.sesiones["07-11"]
        broker = motor.brokers[dia.isoformat()]
        assert len(r.operaciones) == 1, (k, dia)  # la primera orden se llena y pierde cada dia
        if k == 9 or k == 10:
            assert "RN-036" in traza.disparadas, (k, dia)
            assert ("detenido_por_racha", "hasta_el_dia_siguiente") in {
                (h, v) for _, _, h, v in traza.fijados
            }, (k, dia)
            assert any(b[1] == "accion:colocar_orden_limite" for b in traza.bloqueadas), (k, dia)
            assert "o2" not in broker.ordenes, (k, dia)
            assert motor.trazas_broker[dia.isoformat()].cancelados_fin_dia == 0, (k, dia)
        else:
            assert "RN-036" not in traza.disparadas, (k, dia)
            assert broker.ordenes["o2"].estado == CANCELADA, (k, dia)  # RN-035 al abrir la tarde
    assert motor.racha.racha == 10
    assert "RACHA DE PERDIDAS (RN-036, A-51): 10 seguidas" in cableado.informe_simulacion(motor)
    assert not any(
        p.startswith("acumulador:racha")
        for r in resultados
        for _, p in r.sesiones["07-11"].no_implementadas
    )


def test_con_la_cuenta_diaria_la_racha_empieza_de_cero_cada_dia(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    motor = tc._motor(registro, vocabulario, tc._mercado(tc.RUTA_STOP))
    motor.cuenta_diaria = True
    motor.mercados = {d.isoformat(): _mercado_del_dia(d, tc.RUTA_STOP) for d in DIAS[:2]}
    for dia in DIAS[:2]:
        salto = (dia - tc.DIA).days * 1440
        predicados, acumuladores = tc._sinteticas(tc.MINUTO_ZONA + salto)
        motor.primitivas_extra = predicados
        motor.acumuladores_extra = acumuladores
        motor.correr_dia(DiaDeMercado(dia, tc.HUSO, tc.SESIONES, DatosMercado(tc._h4_alcista())))
    assert motor.racha is not None and motor.racha.racha == 1
