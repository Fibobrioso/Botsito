"""A-36 (sesion 4, S-22; `fb-2026-10-04-sesion-04` con `--supersede` del REOPEN): la orden de
entrada va exactamente en el 0 de la caja, contando la mecha, y sin tener en cuenta el spread.
Congela lo que el motor ya hacia (ADR-0064 §2): no falla en `main`; se escribe para que nadie lo
mueva sin decirlo. Velas y mercado SINTETICOS de 2030."""

from __future__ import annotations

from pathlib import Path

from botsito.config.registro import cargar_registro
from botsito.domain.estructura_m1 import VENTA, ultimo_punto_de_ruptura
from botsito.engine import zonas
from tests.unit import test_orden_stop_pivote as top

RAIZ = Path(__file__).resolve().parents[2]
REGISTRO = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")


def test_el_0_es_el_extremo_con_mecha_del_pivote_de_m1() -> None:
    velas = top._serie(top.VENTA_DOS_BAJOS)
    punto = ultimo_punto_de_ruptura(velas, VENTA)
    assert punto is not None
    vela = velas[punto.marca]
    # la mecha, no el cuerpo: en `_serie` la minima queda un punto por debajo del cuerpo
    assert punto.nivel == int(vela.minima) < min(int(vela.abierta), int(vela.cierre))
    datos = top._Datos(velas, toma=top.M0 + 1)
    e = top._estado()
    zonas.zona_del_punto(REGISTRO, top._momento(datos, 0), e)
    z = zonas.zona_del_punto(REGISTRO, top._momento(datos, len(velas) - 1), e)
    assert z is not None and z.entrada == punto.nivel  # el 0 de la caja es el punto, tal cual


def test_la_orden_stop_se_coloca_en_el_0_sin_sumar_el_spread(tmp_path: Path) -> None:
    motor, tc, _ = top._cadena(top._registro(tmp_path))
    assert tc.SPREAD > 0  # el mercado sintetico tiene spread, y la orden no lo lleva
    broker = motor.brokers[tc.DIA.isoformat()]
    assert broker.ordenes["o1"].precio == tc.ENTRADA
    assert broker.ordenes["o2"].precio == tc.ENTRADA - 4  # el 0 de la zona nueva, tal cual
