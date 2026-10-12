"""RN-035, tramo ventana_fin (sesion 4, S-5; trabajo/activar-sesion-04-motor, decision 5): la orden
que sigue pendiente al llegar ventana_fin la retira RN-035 segun orden_pendiente_al_abrir_sesion, y
la cancelacion del cableado al terminar el dia (ADR-0053 §6) ya no encuentra nada. Y el hueco que NO
se arregla aqui, CONGELADO: una orden que se llena en el ultimo minuto de la H4 -[fin-1, fin)-,
despues de que RN-002 ya cerrara en el evento fin-1, se cierra en el evento del propio limite
(ADR-0060 §5), igual a las 11 que a ventana_fin. Todo sintetico; el dia es de 2030."""

from __future__ import annotations

from typing import Any

import pytest

from botsito.config.registro import Registro, cargar_registro
from botsito.domain.ticks import MS_POR_MINUTO
from botsito.engine.broker import CANCELADA, MANUAL, PETICION_CANCELAR, PETICION_COLOCAR
from botsito.spec.modelo import cargar_vocabulario
from tests.unit import test_cableado as tc

ZONA_TARDE = tc.MINUTO_ZONA + 240  # 12:00 UTC, dentro de la sesion 11-15 (13:00 en Madrid)


@pytest.fixture(scope="module")
def registro() -> Registro:
    return cargar_registro(tc.RAIZ / "knowledge" / "spec" / "parametros.yaml")


@pytest.fixture(scope="module")
def vocabulario() -> dict[str, dict[str, Any]]:
    return cargar_vocabulario(tc.SPEC)


def _motor(registro: Registro, vocabulario: dict[str, dict[str, Any]], zona: int, ruta: Any) -> Any:
    motor = tc._motor(registro, vocabulario, tc._mercado(ruta))
    predicados, acumuladores = tc._sinteticas(zona)
    motor.primitivas_extra = predicados
    motor.acumuladores_extra = acumuladores
    return motor


def test_rn035_retira_la_pendiente_a_ventana_fin_y_el_cableado_no_encuentra_nada(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    """La orden de la tarde no se llena (el precio no baja). A ventana_fin la retira RN-035 con su
    motivo en la traza del motor (la regla en `disparadas`), y la red de seguridad del cableado
    no cancela nada. Falla con el codigo de `main`: alli RN-035 solo dispara al abrir una sesion y
    la orden la cancela el cableado sin regla."""
    assert registro.opcion("orden_pendiente_al_abrir_sesion") == "se_retira"
    motor = _motor(registro, vocabulario, ZONA_TARDE, {})
    r = motor.correr_dia(tc._dia())
    o1 = motor.brokers[tc.DIA.isoformat()].ordenes["o1"]
    assert o1.colocada_ms == ZONA_TARDE * MS_POR_MINUTO - 1
    assert o1.estado == CANCELADA and o1.ultimo_cambio_ms == tc.MINUTO_FIN * MS_POR_MINUTO - 1
    assert "RN-035" in r.sesiones["11-15"].disparadas
    assert "RN-035" not in r.sesiones["07-11"].disparadas  # la manana no tuvo orden
    tb = motor.trazas_broker[tc.DIA.isoformat()]
    assert tb.cancelados_fin_dia == 0  # ADR-0053 §6 queda como red de seguridad: no encontro nada
    assert [(p.tipo, p.id) for p in tb.peticiones] == [
        (PETICION_COLOCAR, "o1"),
        (PETICION_CANCELAR, "o1"),
    ]
    assert not r.operaciones


@pytest.mark.parametrize(
    ("zona", "fin"),
    [
        (tc.MINUTO_ZONA, tc.FIN_H4),  # la manana: el fin de la primera H4, las 11 del trader
        (ZONA_TARDE, tc.MINUTO_FIN),  # la tarde: ventana_fin, las 3
    ],
)
def test_hueco_la_orden_que_se_llena_en_el_ultimo_minuto_se_cierra_en_el_limite(
    registro: Registro, vocabulario: dict[str, dict[str, Any]], zona: int, fin: int
) -> None:
    """CONGELA lo que pasa hoy, no lo arregla (decision 5 del encargo; pregunta para la sesion 5):
    RN-002 cierra lo abierto en el evento fin-1 (`vence_vela_h4` con cierre_h4_antelacion), pero
    una orden pendiente puede llenarse DESPUES, dentro del ultimo minuto [fin-1, fin); entonces se
    cierra en el evento del propio limite (ADR-0060 §5), y la posicion vive menos de un minuto.
    RN-035 no la ve: al llegar el limite ya no esta pendiente."""
    # el BID baja 10 puntos en el ultimo minuto: el ASK (BID + spread) queda por debajo de la
    # entrada y la limite se llena en el tick de los 40 s; el stop (16 puntos) no se toca
    motor = _motor(registro, vocabulario, zona, {fin - 1: tc.ENTRADA - 10})
    r = motor.correr_dia(tc._dia())
    broker = motor.brokers[tc.DIA.isoformat()]
    assert len(r.operaciones) == 1 and len(broker.posiciones) == 1
    p = next(iter(broker.posiciones.values()))
    assert (fin - 1) * MS_POR_MINUTO <= p.abierta_ms < fin * MS_POR_MINUTO
    assert not p.abierta and p.cerrada_ms == fin * MS_POR_MINUTO - 1
    assert p.motivo_cierre == MANUAL  # RN-002, cerrar_a_mercado
    assert "RN-002" in r.sesiones["11-15"].disparadas  # el evento del limite es de la sesion 11-15
    assert "RN-035" not in r.sesiones["11-15"].disparadas
    assert motor.trazas_broker[tc.DIA.isoformat()].cancelados_fin_dia == 0
