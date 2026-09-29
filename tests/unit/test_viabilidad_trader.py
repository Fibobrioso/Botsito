"""La viabilidad del trader (`scripts/viabilidad_trader.py`): sus funciones puras sobre casos
SINTETICOS -el R de una operacion, la clase y la diferencia grande, el bootstrap con semilla, las
estadisticas, el coste de la comision en R, el lote y el veredicto-, con la salida fijada. Ninguna
vela ni ninguna operacion real se lee aqui."""

from __future__ import annotations

import importlib.util
import sys
from decimal import Decimal
from pathlib import Path
from types import ModuleType

import pytest

RAIZ = Path(__file__).resolve().parents[2]


def _cargar() -> ModuleType:
    nombre = "viabilidad_trader"
    if nombre in sys.modules:
        return sys.modules[nombre]
    spec = importlib.util.spec_from_file_location(nombre, RAIZ / "scripts" / f"{nombre}.py")
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def test_el_r_de_una_operacion_y_su_clase() -> None:
    v = _cargar()
    # una compra con stop a 10 puntos que cierra 30 por encima gana 3R; una venta, al reves
    assert v.r_de("compra", 1.10000, 1.09990, 1.10030) == pytest.approx(3.0)
    assert v.r_de("venta", 1.10000, 1.10010, 1.10010) == pytest.approx(-1.0)
    assert v.r_de("venta", 1.10000, 1.10010, 1.10000) == pytest.approx(0.0)
    assert [v.clase(r) for r in (3.0, 0.09, -0.09, -1.0)] == ["gana", "cero", "cero", "pierde"]
    with pytest.raises(ValueError, match="sin R"):
        v.r_de("compra", 1.1, 1.1, 1.2)


def test_la_diferencia_grande() -> None:
    v = _cargar()
    assert v.diferencia_grande(3.0, -1.0)  # cambia la clase
    assert v.diferencia_grande(3.0, 4.2)  # misma clase, mas de 1R
    assert not v.diferencia_grande(3.0, 3.9)
    assert v.diferencia_grande(-1.0, 0.0)  # la anotada a cero: el trader subio el stop


def test_el_bootstrap_y_las_estadisticas_fijadas() -> None:
    v = _cargar()
    assert v.bootstrap([1.0, -1.0, 3.0, -1.0, 0.0], n=2000, semilla=7) == pytest.approx(
        (0.4, -0.8, 1.8)
    )
    assert v.bootstrap([2.0, 2.0, 2.0], n=500) == pytest.approx((2.0, 2.0, 2.0))
    e = v.estadisticas([3.0, -1.0, -1.0, 0.05, 3.0, -1.2])
    assert (e.n, e.ganan, e.pierden, e.cero) == (6, 2, 3, 1)
    assert e.r_medio_ganadoras == pytest.approx(3.0)
    assert e.r_medio_perdedoras == pytest.approx(-3.2 / 3)
    assert (e.esperanza, e.ic_bajo, e.ic_alto) == pytest.approx((0.475, -0.8916667, 1.8416667))
    assert e.tasa_acierto == pytest.approx(2 / 6)


def test_la_comision_en_r_y_el_lote() -> None:
    v = _cargar()
    contrato, escala = Decimal(100000), 100000
    # 5 USD por lote en cada lado frente a un stop de 5 puntos: 2R, sea cual sea el lote
    assert v.comision_en_r(Decimal(5), 2, 5, contrato, escala) == pytest.approx(2.0)
    assert v.comision_en_r(Decimal(5), 1, 20, contrato, escala) == pytest.approx(0.25)
    # 500 USD de riesgo a 15 puntos: 33,33 lotes, hacia abajo a 0,01
    assert v.lote_por_riesgo(Decimal(500), 15, contrato, escala) == Decimal("33.33")
    assert v.lote_por_riesgo(Decimal(500), 0, contrato, escala) == Decimal(0)


def test_el_veredicto() -> None:
    v = _cargar()
    assert v.veredicto("SUPERADA", "objetivo", 0.1, 0.9) == (
        "pasa",
        "alcanza el objetivo con los días mínimos y sin romper un límite",
    )
    assert v.veredicto("SUSPENDIDA", "perdida diaria", -0.4, 0.6)[0] == "no pasa"
    assert "cruza el 0" in v.veredicto("SUSPENDIDA", "perdida diaria", -0.4, 0.6)[1]
    assert v.veredicto("EN_CURSO", "sin objetivo", -0.4, 0.6)[0] == "no concluyente"


def test_las_marcas_en_el_cierre_se_quitan_antes_de_la_cuenta() -> None:
    """Una marca en el mismo instante del cierre -la del tick que salta el stop- no dice nada que
    el cierre no diga; el script la quita antes de `evaluar_fase` (VIABILIDAD-TRADER.md §6)."""
    from datetime import UTC, datetime

    from botsito.engine.cuenta import Marca, Operacion

    v = _cargar()
    t0 = datetime(2030, 1, 15, 8, 0, tzinfo=UTC)
    t1 = datetime(2030, 1, 15, 8, 5, tzinfo=UTC)
    op = Operacion(
        id="x",
        direccion="venta",
        lotes=Decimal(1),
        apertura=Marca(t0, Decimal("1.10000")),
        cierre=Marca(t1, Decimal("1.10010")),
        marcas=(Marca(t0, Decimal("1.10005")), Marca(t1, Decimal("1.10010"))),
    )
    assert v.marcas_en_el_cierre([op]) == 1
    limpia = v.marcas_antes_del_cierre(op)
    assert limpia.marcas == (Marca(t0, Decimal("1.10005")),)
    assert v.marcas_en_el_cierre([limpia]) == 0
