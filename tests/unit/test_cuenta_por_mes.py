"""Una cuenta por mes (ADR-0092 §8 y su NOTA; `trabajo/cuenta-por-mes`, D6 del encargo), todo
SINTETICO sobre el dia de 2030 de `test_cableado.py` desplazado a otros dias: ninguna fecha real y
ninguna corrida del arnes.

Lo que empieza de nuevo al cambiar de mes: la cuenta, desde el capital del perfil, el seguidor del
tope del trader y el primero en tocar un limite. La racha de RN-036 queda PENDIENTE de la PARADA
condicional de CUENTA-POR-MES.md (punto 1): hasta la respuesta, sigue. Dentro de un mes, y con
`--diagnostico-cuenta-diaria`, la salida es la de `main` (8aeed0b), congelada en
`tests/golden/cuenta_por_mes/` por `docs/validation/anexos/CUENTA-POR-MES/generar_goldens.py` en
un clon de `main`.

Rompen en `main` por lo que miden: `test_el_segundo_mes_vuelve_a_operar_desde_el_capital` (en
`main` febrero sigue SUSPENDIDO y no coloca), `test_el_seguidor_del_tope_y_el_primer_toque_...`
(en `main` el seguidor corta con el saldo de enero y el primer toque sigue siendo el de enero) y
`test_el_visor_ve_el_saldo_del_mes_nuevo_desde_el_capital`. Los dos goldens pasan en `main`."""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import Any
from zoneinfo import ZoneInfo

import pytest

from botsito.config.registro import Registro, cargar_registro
from botsito.engine import cableado
from botsito.engine.cuenta import EstadoCuenta
from botsito.engine.tope_trader import tope_del_registro
from botsito.spec.modelo import cargar_vocabulario
from tests.unit import escenarios_cuenta_por_mes as esc
from tests.unit import test_cableado as tc

GOLDEN = tc.RAIZ / "tests" / "golden" / "cuenta_por_mes"
ENE, FEB = esc.ENE_1.isoformat(), esc.FEB_1.isoformat()


@pytest.fixture(scope="module")
def registro() -> Registro:
    return cargar_registro(tc.RAIZ / "knowledge" / "spec" / "parametros.yaml")


@pytest.fixture(scope="module")
def vocabulario() -> dict[str, dict[str, Any]]:
    return cargar_vocabulario(tc.SPEC)


def _solo_febrero(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> cableado.MotorCableado:
    """El dia de febrero corrido SOLO, desde el capital: lo que tiene que dar el mes nuevo."""
    plan = ((esc.FEB_1, tc.RUTA_STOP),)
    motor = esc.motor_de(registro, vocabulario, plan)
    esc.correr(motor, plan)
    return motor


def _ms_del_dia(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, UTC).date().isoformat()


# ------------------------------------------------------------------------- D6 (1) y D3


def test_el_segundo_mes_vuelve_a_operar_desde_el_capital(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    """Enero: el salto de 2.000 puntos suspende la cuenta por la perdida total (como el test del
    hueco de test_cableado). Febrero: cuenta nueva desde el capital, el bot vuelve a colocar con el
    lote del capital y su dia da lo mismo que corrido solo. En `main`, febrero sigue SUSPENDIDO,
    RN-031 prohibe y no hay ninguna operacion."""
    motor = esc.motor_de(registro, vocabulario, esc.DOS_MESES)
    r_ene, r_feb = esc.correr(motor, esc.DOS_MESES)
    capital = motor.reglas_fase.capital_inicial
    assert len(r_ene.operaciones) == 1
    saldo_ene = motor.trazas_broker[ENE].saldo_fin
    assert saldo_ene is not None and saldo_ene < capital * Decimal("0.9")
    # febrero opera, con el lote del riesgo del capital (0,5 % de 100.000 sobre 16 puntos)
    assert len(r_feb.operaciones) == 1
    assert motor.trazas_broker[FEB].margen_al_colocar["o1"][3] == Decimal("31.25")
    solo = _solo_febrero(registro, vocabulario)
    assert motor.trazas_broker[FEB].saldo_fin == solo.trazas_broker[FEB].saldo_fin
    assert motor.trazas_broker[FEB].eventos == solo.trazas_broker[FEB].eventos
    assert motor.veredicto()[0] is EstadoCuenta.EN_CURSO
    assert [d for d, *_ in cableado.curva_de_equity(motor)] == [FEB]
    # D3: la cuenta de enero, cerrada y conservada para la salida
    [enero] = motor.cuentas_cerradas
    assert enero.mes == "2030-01" and enero.estado is EstadoCuenta.SUSPENDIDA
    assert "perdida" in enero.motivo and enero.instante is not None
    assert enero.saldo == saldo_ene and enero.dias_de_trading == 1
    assert [d for d, *_ in enero.curva] == [ENE]
    assert enero.primero_en_tocar is not None and _ms_del_dia(enero.primero_en_tocar[2]) == ENE


# ------------------------------------------------------------------------------ D6 (2)


def test_el_seguidor_del_tope_y_el_primer_toque_empiezan_de_cero_en_el_mes_nuevo(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    """Con el tope del trader del registro (A-44 RESUELTA) y el hueco los dos meses: en febrero
    el seguidor nace con el capital y no corta nada en su primer dia, y el primer toque de la cuenta
    de febrero es de febrero. En `main` el seguidor corta el dia y la semana al abrir febrero con
    el saldo de enero, y el primer toque se queda en enero (febrero ni siquiera coloca)."""
    plan = ((esc.ENE_1, tc.RUTA_HUECO), (esc.FEB_1, tc.RUTA_HUECO))
    motor = esc.motor_de(registro, vocabulario, plan)
    motor.tope = tope_del_registro(registro, ZoneInfo("Europe/Prague"))
    esc.correr(motor, plan)
    capital = motor.reglas_fase.capital_inicial
    assert motor.seguidor is not None
    assert motor.seguidor.cortes == []
    assert motor.seguidor.saldo_corte_dia == capital
    assert motor.seguidor.saldo_corte_semana == capital
    assert motor.primero_en_tocar is not None and _ms_del_dia(motor.primero_en_tocar[2]) == FEB
    [enero] = motor.cuentas_cerradas
    assert enero.primero_en_tocar is not None and _ms_del_dia(enero.primero_en_tocar[2]) == ENE


@pytest.mark.xfail(
    strict=True,
    reason="PARADA condicional 1 de CUENTA-POR-MES.md: la racha de RN-036 no se reinicia al "
    "cambiar de mes hasta que el consultor responda (la spec la describe en todos los dias)",
)
def test_la_racha_empieza_de_cero_en_el_mes_nuevo(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    """D1 tal como lo escribio el consultor: una perdida en enero y otra en febrero dan una racha
    de 1 en febrero. Hoy da 2 (ver el test siguiente)."""
    plan = ((esc.ENE_1, tc.RUTA_STOP), (esc.FEB_1, tc.RUTA_STOP))
    motor = esc.motor_de(registro, vocabulario, plan)
    esc.correr(motor, plan)
    assert motor.racha is not None and motor.racha.racha == 1


def test_hasta_la_respuesta_la_racha_sigue_de_un_mes_a_otro(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    plan = ((esc.ENE_1, tc.RUTA_STOP), (esc.FEB_1, tc.RUTA_STOP))
    motor = esc.motor_de(registro, vocabulario, plan)
    esc.correr(motor, plan)
    assert motor.racha is not None and motor.racha.racha == 2
    assert len(motor.cuentas_cerradas) == 1  # la cuenta si empezo de nuevo


# ------------------------------------------------------------------------ D6 (3) y (4)


@pytest.mark.parametrize("nombre", sorted(esc.ESCENARIOS_MAIN))
def test_la_salida_es_la_de_main(
    registro: Registro, vocabulario: dict[str, dict[str, Any]], nombre: str
) -> None:
    """Dos dias del mismo mes (la cuenta se arrastra del 15 al 16) y la diaria con dos meses: el
    informe ENTERO es byte a byte el de `main`."""
    plan, diaria = esc.ESCENARIOS_MAIN[nombre]
    de_main = (GOLDEN / f"main-{nombre}.txt").read_text(encoding="utf-8")
    assert esc.informe(registro, vocabulario, plan, diaria) == de_main


def test_con_la_diaria_no_se_conserva_ninguna_cuenta(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    plan, _ = esc.ESCENARIOS_MAIN["diaria-dos-meses"]
    motor = esc.motor_de(registro, vocabulario, plan, cuenta_diaria=True)
    esc.correr(motor, plan)
    assert motor.cuentas_cerradas == []
    # y su primer toque sigue siendo de toda la corrida: el de enero
    assert motor.primero_en_tocar is not None and _ms_del_dia(motor.primero_en_tocar[2]) == ENE


def test_dentro_de_un_mes_no_se_cierra_ninguna_cuenta(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    plan, _ = esc.ESCENARIOS_MAIN["dentro-de-un-mes"]
    motor = esc.motor_de(registro, vocabulario, plan)
    esc.correr(motor, plan)
    assert motor.cuentas_cerradas == []
    assert motor.cuenta is not None and motor.cuenta.dias_de_trading == 2


def test_el_volcado_de_los_escenarios(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    """Saca por la salida estandar (con `-s`) todas las salidas de los escenarios, delimitadas: en
    un clon de `main` es lo que genera los goldens (`escenarios_cuenta_por_mes.volcado`). Aqui solo
    comprueba que el volcado se puede partir."""
    texto = esc.volcado(registro, vocabulario)
    print(texto)
    assert texto.count(esc.INICIO_VOLCADO) == texto.count(esc.FIN_VOLCADO) == 7


# ------------------------------------------------------------------------------ D6 (6)


def test_el_visor_ve_el_saldo_del_mes_nuevo_desde_el_capital(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    """El visor con --simular corre `correr_dia` dia a dia y lee el saldo por
    `detalle_para_visor` (TrazaBroker.saldo_fin): el primer dia de febrero parte del capital. En
    `main` lleva el saldo suspendido de enero."""
    motor = esc.motor_de(registro, vocabulario, esc.DOS_MESES)
    esc.correr(motor, esc.DOS_MESES)
    ene = cableado.detalle_para_visor(motor, ENE)
    feb = cableado.detalle_para_visor(motor, FEB)
    solo = cableado.detalle_para_visor(_solo_febrero(registro, vocabulario), FEB)
    assert ene is not None and feb is not None and solo is not None
    assert feb.saldo_fin == solo.saldo_fin and feb.equity_fin == solo.equity_fin
    assert feb.saldo_fin != ene.saldo_fin
    assert len(feb.posiciones) == 1


def test_la_cuenta_cambia_por_el_mes_de_la_clave_y_no_por_los_dias_que_pasan(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    """Del 15 al 16 de enero no cambia nada; del 16 de enero al 12 de febrero, si; del 12 al 13
    de febrero, no: el mes es el AAAA-MM de la clave del dia corrido."""
    plan = (
        (esc.ENE_1, tc.RUTA_STOP),
        (esc.ENE_2, tc.RUTA_STOP),
        (esc.FEB_1, tc.RUTA_STOP),
        (esc.FEB_2, tc.RUTA_STOP),
    )
    motor = esc.motor_de(registro, vocabulario, plan)
    esc.correr(motor, plan)
    [enero] = motor.cuentas_cerradas
    assert enero.mes == "2030-01" and enero.dias_de_trading == 2
    assert [d for d, *_ in enero.curva] == [ENE, esc.ENE_2.isoformat()]
    assert motor.cuenta is not None and motor.cuenta.dias_de_trading == 2
    assert [d for d, *_ in cableado.curva_de_equity(motor)] == [FEB, esc.FEB_2.isoformat()]
