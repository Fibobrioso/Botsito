"""Escenarios SINTETICOS de `trabajo/cuenta-por-mes` (ADR-0092 §8 y su NOTA): el dia sintetico de
`test_cableado.py` desplazado a otros dias de 2030, de uno o de dos meses. Solo usa lo que ya existe
en `main` (8aeed0b), para que los goldens de `main` se generen con este MISMO codigo copiado a su
clon (`docs/validation/anexos/CUENTA-POR-MES/generar_goldens.py`). Ninguna fecha real."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import date
from typing import Any

from botsito.cases.criterio_fidelidad import Operacion, cargar_criterio
from botsito.config.registro import Registro
from botsito.engine import cableado
from botsito.engine.motor import DatosMercado, DiaDeMercado, ResultadoDia
from tests.unit import test_cableado as tc
from tests.unit.test_racha_perdidas import _mercado_del_dia

ENE_1 = tc.DIA  # 2030-01-15, martes, invierno
ENE_2 = date(2030, 1, 16)
FEB_1 = date(2030, 2, 12)  # martes, cuatro semanas despues; sigue siendo invierno en Madrid
FEB_2 = date(2030, 2, 13)

Plan = Sequence[tuple[date, dict[int, int]]]  # dia y ruta del BID (la de test_cableado)

# los escenarios con golden de `main` (tests/golden/cuenta_por_mes/): nombre -> (dias y rutas,
# cuenta_diaria)
ESCENARIOS_MAIN: dict[str, tuple[Plan, bool]] = {
    # D6 (3): dos dias del MISMO mes; la cuenta se arrastra del 15 al 16, como en main
    "dentro-de-un-mes": (((ENE_1, tc.RUTA_STOP), (ENE_2, tc.RUTA_STOP)), False),
    # D6 (4): la diaria con dos meses; reinicia cada dia, como en main
    "diaria-dos-meses": (((ENE_1, tc.RUTA_HUECO), (FEB_1, tc.RUTA_STOP)), True),
}
# el escenario que CAMBIA a proposito (D6 (1) y (5)): su salida de main va al anexo, no a un golden
DOS_MESES: Plan = ((ENE_1, tc.RUTA_HUECO), (FEB_1, tc.RUTA_STOP))
RUTAS_METODO = {"hueco": tc.RUTA_HUECO, "stop": tc.RUTA_STOP, "viva": tc.RUTA_VIVA}


def motor_de(
    registro: Registro,
    vocabulario: dict[str, dict[str, Any]],
    plan: Plan,
    *,
    cuenta_diaria: bool = False,
) -> cableado.MotorCableado:
    motor = tc._motor(registro, vocabulario, tc._mercado(tc.RUTA_STOP))
    motor.mercados = {d.isoformat(): _mercado_del_dia(d, ruta) for d, ruta in plan}
    motor.cuenta_diaria = cuenta_diaria
    return motor


def correr(motor: cableado.MotorCableado, plan: Plan) -> list[ResultadoDia]:
    """Corre los dias del plan en orden, con la estrategia sintetica de test_cableado en el minuto
    de la zona de cada dia (como el test de nueve dias de test_racha_perdidas)."""
    resultados = []
    for dia, _ in plan:
        salto = (dia - tc.DIA).days * 1440
        predicados, acumuladores = tc._sinteticas(tc.MINUTO_ZONA + salto)
        motor.primitivas_extra = predicados
        motor.acumuladores_extra = acumuladores
        resultados.append(
            motor.correr_dia(
                DiaDeMercado(dia, tc.HUSO, tc.SESIONES, DatosMercado(tc._h4_alcista()))
            )
        )
    return resultados


def informe(
    registro: Registro, vocabulario: dict[str, dict[str, Any]], plan: Plan, cuenta_diaria: bool
) -> str:
    motor = motor_de(registro, vocabulario, plan, cuenta_diaria=cuenta_diaria)
    correr(motor, plan)
    return cableado.informe_simulacion(motor)


def con_criterio(motor: cableado.MotorCableado) -> cableado.MotorCableado:
    """El criterio REAL de ADR-0092 y, por cada posicion del bot, una operacion del trader con la
    misma entrada, el mismo stop y el mismo llenado (como test_metodo_adr0092): asi la seccion saca
    la cascada y la rentabilidad, a) a f), y no solo «sin el criterio»."""
    motor.criterio = cargar_criterio(tc.RAIZ)
    filas = cableado.posiciones_del_bot(motor)
    ordenes = cableado.ordenes_para_la_cascada(motor)
    motor.operaciones_trader = tuple(
        Operacion(p.dia, p.sesion, p.lado, p.llenada, o.entrada, o.stop)
        for p, o in zip(filas, ordenes, strict=False)
    )
    return motor


def seccion_metodo(texto: str) -> str:
    """La seccion de ADR-0092 del informe: desde su cabecera hasta el final."""
    return texto[texto.index("\n" + cableado.CABECERA_METODO) :]


def seccion_de_un_dia(
    registro: Registro, vocabulario: dict[str, dict[str, Any]], ruta: Mapping[int, int]
) -> str:
    motor = tc._motor(registro, vocabulario, tc._mercado(ruta))
    motor.correr_dia(tc._dia())
    return seccion_metodo(cableado.informe_simulacion(con_criterio(motor)))


def informe_dos_meses_con_criterio(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> str:
    motor = motor_de(registro, vocabulario, DOS_MESES)
    correr(motor, DOS_MESES)
    return cableado.informe_simulacion(con_criterio(motor))


INICIO_VOLCADO = "<<<VOLCADO "
FIN_VOLCADO = "<<<FIN>>>"


def volcado(registro: Registro, vocabulario: dict[str, dict[str, Any]]) -> str:
    """Todas las salidas de los escenarios, cada una entre `<<<VOLCADO ruta>>>` y `<<<FIN>>>`,
    para que `test_cuenta_por_mes.py::test_el_volcado_de_los_escenarios`, corrido con `-s` en un
    clon de `main`, las saque por la salida estandar y
    `docs/validation/anexos/CUENTA-POR-MES/partir_volcado.py` las parta en ficheros: los goldens
    (`cuenta_por_mes/`, `metodo_adr0092/`) y la salida de `main` del escenario que cambia a
    proposito (`anexo/`). Asi el codigo que genera es el mismo que el que compara."""
    salidas: list[tuple[str, str]] = []
    for nombre, (plan, diaria) in sorted(ESCENARIOS_MAIN.items()):
        salidas.append(
            (f"cuenta_por_mes/main-{nombre}.txt", informe(registro, vocabulario, plan, diaria))
        )
    for nombre, ruta in sorted(RUTAS_METODO.items()):
        salidas.append(
            (f"metodo_adr0092/main-{nombre}.txt", seccion_de_un_dia(registro, vocabulario, ruta))
        )
    salidas.append(("anexo/dos-meses.txt", informe(registro, vocabulario, DOS_MESES, False)))
    salidas.append(
        ("anexo/dos-meses-con-criterio.txt", informe_dos_meses_con_criterio(registro, vocabulario))
    )
    return "".join(f"{INICIO_VOLCADO}{r}>>>\n{t}{FIN_VOLCADO}\n" for r, t in salidas)
