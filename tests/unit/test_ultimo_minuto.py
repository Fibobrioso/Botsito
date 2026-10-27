"""El ultimo minuto antes de las 11 y de las 3 (sesion 5, S-22; trabajo/activar-sesion-05-motor,
punto 6): RN-035 retira la orden sin llenar en [fin - cierre_h4_antelacion, fin) de cada vela H4 de
la ventana (ev-v16-002248-08e9600f, «un minuto antes»), y RN-037 (gate) no deja colocar ni
recolocar ninguna orden en ese minuto (ev-v16-002323-515b9da4); el evento del propio limite ya es
de la sesion siguiente y en el si se coloca. Lo que se llena antes del ultimo minuto lo cierra
RN-002 en el evento siguiente (ADR-0060 §5). Por el cableado real y la spec real, con el registro
vigente; todo sintetico, el dia es de 2030. Falla con el codigo de main: alli la orden se llenaba
en el ultimo minuto (el HUECO de test_rn035_ventana_fin.py) y se colocaba en el."""

from __future__ import annotations

from typing import Any

import pytest

from botsito.config.registro import Registro, cargar_registro
from botsito.domain.ticks import MS_POR_MINUTO
from botsito.engine.broker import CANCELADA, MANUAL, PETICION_CANCELAR, PETICION_COLOCAR
from botsito.spec.modelo import cargar_vocabulario
from tests.unit import test_cableado as tc
from tests.unit import test_rn035_ventana_fin as t35

ULTIMOS = [
    (tc.MINUTO_ZONA, tc.FIN_H4, "07-11"),  # la manana: el fin de la primera H4, las 11
    (t35.ZONA_TARDE, tc.MINUTO_FIN, "11-15"),  # la tarde: ventana_fin, las 3
]


@pytest.fixture(scope="module")
def registro() -> Registro:
    return cargar_registro(tc.RAIZ / "knowledge" / "spec" / "parametros.yaml")


@pytest.fixture(scope="module")
def vocabulario() -> dict[str, dict[str, Any]]:
    return cargar_vocabulario(tc.SPEC)


@pytest.mark.parametrize(("zona", "fin", "sesion"), ULTIMOS)
def test_rn035_retira_la_orden_sin_llenar_en_el_ultimo_minuto(
    registro: Registro, vocabulario: dict[str, dict[str, Any]], zona: int, fin: int, sesion: str
) -> None:
    """La orden pendiente se retira en el evento fin - 1 (cierre_h4_antelacion = 1), antes de los
    ticks del ultimo minuto: aunque el BID baje en ese minuto, no se llena. En main se llenaba y
    la posicion vivia menos de un minuto (ADR-0060 §5)."""
    antelacion = registro.minutos("cierre_h4_antelacion")
    motor = t35._motor(registro, vocabulario, zona, {fin - 1: tc.ENTRADA - 10})
    r = motor.correr_dia(tc._dia())
    broker = motor.brokers[tc.DIA.isoformat()]
    o1 = broker.ordenes["o1"]
    assert o1.estado == CANCELADA
    assert o1.ultimo_cambio_ms == (fin - antelacion) * MS_POR_MINUTO - 1
    assert "RN-035" in r.sesiones[sesion].disparadas
    assert not r.operaciones and not broker.posiciones
    tb = motor.trazas_broker[tc.DIA.isoformat()]
    assert tb.cancelados_fin_dia == 0
    assert [(p.tipo, p.id) for p in tb.peticiones] == [
        (PETICION_COLOCAR, "o1"),
        (PETICION_CANCELAR, "o1"),
    ]


@pytest.mark.parametrize(("zona", "fin", "sesion"), ULTIMOS)
def test_rn037_no_deja_colocar_en_el_ultimo_minuto(
    registro: Registro, vocabulario: dict[str, dict[str, Any]], zona: int, fin: int, sesion: str
) -> None:
    """La zona aparece en el cierre fin - 1: RN-037 prohibe abrir_operacion y RN-015 no coloca
    (bloqueada con nombre); ninguna orden llega al broker. En main se colocaba."""
    del zona
    motor = t35._motor(registro, vocabulario, fin - 1, {})
    r = motor.correr_dia(tc._dia())
    traza = r.sesiones[sesion]
    assert "RN-037" in traza.disparadas
    assert (
        "RN-015",
        "accion:colocar_orden_limite",
        "prohibida:abrir_operacion",
    ) in traza.bloqueadas
    assert not motor.brokers[tc.DIA.isoformat()].ordenes
    assert not motor.trazas_broker[tc.DIA.isoformat()].peticiones


def _motor_con_zona_en(
    registro: Registro, vocabulario: dict[str, dict[str, Any]], instante: int
) -> Any:
    """Como `t35._motor`, pero con un `toca_colocar_orden_limite` SIN estado: SI en `instante`,
    cuantas veces se evalue. El sintetico de `test_cableado` se consume al evaluarse, y en la
    apertura de una sesion el interprete evalua el `cuando` de RN-011 una vez de mas para avisar
    de empates con RN-003 (ADR-0049 H3): con el de un solo uso, RN-011 ya no lo veia."""
    motor = t35._motor(registro, vocabulario, instante, {})

    def toca(args: Any, momento: Any, estado: Any) -> Any:
        from botsito.engine.interprete import Resultado, Tri

        if int(momento.instante) == instante:
            return Resultado(Tri.SI, {"Z": "zona:1"})
        return Resultado(Tri.NO)

    motor.primitivas_extra = {**motor.primitivas_extra, "toca_colocar_orden_limite": toca}
    return motor


def test_en_el_primer_cierre_de_la_sesion_de_las_11_se_puede_colocar(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    """El evento del limite (las 11) ya es de la sesion siguiente: RN-037 no dispara y la orden se
    coloca en ese mismo cierre."""
    motor = _motor_con_zona_en(registro, vocabulario, tc.FIN_H4)
    r = motor.correr_dia(tc._dia())
    o1 = motor.brokers[tc.DIA.isoformat()].ordenes["o1"]
    assert o1.colocada_ms == tc.FIN_H4 * MS_POR_MINUTO - 1
    tarde = r.sesiones["11-15"]
    assert "RN-011" in tarde.disparadas and "RN-015" in tarde.disparadas
    # RN-037 dispara cada dia a las 10:59 y a las 14:59 (la gate evalua SI), pero no bloqueo nada:
    # en el limite de las 11 su predicado da NO y la colocacion paso
    assert ("RN-015", "accion:colocar_orden_limite", "prohibida:abrir_operacion") not in (
        tarde.bloqueadas | r.sesiones["07-11"].bloqueadas
    )
    assert (tc.FIN_H4, "RN-011", "orden_dimensionada", "zona:1") in tarde.fijados


def test_lo_que_se_llena_antes_del_ultimo_minuto_lo_cierra_rn002_en_el_evento_siguiente(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    """ADR-0060 §5 sigue entero para la posicion: una orden que se llena en el minuto anterior al
    ultimo (fin - 2) abre una posicion que RN-002 cierra en el evento siguiente, fin - 1, el mismo
    en que RN-035 ya no encuentra nada que retirar."""
    fin = tc.FIN_H4
    motor = t35._motor(registro, vocabulario, tc.MINUTO_ZONA, {fin - 2: tc.ENTRADA - 10})
    r = motor.correr_dia(tc._dia())
    broker = motor.brokers[tc.DIA.isoformat()]
    assert len(r.operaciones) == 1 and len(broker.posiciones) == 1
    p = next(iter(broker.posiciones.values()))
    assert (fin - 2) * MS_POR_MINUTO <= p.abierta_ms < (fin - 1) * MS_POR_MINUTO
    assert not p.abierta and p.cerrada_ms == (fin - 1) * MS_POR_MINUTO - 1
    assert p.motivo_cierre == MANUAL
    assert "RN-002" in r.sesiones["07-11"].disparadas
    assert "RN-035" not in r.sesiones["07-11"].disparadas  # ya no habia orden pendiente


def test_la_forma_y_el_vocabulario(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    """RN-035 lee la rejilla y la antelacion por su nombre, en una tercera rama; RN-037 es una
    gate sobre abrir_operacion con el mismo predicado; el predicado es de reloj, con sus dos
    argumentos, y no vale en el limite."""
    from botsito.spec.modelo import _invocaciones, cargar_reglas

    reglas = {r.id: r for r in cargar_reglas(tc.SPEC)}
    rn035, rn037 = reglas["RN-035"], reglas["RN-037"]
    assert {"anclaje_h4", "cierre_h4_antelacion"} <= set(rn035.parametros)
    assert rn037.clase == "gate" and rn037.vigente
    assert isinstance(rn035.forma, dict) and isinstance(rn037.forma, dict)
    assert rn037.forma["entonces"] == {"prohibe": ["abrir_operacion"]}
    for forma in (rn035.forma, rn037.forma):
        llamadas = dict(_invocaciones(forma["cuando"]))
        assert llamadas["en_el_ultimo_tramo_h4"] == {
            "anclaje": "anclaje_h4",
            "antelacion": "cierre_h4_antelacion",
        }
    declarado = vocabulario["predicados"]["en_el_ultimo_tramo_h4"]
    assert declarado["fuente"] == "reloj" and declarado["argumentos"] == ["anclaje", "antelacion"]
    assert declarado["cita"] == "ev-v16-002248-08e9600f"
    assert rn035.cita == "fb-2026-10-23-sesion-05-1526aa39"
    assert rn037.cita == "ev-v16-002323-515b9da4"
    assert registro.minutos("cierre_h4_antelacion") == 1
