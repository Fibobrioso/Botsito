"""La viabilidad con la comision y las variantes de A-18 (`scripts/viabilidad_comision.py`): sus
funciones puras sobre casos SINTETICOS -los niveles de cada variante en compra y en venta, el R
nominal, los pips, el coste en R y la celda de la tabla-, con la salida fijada. Ninguna vela ni
ninguna operacion real se lee aqui."""

from __future__ import annotations

import importlib.util
import sys
from decimal import Decimal
from pathlib import Path
from types import ModuleType

import pytest

RAIZ = Path(__file__).resolve().parents[2]


def _cargar() -> ModuleType:
    nombre = "viabilidad_comision"
    if nombre in sys.modules:
        return sys.modules[nombre]
    spec = importlib.util.spec_from_file_location(nombre, RAIZ / "scripts" / f"{nombre}.py")
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def test_los_niveles_de_cada_variante() -> None:
    v = _cargar()
    n = v.Niveles
    # compra: entrada (el 0) en 1000, stop del libro (el 1) en 990 -> D = 10, 0,8 D = 8
    assert v.niveles("V1", "compra", 1000, 990) == n(990, None, 1030, 10)
    assert v.niveles("V2", "compra", 1000, 990) == n(992, None, 1030, 8)
    assert v.niveles("V3", "compra", 1000, 990) == n(990, 992, 1030, 10)
    assert v.niveles("V4", "compra", 1000, 990) == n(990, 992, 1024, 10)
    # venta: entrada en 1000, stop en 1015 -> D = 15, 0,8 D = 12
    assert v.niveles("V1", "venta", 1000, 1015) == n(1015, None, 955, 15)
    assert v.niveles("V2", "venta", 1000, 1015) == n(1012, None, 955, 12)
    assert v.niveles("V3", "venta", 1000, 1015) == n(1015, 1012, 955, 15)
    assert v.niveles("V4", "venta", 1000, 1015) == n(1015, 1012, 964, 15)
    # 0,8 D al punto mas cercano: 13 -> 10,4 -> 10; 7 -> 5,6 -> 6
    assert v.niveles("V2", "compra", 1000, 987).distancia_lote == 10
    assert v.niveles("V2", "compra", 1000, 993).distancia_lote == 6
    with pytest.raises(ValueError, match="desconocida"):
        v.niveles("V9", "compra", 1000, 990)
    with pytest.raises(ValueError, match="stop en la entrada"):
        v.niveles("V1", "compra", 1000, 1000)


def test_el_r_nominal_los_pips_y_el_coste() -> None:
    v = _cargar()
    # V2 con lote para 8 puntos: un objetivo a 30 puntos es 3,75 R
    assert v.r_nominal("compra", 1000, 1030, 8) == pytest.approx(3.75)
    assert v.r_nominal("venta", 1000, 1012, 12) == pytest.approx(-1.0)
    # V3: lote para el 1 (10), stop en el 0,8: pierde 0,8 R
    assert v.r_nominal("compra", 1000, 992, 10) == pytest.approx(-0.8)
    assert v.pips(15) == pytest.approx(1.5)
    contrato, escala = Decimal(100000), 100000
    # 10 USD de ida y vuelta frente a 10 puntos por lote: 1 R; y 2 puntos de spread, 0,2 R
    assert v.coste_en_r(Decimal(10), 2, 10, contrato, escala) == pytest.approx((1.0, 0.2))
    assert v.coste_en_r(Decimal(3), 0, 15, contrato, escala) == pytest.approx((0.2, 0.0))


def test_la_celda_de_la_tabla() -> None:
    v = _cargar()
    assert (
        v.celda(0.123, -0.4, 0.6, ["pasa", "no pasa", "no concluyente"])
        == "+0,12 [-0,40; +0,60] · pasa / no pasa / no concluyente"
    )
