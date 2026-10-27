"""RN-035, tramo ventana_fin (sesion 4, S-5; trabajo/activar-sesion-04-motor, decision 5): la orden
que sigue pendiente al llegar ventana_fin la retira RN-035 segun orden_pendiente_al_abrir_sesion, y
la cancelacion del cableado al terminar el dia (ADR-0053 §6) ya no encuentra nada. El hueco que
este fichero congelaba -una orden que se llenaba en el ultimo minuto de la H4- quedo cerrado el
2026-10-26 (sesion 5, S-22): RN-035 la retira un minuto antes (tests/unit/test_ultimo_minuto.py).
Todo sintetico; el dia es de 2030."""

from __future__ import annotations

from typing import Any

import pytest

from botsito.config.registro import Registro, cargar_registro
from botsito.domain.ticks import MS_POR_MINUTO
from botsito.engine.broker import CANCELADA, PETICION_CANCELAR, PETICION_COLOCAR
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
    """La orden de la tarde no se llena (el precio no baja). La retira RN-035 con su motivo en la
    traza del motor (la regla en `disparadas`), y la red de seguridad del cableado no cancela
    nada. CAMBIA DE SENTIDO A PROPOSITO el 2026-10-26 (sesion 5, S-22): la retirada ya no es a
    ventana_fin sino un minuto antes, en el ultimo tramo de la H4 (`cierre_h4_antelacion`); la
    rama de ventana_fin se queda como red y no encuentra nada."""
    assert registro.opcion("orden_pendiente_al_abrir_sesion") == "se_retira"
    antelacion = registro.minutos("cierre_h4_antelacion")
    motor = _motor(registro, vocabulario, ZONA_TARDE, {})
    r = motor.correr_dia(tc._dia())
    o1 = motor.brokers[tc.DIA.isoformat()].ordenes["o1"]
    assert o1.colocada_ms == ZONA_TARDE * MS_POR_MINUTO - 1
    assert o1.estado == CANCELADA
    assert o1.ultimo_cambio_ms == (tc.MINUTO_FIN - antelacion) * MS_POR_MINUTO - 1
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
    ("zona", "fin", "sesion"),
    [
        (tc.MINUTO_ZONA, tc.FIN_H4, "07-11"),  # la manana: el fin de la primera H4, las 11
        (ZONA_TARDE, tc.MINUTO_FIN, "11-15"),  # la tarde: ventana_fin, las 3
    ],
)
def test_hueco_la_orden_que_se_llena_en_el_ultimo_minuto_se_cierra_en_el_limite(
    registro: Registro, vocabulario: dict[str, dict[str, Any]], zona: int, fin: int, sesion: str
) -> None:
    """CAMBIA DE SENTIDO A PROPOSITO el 2026-10-26 (sesion 5, S-22; trabajo/activar-sesion-05-motor,
    punto 6): hasta entonces CONGELABA el hueco -una orden pendiente podia llenarse en el ultimo
    minuto [fin-1, fin), despues de que RN-002 cerrara en fin-1, y la posicion se cerraba en el
    evento del limite (ADR-0060 §5)-. Desde entonces RN-035 retira la orden sin llenar en el
    evento fin-1 («un minuto antes», ev-v16-002248-08e9600f) y no se llena aunque el BID baje en
    ese minuto, a las 11 y a las 3. El nombre se conserva para que la historia se lea; lo demas
    esta en tests/unit/test_ultimo_minuto.py."""
    motor = _motor(registro, vocabulario, zona, {fin - 1: tc.ENTRADA - 10})
    r = motor.correr_dia(tc._dia())
    broker = motor.brokers[tc.DIA.isoformat()]
    assert not r.operaciones and not broker.posiciones
    o1 = broker.ordenes["o1"]
    assert o1.estado == CANCELADA and o1.ultimo_cambio_ms == (fin - 1) * MS_POR_MINUTO - 1
    assert "RN-035" in r.sesiones[sesion].disparadas
    assert "RN-002" not in r.sesiones["11-15"].disparadas  # nada abierto que cerrar en el limite
    assert motor.trazas_broker[tc.DIA.isoformat()].cancelados_fin_dia == 0
