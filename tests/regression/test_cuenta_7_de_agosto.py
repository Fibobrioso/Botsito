"""Regresion de `trabajo/corregir-evaluar-fase`: la cuenta del 7 de agosto de 2026 (construccion)
marca la infraccion de perdida diaria en el tick del pico, a las 12:30:01.312 UTC.

Las cuatro operaciones del trader de ese dia se repiten por el broker sobre los ticks de
Dukascopy -precios del caso desplazados -2 puntos, objetivo de 3R, 0,5 % de 100 000 hasta el stop
inicial- y `evaluar_fase` las juzga. Hasta esta rama, la marca que el broker deja en el instante del
cierre se procesaba despues del cierre y reabria la posicion: ese dia la cuenta suspendia a las
12:10:26, con una perdida fantasma que doblaba la de la tercera operacion, cuando el saldo real
seguia por encima del limite (VIABILIDAD-TRADER.md §6).

Necesita los ticks y las M1 de `data/`, que viven fuera de git: sin ellos (la CI), se salta.
"""

from __future__ import annotations

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
from botsito.engine.broker import Broker
from botsito.engine.perfil_cuenta import cargar_perfil
from botsito.engine.simulador_config import FICHERO_LLENADO, cargar_config_llenado

RAIZ = Path(__file__).resolve().parents[2]
CASO = "caso-eurusd-2026-08-07"
DESFASE_PUNTOS = 2  # OANDA - Dukascopy (BLOQUE-DE-LA-CAJA.md §2.3)


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


def test_la_cuenta_del_7_de_agosto_marca_la_perdida_diaria_en_el_pico() -> None:
    md = _mercado()
    registro = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
    perfil = cargar_perfil(RAIZ / "knowledge" / "cuentas" / "ftmo-2step-swing-100k.yaml")
    reglas_fase = cuenta.reglas_de_fase(perfil, "reto")
    contrato = registro.decimal("instrumento_contrato")
    cfg = cargar_config_llenado(RAIZ / FICHERO_LLENADO).configuracion()
    b = Broker(simulacion.reglas_broker_de(perfil), cfg, md.mercado(), contrato, md.escala)
    assert md.operaciones_trader is not None and len(md.operaciones_trader) == 4
    for i, op in enumerate(md.operaciones_trader, 1):
        entrada = int((op.apertura.precio * md.escala).to_integral_value()) - DESFASE_PUNTOS
        stop = int((op.marcas[0].precio * md.escala).to_integral_value()) - DESFASE_PUNTOS
        distancia = abs(entrada - stop)
        objetivo = entrada + (3 if op.direccion == "compra" else -3) * distancia
        lotes = (Decimal(500) / (Decimal(distancia) / md.escala * contrato)).quantize(
            Decimal("0.01"), rounding=ROUND_DOWN
        )
        t = op.apertura.instante
        ms = int(a_minuto(t.replace(second=0, microsecond=0))) * MS_POR_MINUTO + t.second * 1000
        b.abrir_conocida(f"t{i}", op.direccion, entrada, lotes, stop, objetivo, ms, "caso")
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
