"""Una cuenta por mes (ADR-0092 §8 y su NOTA; `trabajo/cuenta-por-mes`, D6 del encargo), todo
SINTETICO sobre el dia de 2030 de `test_cableado.py` desplazado a otros dias: ninguna fecha real y
ninguna corrida del arnes.

Lo que empieza de nuevo al cambiar de mes: la cuenta, desde el capital del perfil, el seguidor del
tope del trader, la racha de RN-036 (respuesta del consultor a la PARADA de CUENTA-POR-MES.md,
punto 1: vive lo que vive la cuenta) y el primero en tocar un limite. Dentro de un mes, y con
`--diagnostico-cuenta-diaria`, la salida es la de `main` (8aeed0b), congelada en
`tests/golden/cuenta_por_mes/` (y la seccion de ADR-0092 con un mes, en
`tests/golden/metodo_adr0092/`) por `test_el_volcado_de_los_escenarios`, corrido con `-s` en un
clon de `main`, y `docs/validation/anexos/CUENTA-POR-MES/partir_volcado.py`.

Este fichero solo importa lo que ya existe en `main`, para poder correrlo alli (las piezas puras
nuevas de `criterio_fidelidad.py`, en `test_cuenta_por_mes_metodo.py`). Rompen en `main` por lo
que miden: `test_el_segundo_mes_vuelve_a_operar_desde_el_capital` (en `main` febrero sigue
SUSPENDIDO y no coloca), `test_el_seguidor_del_tope_y_el_primer_toque_...` (en `main` el seguidor
corta con el saldo de enero y el primer toque sigue siendo el de enero),
`test_el_visor_ve_el_saldo_del_mes_nuevo_desde_el_capital`,
`test_la_cuenta_cambia_por_el_mes_de_la_clave_...`, `test_la_racha_empieza_de_cero_en_el_mes_nuevo`
(en `main` da 2) y los dos de la salida con varios meses. Los
goldens pasan en `main`."""

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


def test_la_racha_empieza_de_cero_en_el_mes_nuevo(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    """Respuesta del consultor a la PARADA, punto 1.e: una perdida en enero y otra en febrero dan
    una racha de 1 en febrero, y la de enero se queda en su cuenta cerrada. En `main` da 2."""
    plan = ((esc.ENE_1, tc.RUTA_STOP), (esc.FEB_1, tc.RUTA_STOP))
    motor = esc.motor_de(registro, vocabulario, plan)
    esc.correr(motor, plan)
    assert motor.racha is not None and motor.racha.racha == 1
    [enero] = motor.cuentas_cerradas
    assert enero.racha.startswith("1 seguidas")


def test_dentro_de_una_cuenta_la_racha_sigue_de_un_dia_a_otro(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    """Dentro de un mes la racha hace lo de `main`: dos perdidas en dos dias de enero dan 2 (pasa
    tambien en `main`)."""
    plan = ((esc.ENE_1, tc.RUTA_STOP), (esc.ENE_2, tc.RUTA_STOP))
    motor = esc.motor_de(registro, vocabulario, plan)
    esc.correr(motor, plan)
    assert motor.racha is not None and motor.racha.racha == 2


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
    # primero lo que tambien se mide en `main` (alli la curva lleva los cuatro dias y la cuenta
    # cuatro dias de trading)
    assert [d for d, *_ in cableado.curva_de_equity(motor)] == [FEB, esc.FEB_2.isoformat()]
    assert motor.cuenta is not None and motor.cuenta.dias_de_trading == 2
    [enero] = motor.cuentas_cerradas
    assert enero.mes == "2030-01" and enero.dias_de_trading == 2
    assert [d for d, *_ in enero.curva] == [ENE, esc.ENE_2.isoformat()]


# ------------------------------------------------------------------- D6 (5): la salida, D4 y D5

GOLDEN_METODO = tc.RAIZ / "tests" / "golden" / "metodo_adr0092"


def test_con_varios_meses_la_salida_lleva_un_bloque_por_cuenta(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    """D4: la cabecera dice cuantas cuentas y remite el primer toque a cada mes; el
    veredicto, el saldo, los dias, el primer toque, la racha al cierre y la curva van por mes, en
    orden; el veredicto del tramo entero ya no sale. En `main` sale un solo veredicto, SUSPENDIDA,
    con febrero dentro de la curva de enero (`anexos/CUENTA-POR-MES/main/dos-meses.txt`)."""
    texto = esc.informe(registro, vocabulario, esc.DOS_MESES, False)
    lineas = texto.splitlines()
    assert "CUENTA: UNA POR MES (ADR-0092 §8): 2 cuentas" in lineas
    # la racha va con la cuenta (respuesta a la PARADA, punto 1): la cabecera remite a cada mes
    assert "RACHA DE PERDIDAS (RN-036, A-51): por cuenta: ver cada mes" in lineas
    assert "PRIMERO EN TOCAR UN LIMITE: por cuenta: ver cada mes" in lineas
    assert "### Veredicto de la cuenta sobre el tramo" not in lineas
    i_ene, i_feb = lineas.index("### Cuenta de 2030-01"), lineas.index("### Cuenta de 2030-02")
    assert i_ene < i_feb
    enero, febrero = (
        lineas[i_ene:i_feb],
        lineas[
            i_feb : lineas.index("### Eventos del broker (dia | instante UTC | tipo | id | fuente)")
        ],
    )
    assert "estado: SUSPENDIDA" in enero and "estado: EN_CURSO" in febrero
    assert any(x.startswith("PRIMERO EN TOCAR UN LIMITE: firma") for x in enero)
    assert "PRIMERO EN TOCAR UN LIMITE: ninguno" in febrero
    assert "dias de trading: 1" in enero and "dias de trading: 1" in febrero
    assert any(x.startswith("RACHA DE PERDIDAS (RN-036, A-51) al cerrar el mes: ") for x in enero)
    # la curva de cada cuenta solo nombra los dias de su mes; la de febrero empieza en el capital
    assert [x for x in enero if x.startswith("2030-")] == [
        x for x in enero if x.startswith(f"{ENE} |")
    ]
    [fila_feb] = [x for x in febrero if x.startswith(f"{FEB} |")]
    assert fila_feb.split(" | ")[1] == "100000"


def test_con_un_mes_la_seccion_de_adr0092_es_la_de_main(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    """D5: la guardia nueva, con el criterio REAL en el motor (a) a f) salen enteros) y el dia
    sintetico con las tres rutas: la seccion es byte a byte la de `main`."""
    for nombre, ruta in sorted(esc.RUTAS_METODO.items()):
        de_main = (GOLDEN_METODO / f"main-{nombre}.txt").read_text(encoding="utf-8")
        assert esc.seccion_de_un_dia(registro, vocabulario, ruta) == de_main, nombre


def test_con_varios_meses_d_y_e_son_por_cuenta_y_f_dice_cual(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    """D5: la cascada y la esperanza, sobre todas las operaciones; d) y e), la peor cuenta y su
    mes; f), si alguna cuenta entro en SUSPENDIDA y cual."""
    texto = esc.informe_dos_meses_con_criterio(registro, vocabulario)
    lineas = esc.seccion_metodo(texto).splitlines()
    assert "a) N (operaciones llenadas y cerradas): 2" in lineas
    d = next(x for x in lineas if x.startswith("d) "))
    e = next(x for x in lineas if x.startswith("e) "))
    f = next(x for x in lineas if x.startswith("f) "))
    assert ", por cuenta: " in d and d.endswith("la peor, la cuenta de 2030-01")
    assert ", por cuenta: " in e and e.endswith("la peor, la cuenta de 2030-01")
    assert f == "f) alguna cuenta entro en SUSPENDIDA: si (2030-01)"
    # la cascada, sobre las operaciones de los dos meses juntas
    total = next(x for x in lineas if x.startswith("total | "))
    assert total.split(" | ")[-1] == "2"
