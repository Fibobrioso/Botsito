"""RN-020 retira la orden pendiente al llegar al tope del trader (ADR-0086, DECISION DEL CONSULTOR
con el modelo y el motivo de RN-036, ADR-0077 §3). Por el cableado real y la spec real: un
acumulador `perdida_dia` SINTETICO alcanza el tope en un cierre de M1 con una orden colocada y sin
llenar; RN-020 dispara, fija detenido_por_tope, prohibe abrir y cancela la orden en ese mismo
cierre; el cableado no encuentra nada al fin del dia. Todo sintetico, el dia es de 2030. Falla con
el codigo de main: alli la orden seguia viva hasta que RN-035 la retiraba."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import pytest

from botsito.config.registro import Registro, cargar_registro
from botsito.domain.ticks import MS_POR_MINUTO
from botsito.engine.broker import CANCELADA, PETICION_CANCELAR, PETICION_COLOCAR
from botsito.engine.interprete import EstadoDia, Momento, Resultado, Tri
from botsito.spec.modelo import cargar_reglas, cargar_vocabulario
from tests.unit import test_cableado as tc

TOPE_EN = tc.MINUTO_ZONA + 5  # el cierre de M1 en que el acumulador sintetico alcanza el tope


@pytest.fixture(scope="module")
def registro() -> Registro:
    return cargar_registro(tc.RAIZ / "knowledge" / "spec" / "parametros.yaml")


@pytest.fixture(scope="module")
def vocabulario() -> dict[str, dict[str, Any]]:
    return cargar_vocabulario(tc.SPEC)


def _motor(registro: Registro, vocabulario: dict[str, dict[str, Any]]) -> Any:
    """La orden se coloca en MINUTO_ZONA y el precio no baja a ella; desde TOPE_EN el acumulador
    `perdida_dia` dice que el tope del dia esta alcanzado (sintetico: el cableado real mide la
    perdida de la cuenta, y aqui no hay ninguna)."""
    motor = tc._motor(registro, vocabulario, tc._mercado({}))
    predicados, acumuladores = tc._sinteticas()

    def tope_alcanzado(args: Mapping[str, Any], momento: Momento, estado: EstadoDia) -> Any:
        return Resultado(Tri.SI if int(momento.instante) >= TOPE_EN else Tri.NO)

    motor.primitivas_extra = predicados
    motor.acumuladores_extra = {**acumuladores, "perdida_dia": tope_alcanzado}
    return motor


def test_rn020_retira_la_orden_pendiente_al_llegar_al_tope(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    motor = _motor(registro, vocabulario)
    r = motor.correr_dia(tc._dia())
    traza = r.sesiones["07-11"]
    assert "RN-020" in traza.disparadas
    assert (TOPE_EN, "RN-020", "detenido_por_tope", "hasta_el_corte_siguiente") in traza.fijados
    broker = motor.brokers[tc.DIA.isoformat()]
    o1 = broker.ordenes["o1"]
    assert o1.colocada_ms == tc.MINUTO_ZONA * MS_POR_MINUTO - 1
    assert o1.estado == CANCELADA and o1.ultimo_cambio_ms == TOPE_EN * MS_POR_MINUTO - 1
    assert not r.operaciones and not broker.posiciones
    tb = motor.trazas_broker[tc.DIA.isoformat()]
    assert tb.cancelados_fin_dia == 0
    assert [(p.tipo, p.id) for p in tb.peticiones] == [
        (PETICION_COLOCAR, "o1"),
        (PETICION_CANCELAR, "o1"),
    ]
    # y despues del tope no se coloca nada mas: RN-020 sigue prohibiendo con el hecho encendido
    assert "RN-035" not in traza.disparadas  # a las 10:59 ya no habia nada que retirar


def test_la_forma_de_rn020_lleva_la_accion_de_rn036(vocabulario: dict[str, dict[str, Any]]) -> None:
    reglas = {r.id: r for r in cargar_reglas(tc.SPEC)}
    rn020, rn036 = reglas["RN-020"], reglas["RN-036"]
    assert isinstance(rn020.forma, dict) and isinstance(rn036.forma, dict)
    assert rn020.clase == "gate" and rn020.vigente
    hace = rn020.forma["entonces"]["hace"]
    assert {"retirar_ordenes_pendientes": {}} in hace
    assert {"retirar_ordenes_pendientes": {}} in rn036.forma["entonces"]["hace"]
    assert rn020.forma["entonces"]["prohibe"] == ["abrir_operacion"]
    assert vocabulario["acciones"]["retirar_ordenes_pendientes"]["argumentos"] == []
