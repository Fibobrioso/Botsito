"""La vida de la orden en la cola de simulacion (rama `trabajo/corrida-construccion`, respuesta del
consultor a la PARADA 2, punto 1.b): «### Ordenes» (una linea por orden que el bot intento colocar,
con su resultado y su motivo) y «### Rechazos por motivo». Todo sintetico, sobre el cableado real
y la spec real, con los dias de 2030 de `test_cableado`: una llenada, una rechazada con su motivo,
una cancelada a ventana_fin, una cancelada al abrir otra sesion y una viva al cerrar el dia. Nada
de esto decide: solo lee la traza del broker, y las opciones del comando siguen siendo las mismas.
"""

from __future__ import annotations

import dataclasses
from decimal import Decimal
from types import SimpleNamespace
from typing import Any

import pytest

from botsito.config.registro import Registro, cargar_registro
from botsito.domain.ticks import MS_POR_MINUTO
from botsito.engine import cableado
from botsito.engine.broker import (
    CANCELADA,
    MOTIVO_PRECIO_INVALIDO,
    PETICION_CANCELAR,
    Broker,
    Rechazo,
    margen_requerido,
)
from botsito.engine.entrada import STOP_EN_RUPTURA
from botsito.engine.llenado import Configuracion
from botsito.engine.perfil_cuenta import cargar_perfil
from botsito.engine.simulacion import reglas_broker_de
from botsito.spec.modelo import cargar_vocabulario
from tests.unit import test_cableado as tc

DIA = tc.DIA.isoformat()
ZONA_TARDE = tc.MINUTO_ZONA + 240  # 12:00 UTC, dentro de la sesion 11-15
PRECIO = Decimal(tc.ENTRADA) / tc.ESCALA  # 1.09995


@pytest.fixture(scope="module")
def registro() -> Registro:
    return cargar_registro(tc.RAIZ / "knowledge" / "spec" / "parametros.yaml")


@pytest.fixture(scope="module")
def vocabulario() -> dict[str, dict[str, Any]]:
    return cargar_vocabulario(tc.SPEC)


def _lineas_de_ordenes(motor: Any) -> list[str]:
    texto = cableado.informe_simulacion(motor)
    assert texto.count(cableado.CABECERA_ORDENES) == 1
    seccion = texto.split("### Ordenes", 1)[1].split("### Rechazos por motivo", 1)[0]
    return [ln for ln in seccion.splitlines() if ln.startswith(f"{DIA} | ")]


def _rechazos(motor: Any) -> list[str]:
    texto = cableado.informe_simulacion(motor)
    seccion = texto.split("### Rechazos por motivo (mes | motivo | peticion | rechazos)", 1)[1]
    seccion = seccion.split("### Peticiones al servidor", 1)[0]
    return [ln for ln in seccion.splitlines() if ln.strip()]


# ------------------------------------------------------------------------------ llenada


def test_una_orden_llenada_sale_llenada_con_el_instante_del_llenado(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    motor = tc._motor(registro, vocabulario, tc._mercado(tc.RUTA_STOP))
    motor.correr_dia(tc._dia())
    broker = motor.brokers[DIA]
    p = next(iter(broker.posiciones.values()))
    (fila,) = _lineas_de_ordenes(motor)
    o1 = broker.ordenes["o1"]
    colocada = cableado._instante(o1.colocada_ms).isoformat()
    # las siete columnas de margen (rama trabajo/margen-lote): el lote COLOCADO, la distancia, el
    # margen que pide la orden al ask del cierre en que se coloco (la UNICA funcion de margen), el
    # margen libre de la cuenta (100.000, sin nada vivo), el riesgo en % del saldo, el lote del
    # RIESGO (0,5 % de 100.000 sobre 16 puntos: 31,25) y el limite que mordio. En este dia sintetico
    # el lote del riesgo pide mas margen del que hay (la medida 2) y desde ADR-0081 el cableado lo
    # limita al que cabe en el 95 % del margen libre: el colocado es menor y su margen cabe
    ask, _ = broker.precio_de_conversion("compra", o1.colocada_ms)
    requerido = margen_requerido(
        o1.lotes, ask, broker.escala, broker.contrato, broker.reglas.apalancamiento or 0
    )
    riesgo = o1.lotes * 16 / broker.escala * broker.contrato / Decimal(100_000) * 100
    assert fila == (
        f"{DIA} | 07-11 | o1 | {colocada} | {PRECIO} | llenada | - | "
        f"{cableado._instante(p.abierta_ms).isoformat()} | {o1.lotes} | 16 | {requerido:.2f} | "
        f"100000.00 | {riesgo:.3f} | 31.25 | margen | - | -"
    )  # las dos ultimas (rama trabajo/punto-usado): sin productor, sin punto ni caja
    assert o1.lotes < Decimal("31.25") and requerido <= Decimal("0.95") * Decimal(100_000)
    assert "ordenes: llenada 1" in cableado.informe_simulacion(motor)
    assert _rechazos(motor) == ["ninguno"]
    assert "no enviadas: 0" in cableado.informe_simulacion(motor)


def test_sin_apalancamiento_en_el_perfil_las_columnas_de_margen_dicen_sin_medida(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    """El otro sentido del campo (regimen de `bloqueadas`, R3.1): un perfil sin apalancamiento no
    tiene margen que medir, y las dos columnas de margen salen `-`; el lote, la distancia y el
    riesgo siguen saliendo, porque no dependen del apalancamiento. Nada mas cambia."""
    motor = tc._motor(registro, vocabulario, tc._mercado(tc.RUTA_STOP))
    motor.reglas_broker = dataclasses.replace(motor.reglas_broker, apalancamiento=None)
    motor.correr_dia(tc._dia())
    (fila,) = _lineas_de_ordenes(motor)
    assert fila.endswith(
        f" | 31.25 | 16 | {cableado.SIN_MEDIDA} | {cableado.SIN_MEDIDA} | 0.500 | 31.25 | ninguno"
        f" | {cableado.SIN_MEDIDA} | {cableado.SIN_MEDIDA}"
    )
    assert " | llenada | - | " in fila
    assert "ordenes: llenada 1" in cableado.informe_simulacion(motor)


# ---------------------------------------------------------------------------- rechazada


def test_una_orden_rechazada_sale_con_el_motivo_del_broker_y_cuenta_por_motivo(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    """En RUTA_STOP el precio esta por encima de la entrada cuando se coloca: una compra STOP alli
    queda del lado equivocado y el broker la rechaza (ADR-0057, `test_cableado`)."""
    motor = tc._motor(registro, vocabulario, tc._mercado(tc.RUTA_STOP))
    motor.tipo_orden = STOP_EN_RUPTURA
    motor.correr_dia(tc._dia())
    broker = motor.brokers[DIA]
    assert not broker.posiciones
    filas = _lineas_de_ordenes(motor)
    assert filas and all(f" | rechazada | {MOTIVO_PRECIO_INVALIDO} | " in f for f in filas), filas
    rechazos = _rechazos(motor)
    assert rechazos == [f"2030-01 | {MOTIVO_PRECIO_INVALIDO} | colocar | {len(filas)}"]
    assert f"rechazos del broker: {len(filas)}" in cableado.informe_simulacion(motor)


# ------------------------------------------------------- cancelada: ventana_fin, otra sesion


def _motor_con_zona(
    registro: Registro, vocabulario: dict[str, dict[str, Any]], zona: int, ruta: Any
) -> Any:
    motor = tc._motor(registro, vocabulario, tc._mercado(ruta))
    predicados, acumuladores = tc._sinteticas(zona)
    motor.primitivas_extra = predicados
    motor.acumuladores_extra = acumuladores
    return motor


def test_la_pendiente_de_la_tarde_sale_cancelada_en_ventana_fin_por_rn035(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    """Como `test_rn035_ventana_fin`: la orden de la tarde no se llena y RN-035 la retira; la fila
    dice donde cayo el cierre y que reglas dispararon. CAMBIA DE SENTIDO A PROPOSITO el 2026-10-26
    (sesion 5, S-22): la retirada es un minuto antes de ventana_fin, en el ultimo tramo de la vela
    H4, y la fila lo dice asi."""
    antelacion = registro.minutos("cierre_h4_antelacion")
    retirada = (tc.MINUTO_FIN - antelacion) * MS_POR_MINUTO - 1
    motor = _motor_con_zona(registro, vocabulario, ZONA_TARDE, {})
    motor.correr_dia(tc._dia())
    tb = motor.trazas_broker[DIA]
    assert tb.cancelados_fin_dia == 0
    assert [(ms, id) for ms, id, _ in tb.cancelaciones] == [(retirada, "o1")]
    (fila,) = _lineas_de_ordenes(motor)
    campos = fila.split(" | ")
    assert campos[1:3] == ["11-15", "o1"] and campos[5] == "cancelada"
    assert campos[6].startswith(
        "en el ultimo tramo de la vela H4; reglas disparadas en ese cierre: "
    )
    assert "RN-035" in campos[6] and "viva" not in fila
    assert campos[7] == cableado._instante(retirada).isoformat()


def test_la_pendiente_de_la_manana_sale_cancelada_al_abrir_otra_sesion(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    """CAMBIA DE SENTIDO A PROPOSITO el 2026-10-26 (sesion 5, S-22): la orden de la manana ya no
    sale cancelada al abrir la tarde sino un minuto antes, en el ultimo tramo de su vela H4; el
    nombre se conserva para que la historia se lea."""
    antelacion = registro.minutos("cierre_h4_antelacion")
    motor = _motor_con_zona(registro, vocabulario, tc.MINUTO_ZONA, {})
    motor.correr_dia(tc._dia())
    tb = motor.trazas_broker[DIA]
    apertura_tarde = next(d for n, d, _ in tb.limites if n == "11-15")
    assert [(ms, id) for ms, id, _ in tb.cancelaciones] == [
        ((apertura_tarde - antelacion) * MS_POR_MINUTO - 1, "o1")
    ]
    (fila,) = _lineas_de_ordenes(motor)
    campos = fila.split(" | ")
    assert campos[1:3] == ["07-11", "o1"] and campos[5] == "cancelada"
    assert campos[6].startswith(
        "en el ultimo tramo de la vela H4; reglas disparadas en ese cierre: "
    )
    assert "RN-035" in campos[6]


def test_el_motivo_de_una_cancelacion_dice_donde_cayo_y_que_disparo() -> None:
    limites = (("07-11", 100, 340), ("11-15", 340, 580))
    assert cableado._motivo_de_cancelacion(340, limites, ["RN-035", "RN-003"]) == (
        "al abrir otra sesion; reglas disparadas en ese cierre: RN-003, RN-035"
    )
    assert cableado._motivo_de_cancelacion(580, limites, ["RN-035"]) == (
        "en ventana_fin; reglas disparadas en ese cierre: RN-035"
    )
    assert cableado._motivo_de_cancelacion(200, limites, ["RN-004", "RN-006"]) == (
        "reglas disparadas en ese cierre: RN-004, RN-006"
    )
    assert cableado._motivo_de_cancelacion(200, limites, []) == (
        f"reglas disparadas en ese cierre: {cableado.MOTIVO_SIN_REGLA}"
    )
    # la apertura de la PRIMERA sesion no es «abrir otra sesion»
    assert cableado._motivo_de_cancelacion(100, limites, ["RN-035"]).startswith("reglas ")
    # el ultimo tramo de la vela H4 (sesion 5, S-22), con la antelacion del registro: el minuto
    # anterior a cada limite, y no el limite ni dos antes
    assert cableado._motivo_de_cancelacion(339, limites, ["RN-035"], 1) == (
        "en el ultimo tramo de la vela H4; reglas disparadas en ese cierre: RN-035"
    )
    assert cableado._motivo_de_cancelacion(579, limites, ["RN-035"], 1).startswith("en el ultimo ")
    assert cableado._motivo_de_cancelacion(338, limites, ["RN-035"], 1).startswith("reglas ")
    assert cableado._motivo_de_cancelacion(339, limites, ["RN-035"]).startswith("reglas ")


def test_la_sesion_de_una_orden_es_la_del_cierre_en_que_se_coloco() -> None:
    """Revisor de la rama (b1): la orden del PRIMER cierre de una sesion se coloca en
    `desde * MS - 1`, y su sesion es la que abre, no la anterior ni «-». Y la del ultimo cierre
    (ventana_fin) es la sesion que termina."""
    limites = (("07-11", 100, 340), ("11-15", 340, 580))
    ms = MS_POR_MINUTO
    assert cableado._sesion_de(100 * ms - 1, limites) == "07-11"  # el cierre de apertura
    assert cableado._sesion_de(340 * ms - 1, limites) == "11-15"  # el cierre que abre la tarde
    assert cableado._sesion_de(339 * ms - 1, limites) == "07-11"  # el cierre anterior
    assert cableado._sesion_de(580 * ms - 1, limites) == "11-15"  # ventana_fin
    assert cableado._sesion_de(99 * ms - 1, limites) == "-"  # antes de la ventana
    assert cableado._sesion_de(581 * ms - 1, limites) == "-"  # despues
    # en los dos sentidos: con el minuto de `colocada_ms` a secas, la de apertura saldria fuera
    assert cableado._sesion(limites, (100 * ms - 1) // ms)[0] is None


# ------------------------------------------------------------------ viva al cerrar el dia


def test_una_orden_que_la_red_de_seguridad_cancela_sale_viva_al_cerrar_el_dia(
    registro: Registro,
) -> None:
    """La red de seguridad de ADR-0053 §6 no encuentra nada con la spec de hoy (RN-035 llega
    antes), asi que se ejercita la lectura de la traza con un broker y una traza escritos a mano:
    la cancelacion del fin del dia lleva su motivo propio y el resultado es «viva»."""
    perfil = cargar_perfil(tc.PERFIL)
    md = tc._mercado({})
    fin_ms = tc.MINUTO_FIN * MS_POR_MINUTO - 1
    broker = Broker(
        reglas_broker_de(perfil, registro),
        Configuracion(False, 0, lambda _m: tc.SPREAD),
        md.mercado(),
        registro.decimal("instrumento_contrato"),
        md.escala,
        saldo=lambda: Decimal(100_000),  # con apalancamiento en el perfil es obligatorio (ADR-0081)
    )
    ms = tc.MINUTO_ZONA * MS_POR_MINUTO - 1
    o = broker.colocar_limite("o1", "compra", tc.ENTRADA, Decimal("0.1"), tc.EXTREMO + 4,
                              tc.ENTRADA + 60, ms)  # fmt: skip
    assert not isinstance(o, Rechazo)
    broker.avanzar(fin_ms)
    broker.cancelar("o1", fin_ms)
    assert broker.ordenes["o1"].estado == CANCELADA
    tb = cableado.TrazaBroker(
        limites=(("07-11", tc.MINUTO_INI, tc.FIN_H4), ("11-15", tc.FIN_H4, tc.MINUTO_FIN))
    )
    tb.cancelados_fin_dia = 1
    tb.cancelaciones.append((fin_ms, "o1", cableado.MOTIVO_FIN_DIA))
    tb.peticiones = [p for p in broker.traza().peticiones if p.tipo == PETICION_CANCELAR]
    motor = SimpleNamespace(trazas_broker={DIA: tb}, brokers={DIA: broker})
    filas = cableado.vida_de_las_ordenes(motor)  # type: ignore[arg-type]
    assert len(filas) == 1
    dia, sesion, id, colocada, precio, resultado, motivo, cuando = filas[0][:8]
    # sin anotacion de margen en la traza (este test monta la traza a mano), las columnas de
    # margen van en None y el limite en `-`; el lote y la distancia salen de la orden; y sin
    # productor (un motor sin `estados`), el punto es `-` y la caja None (trabajo/punto-usado)
    assert filas[0][8:] == (
        broker.ordenes["o1"].lotes,
        abs(tc.ENTRADA - broker.ordenes["o1"].stop),
        None,
        None,
        None,
        None,
        cableado.SIN_MEDIDA,
        cableado.SIN_MEDIDA,
        None,
    )
    assert (dia, sesion, id, precio, resultado) == (
        DIA,
        "07-11",
        "o1",
        PRECIO,
        "viva al cerrar el dia",
    )
    assert motivo == cableado.MOTIVO_FIN_DIA
    assert cuando is not None and cuando == cableado._instante(fin_ms)
    assert colocada == cableado._instante(ms)
    # y en el texto, en los dos sentidos: viva, no cancelada
    linea = cableado._informe_ordenes(motor)[2]  # type: ignore[arg-type]
    assert " | viva al cerrar el dia | " in linea and " | cancelada | " not in linea
