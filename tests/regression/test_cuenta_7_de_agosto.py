"""Regresion de `trabajo/corregir-evaluar-fase`: la cuenta del 7 de agosto de 2026 (construccion)
marca la infraccion de perdida diaria en el tick del pico, a las 12:30:01.312 UTC.

Las cuatro operaciones del trader de ese dia se repiten por el broker sobre los ticks de
Dukascopy -precios del caso desplazados -2 puntos, objetivo de 3R, 0,5 % de 100 000 hasta el stop
inicial- y `evaluar_fase` las juzga. Hasta esta rama, la marca que el broker deja en el instante del
cierre se procesaba despues del cierre y reabria la posicion: ese dia la cuenta suspendia a las
12:10:26, con una perdida fantasma que doblaba la de la tercera operacion, cuando el saldo real
seguia por encima del limite (VIABILIDAD-TRADER.md §6).

Necesita los ticks y las M1 de `data/`, que viven fuera de git: sin ellos (la CI), se salta.

Desde ADR-0071 (2026-10-09) el perfil de FTMO lleva el volumen maximo medido en la demo, 50 lotes,
y la primera operacion de ese dia pasa de 50 (su stop queda por debajo de 1 pip, ADR-0071 §2): el
broker la rechaza por `volumen_max_lotes`. Esta regresion es del corte de la cuenta, no del volumen,
asi que se repite con el tope que tenia el perfil hasta ese dia, 100, DECLARADO aqui
(`VOLUMEN_MAX_DE_LA_REGRESION`); lo que hace el bot con ese rechazo es el pendiente 37 (A-18).
"""

from __future__ import annotations

import dataclasses
from datetime import UTC, datetime
from decimal import ROUND_DOWN, Decimal
from pathlib import Path

import pytest

from botsito.cases.criterio_fidelidad import cargar_criterio
from botsito.cases.paquete import cargar_config
from botsito.config.ajustes import carpeta_datos
from botsito.config.registro import cargar_registro
from botsito.data.velas import a_minuto
from botsito.domain.ticks import MS_POR_MINUTO
from botsito.engine import cuenta, simulacion
from botsito.engine.broker import Broker, BrokerError
from botsito.engine.perfil_cuenta import cargar_perfil
from botsito.engine.simulador_config import FICHERO_LLENADO, cargar_config_llenado

RAIZ = Path(__file__).resolve().parents[2]
CASO = "caso-eurusd-2026-08-07"
DESFASE_PUNTOS = 2  # OANDA - Dukascopy (BLOQUE-DE-LA-CAJA.md §2.3)
# el tope del perfil hasta ADR-0071 (la web de FTMO); el medido, 50, rechaza la primera operacion
VOLUMEN_MAX_DE_LA_REGRESION = Decimal(100)


def _mercado() -> simulacion.MercadoDia:
    criterio = cargar_criterio(RAIZ)
    registro = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
    config = cargar_config(RAIZ / "knowledge" / "cases" / "kit" / "config.yaml")
    try:
        md = simulacion.mercado_de_construccion(
            RAIZ, carpeta_datos(RAIZ), criterio, config, registro, CASO,
            con_operaciones_del_trader=True,
        )  # fmt: skip
    except (OSError, LookupError, ValueError) as exc:
        pytest.skip(f"sin los datos de construccion en data/: {exc}")
    if not md.origen_ticks:
        pytest.skip("sin los ticks de construccion en data/")
    return md


def _orden(
    op: cuenta.Operacion, escala: int, contrato: Decimal
) -> tuple[cuenta.Direccion, int, Decimal, int, int, int]:
    """(lado, entrada, lotes, stop, objetivo, instante_ms) de una operacion del trader: precios
    desplazados DESFASE_PUNTOS, objetivo de 3R y 0,5 % de 100 000 hasta el stop inicial."""
    entrada = int((op.apertura.precio * escala).to_integral_value()) - DESFASE_PUNTOS
    stop = int((op.marcas[0].precio * escala).to_integral_value()) - DESFASE_PUNTOS
    distancia = abs(entrada - stop)
    objetivo = entrada + (3 if op.direccion == "compra" else -3) * distancia
    lotes = (Decimal(500) / (Decimal(distancia) / escala * contrato)).quantize(
        Decimal("0.01"), rounding=ROUND_DOWN
    )
    t = op.apertura.instante
    ms = int(a_minuto(t.replace(second=0, microsecond=0))) * MS_POR_MINUTO + t.second * 1000
    return op.direccion, entrada, lotes, stop, objetivo, ms


def test_con_el_perfil_real_la_primera_operacion_se_rechaza_por_volumen_maximo() -> None:
    """El hermano de la regresion de abajo, con el perfil REAL: el volumen maximo medido en la demo
    de FTMO (50 lotes, ADR-0071 §2) rechaza la primera operacion del trader del 7 de agosto (dia
    de construccion), porque su stop queda por debajo de 1 pip con el 0,5 % de 100 000. Es la
    consecuencia que declara el informe de `trabajo/demo-ejecucion-1` (§3.2) y el caso que tiene
    que resolver el pendiente 37 (A-18): recortar el lote, partir la orden o no operar."""
    md = _mercado()
    registro = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
    perfil = cargar_perfil(RAIZ / "knowledge" / "cuentas" / "ftmo-2step-swing-100k.yaml")
    contrato = registro.decimal("instrumento_contrato")
    cfg = cargar_config_llenado(RAIZ / FICHERO_LLENADO).configuracion()
    reglas_broker = simulacion.reglas_broker_de(perfil)
    b = Broker(reglas_broker, cfg, md.mercado(), contrato, md.escala)
    assert md.operaciones_trader is not None
    lado, entrada, lotes, stop, objetivo, ms = _orden(md.operaciones_trader[0], md.escala, contrato)
    assert lotes > reglas_broker.volumen_max_lotes
    with pytest.raises(BrokerError, match="volumen_max_lotes"):
        b.abrir_conocida("t1", lado, entrada, lotes, stop, objetivo, ms, "caso")


def test_la_cuenta_del_7_de_agosto_marca_la_perdida_diaria_en_el_pico() -> None:
    md = _mercado()
    registro = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
    perfil = cargar_perfil(RAIZ / "knowledge" / "cuentas" / "ftmo-2step-swing-100k.yaml")
    reglas_fase = cuenta.reglas_de_fase(perfil, "reto")
    contrato = registro.decimal("instrumento_contrato")
    cfg = cargar_config_llenado(RAIZ / FICHERO_LLENADO).configuracion()
    reglas_broker = dataclasses.replace(
        simulacion.reglas_broker_de(perfil), volumen_max_lotes=VOLUMEN_MAX_DE_LA_REGRESION
    )
    b = Broker(reglas_broker, cfg, md.mercado(), contrato, md.escala)
    assert md.operaciones_trader is not None and len(md.operaciones_trader) == 4
    for i, op in enumerate(md.operaciones_trader, 1):
        b.abrir_conocida(f"t{i}", *_orden(op, md.escala, contrato), "caso")
    b.avanzar(md.hasta_ms - 1)
    for p in list(b.posiciones.values()):
        if p.abierta:
            b.cerrar_a_mercado(p.id, md.hasta_ms - 1)
    operaciones = b.operaciones_cerradas()
    # el broker deja la marca del tick que cierra en el instante del cierre: la entrada del fallo
    assert all(any(m.instante == o.cierre.instante for m in o.marcas) for o in operaciones)

    r = cuenta.evaluar_fase(operaciones, reglas_fase, contrato)

    assert r.estado is cuenta.EstadoCuenta.SUSPENDIDA
    assert r.motivo.startswith("perdida diaria"), r.motivo
    assert r.instante == datetime(2026, 8, 7, 12, 30, 1, 312000, tzinfo=UTC)
