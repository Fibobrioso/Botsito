"""Tests de humo de `premisa.py`, sobre datos sinteticos, en los dos sentidos.

`make check` no los recoge (`testpaths = ["tests"]`). Desde la raiz:
    uv run pytest docs/validation/anexos/DIAGNOSTICO-PREMISA/test_premisa.py -p no:cacheprovider

Cubren lo que pide el encargo (fase 1): el R del registro de una compra y de una venta; los tres
tramos de R con sus fronteras (+0,2 y -0,2 exactos); la brecha y las dos lecturas de §5 con la
frontera de 0,20; el R con lote fijo con D iguales (D2 c) y con D distintas, hecho a mano; las tres
lecturas de §4 con sus fronteras; y el retroceso de una compra y de una venta, con sus tramos, el
1,0 exacto y los minutos del respaldo M1. Las cifras se leen de los yaml.
"""

from __future__ import annotations

import sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import premisa as pm  # noqa: E402

from botsito.comun.yaml_estricto import leer_yaml  # noqa: E402

PREMISA = leer_yaml(pm.RAIZ / "docs" / "plan" / "PREMISA-COSTES.yaml")
META = leer_yaml(pm.RAIZ / "docs" / "plan" / "META-TECHO-PAREJAS.yaml")
CRITERIO = leer_yaml(pm.RAIZ / "knowledge" / "cases" / "criterio_fidelidad.yaml")
RFR = PREMISA["registro_frente_a_replica"]
GANA = Decimal(RFR["tramos_r"]["gana_si_mas_de"])
PIERDE = Decimal(RFR["tramos_r"]["pierde_si_menos_de"])
MARGEN = Decimal(RFR["margen_r"])
ORDEN_5 = list(RFR["lectura"]["orden"])
ORDEN_4 = list(PREMISA["backtest_del_trader"]["lectura"]["orden"])
TRAMOS = [Fraction(Decimal(t)) for t in RFR["retroceso_de_las_ganadoras"]["tramos"]]
N_MIN = int(CRITERIO["rentabilidad"]["n_minimo"])
ESP_MIN = Decimal(CRITERIO["rentabilidad"]["esperanza_minima_r"])
ALTO_MIN = Decimal(META["propios"]["techo_no_gana_si_percentil_alto_por_debajo_de_r"])
D = Decimal
UN_PUNTO = D("0.00001")
MS = pm.MS


# --------------------------------------------------------------- el R del registro


def test_el_r_de_una_compra_y_de_una_venta() -> None:
    # compra: entrada 1,10000, stop 1,09900 (D = 0,00100); sale a 1,10300 -> +3; a 1,09950 -> -0,5
    assert pm.r_registro("compra", D("1.10000"), D("1.09900"), D("1.10300")) == D(3)
    assert pm.r_registro("compra", D("1.10000"), D("1.09900"), D("1.09950")) == D("-0.5")
    # venta: entrada 1,10000, stop 1,10100; sale a 1,09800 -> +2; a 1,10100 -> -1
    assert pm.r_registro("venta", D("1.10000"), D("1.10100"), D("1.09800")) == D(2)
    assert pm.r_registro("venta", D("1.10000"), D("1.10100"), D("1.10100")) == D(-1)
    # el mismo movimiento con la direccion cambiada cambia el signo
    assert pm.r_registro("venta", D("1.10000"), D("1.09900"), D("1.10300")) == D(-3)


def test_los_tres_tramos_de_r_con_sus_fronteras() -> None:
    assert D("0.2") == GANA
    assert D("-0.2") == PIERDE
    assert pm.tramo_r(GANA, GANA, PIERDE) == pm.BREAK_EVEN  # +0,2 exacto no gana
    assert pm.tramo_r(GANA + UN_PUNTO, GANA, PIERDE) == pm.GANADORA
    assert pm.tramo_r(PIERDE, GANA, PIERDE) == pm.BREAK_EVEN  # -0,2 exacto no pierde
    assert pm.tramo_r(PIERDE - UN_PUNTO, GANA, PIERDE) == pm.PERDEDORA
    assert pm.tramo_r(D(0), GANA, PIERDE) == pm.BREAK_EVEN


# --------------------------------------------------------------- la brecha y §5


def test_la_brecha_es_registro_menos_replica() -> None:
    assert pm.brecha(D("0.98"), D("0.65")) == D("0.33")
    assert pm.brecha(D("0.10"), D("0.30")) == D("-0.20")
    assert pm.brecha(None, D(1)) is None


def test_las_dos_lecturas_de_5_con_la_frontera_de_0_20() -> None:
    assert D("0.20") == MARGEN
    pierde, peores = ORDEN_5
    base = D("0.33")
    # la diferencia exactamente igual al margen no lo supera
    assert pm.lectura_de_5(base + MARGEN, base, MARGEN, ORDEN_5) == peores
    assert pm.lectura_de_5(base + MARGEN + UN_PUNTO, base, MARGEN, ORDEN_5) == pierde
    assert pm.lectura_de_5(base - D(1), base, MARGEN, ORDEN_5) == peores
    try:
        pm.lectura_de_5(None, base, MARGEN, ORDEN_5)
    except ValueError:
        pass
    else:
        raise AssertionError("una brecha sin definir tiene que romper")


# --------------------------------------------------------------- el lote fijo (D2 c)


def test_con_todas_las_d_iguales_el_r_con_lote_fijo_es_el_r_neto() -> None:
    rs = [D("1.5"), D("-1"), D("0.25"), D("2.9")]
    assert pm.r_con_lote_fijo(rs, [12, 12, 12, 12]) == rs


def test_con_d_distintas_el_r_con_lote_fijo_hecho_a_mano() -> None:
    # mediana de [10, 20, 30] = 20: 1 x 10/20, -1 x 20/20, 2 x 30/20
    assert pm.r_con_lote_fijo([D(1), D(-1), D(2)], [10, 20, 30]) == [D("0.5"), D(-1), D(3)]
    # mediana de [10, 20] = 15 (par): 3 x 10/15 = 2, -3 x 20/15 = -4
    assert pm.r_con_lote_fijo([D(3), D(-3)], [10, 20]) == [D(2), D(-4)]
    # la mediana, en Decimal: el central con N impar, la media de los dos centrales con N par
    assert pm.mediana_de([30, 10, 20]) == D(20)
    assert pm.mediana_de([21, 10]) == D("15.5")
    # y no es el R neto cuando las D difieren
    assert pm.r_con_lote_fijo([D(1), D(1)], [10, 30]) != [D(1), D(1)]


# --------------------------------------------------------------- las tres lecturas de §4


def _l4(n: int, esp: str, bajo: str, alto: str) -> str:
    return pm.lectura_de_4(n, D(esp), D(bajo), D(alto), N_MIN, ESP_MIN, ALTO_MIN, ORDEN_4)


def test_las_tres_lecturas_de_4_con_sus_fronteras() -> None:
    assert ORDEN_4 == ["gana", "no_gana", "no_concluyente"]
    bien = str(ALTO_MIN + 1)
    assert _l4(N_MIN, str(ESP_MIN), "0.001", bien) == "gana"  # las tres fronteras justas
    assert _l4(N_MIN - 1, str(ESP_MIN), "0.001", bien) == "no_concluyente"  # una de menos
    assert _l4(N_MIN, str(ESP_MIN - UN_PUNTO), "0.001", bien) == "no_concluyente"
    assert _l4(N_MIN, str(ESP_MIN), "0", bien) == "no_concluyente"  # percentil bajo 0: no gana
    assert _l4(N_MIN, "-0.00001", "-0.5", bien) == "no_gana"  # esperanza negativa
    assert _l4(N_MIN, "0", "-0.5", str(ALTO_MIN)) == "no_concluyente"  # alto en el umbral
    assert _l4(N_MIN, "0", "-0.5", str(ALTO_MIN - UN_PUNTO)) == "no_gana"
    assert pm.lectura_de_4(5, None, None, None, N_MIN, ESP_MIN, ALTO_MIN, ORDEN_4) == (
        "no_concluyente"
    )


# --------------------------------------------------------------- el retroceso


def test_el_retroceso_de_una_compra_y_de_una_venta_con_el_1_0_exacto() -> None:
    desfase = int(
        leer_yaml(pm.RAIZ / "docs" / "plan" / "PUENTE-TECHO.yaml")["propios"]["desfase_puntos"]
    )
    entrada, d = 110_000, 10
    ref = entrada - desfase
    # compra: el BID minimo, desde la entrada menos el desfase
    assert pm.retroceso("compra", entrada, desfase, ref - 10, d) == Fraction(1)
    assert pm.retroceso("compra", entrada, desfase, ref - 9, d) == Fraction(9, 10)
    assert pm.retroceso("compra", entrada, desfase, ref + 1, d) == Fraction(-1, 10)
    # venta: el ASK maximo, por encima de la entrada menos el desfase
    assert pm.retroceso("venta", entrada, desfase, ref + 10, d) == Fraction(1)
    assert pm.retroceso("venta", entrada, desfase, ref + 5, d) == Fraction(1, 2)
    assert pm.retroceso("venta", entrada, desfase, ref - 1, d) == Fraction(-1, 10)


def test_los_tramos_de_retroceso_con_sus_fronteras() -> None:
    assert [float(t) for t in TRAMOS] == [0.0, 0.5, 0.8, 1.0]
    nombres = pm.nombres_de_tramos(TRAMOS)
    t = pm.tramo_de_retroceso
    assert t(Fraction(0), TRAMOS) == nombres[0]
    assert t(Fraction(49, 100), TRAMOS) == nombres[0]
    assert t(Fraction(1, 2), TRAMOS) == nombres[1]
    assert t(Fraction(79, 100), TRAMOS) == nombres[1]
    assert t(Fraction(4, 5), TRAMOS) == nombres[2]
    assert t(Fraction(99, 100), TRAMOS) == nombres[2]
    assert t(Fraction(1), TRAMOS) == nombres[3]  # el 1,0 exacto, en «1,0 o mas»
    assert t(Fraction(3), TRAMOS) == nombres[3]
    assert t(Fraction(-1, 100), TRAMOS) == "por_debajo"


def _tick(ms: int, bid: int, ask: int) -> Any:
    return SimpleNamespace(instante=ms, bid=bid, ask=ask)


def _mercado(ticks: dict[int, list[Any]], velas: dict[int, Any]) -> tuple[Any, Any]:
    return (lambda m: ticks.get(m)), (lambda m: velas.get(m))


def test_el_extremo_con_ticks_y_con_el_respaldo_m1() -> None:
    m0 = 1_000_000  # minutos sinteticos
    ticks = {
        m0: [_tick(m0 * MS + 10_000, 100, 102), _tick(m0 * MS + 50_000, 97, 99)],
        m0 + 2: [_tick((m0 + 2) * MS + 1_000, 99, 101), _tick((m0 + 2) * MS + 59_000, 90, 120)],
    }
    velas = {m0 + 1: SimpleNamespace(minima=95, maxima=104)}  # el minuto m0+1, sin ticks

    def spread(_m: int) -> int:
        return 3

    tk, m1 = _mercado(ticks, velas)
    desde, hasta = m0 * MS + 20_000, (m0 + 2) * MS + 30_000  # deja fuera el primero y el ultimo
    compra = pm.extremo_en_contra("compra", desde, hasta, tk, m1, spread)
    assert (compra.precio, compra.del_respaldo, compra.minutos_con_respaldo) == (95, True, 1)
    venta = pm.extremo_en_contra("venta", desde, hasta, tk, m1, spread)
    assert (venta.precio, venta.del_respaldo) == (107, True)  # 104 + 3 de spread
    # sin la M1 del respaldo, el extremo sale de los ticks dentro del tramo
    tk2, m1_vacio = _mercado(ticks, {})
    compra2 = pm.extremo_en_contra("compra", desde, hasta, tk2, m1_vacio, spread)
    assert (compra2.precio, compra2.del_respaldo, compra2.minutos_sin_datos) == (97, False, 1)
    venta2 = pm.extremo_en_contra("venta", desde, hasta, tk2, m1_vacio, spread)
    assert venta2.precio == 101  # el ASK de 120 cae fuera del tramo
