"""Tests de humo de `techo_parejas.py`, sobre datos sinteticos (fechas de 2030), en dos sentidos.

`make check` no los recoge (`testpaths = ["tests"]`). Desde la raiz:
    uv run pytest docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/test_techo_parejas.py \\
        -p no:cacheprovider

Cubren lo que pide el encargo (fase 1): una salida A, una B, una C y una D construidas a mano; el
control que falla con una posicion cambiada al centimo; y que el remuestreo de la diferencia por
`remuestreo_por_dias` da lo mismo que su cuenta a mano en un caso pequeno. Ademas, las piezas puras
del modelo (la caja derivada, el objetivo, el lote del riesgo) y la salida del pivote. Las lecturas
se hacen en el orden que dice `docs/plan/META-TECHO-PAREJAS.yaml`, leido del repo.
"""

from __future__ import annotations

import random
import sys
from decimal import ROUND_UP, Decimal
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import techo_parejas as tp  # noqa: E402

from botsito.comun.yaml_estricto import leer_yaml  # noqa: E402

META = leer_yaml(tp.RAIZ / "docs" / "plan" / "META-TECHO-PAREJAS.yaml")
ORDEN_TECHO = META["lecturas"]["orden_de_lectura_del_techo"]
ORDEN_PAREJAS = list(META["lecturas"]["parejas"])
D = Decimal


def _medida(
    n: int = 120,
    esperanza: str = "0.20",
    bajo: str = "0.05",
    alto: str = "0.40",
    diaria: str = "0.02",
    equity: str = "0.97",
    suspendidas: tuple[str, ...] = (),
) -> tp.Medida:
    return tp.Medida(
        n, D(esperanza), D(bajo), D(alto), 0, Fraction(diaria), "2030-01", Fraction(equity),
        "2030-01", suspendidas,
    )  # fmt: skip


def _techo(m: tp.Medida) -> str:
    return tp.lectura_techo(
        m, 100, D("0.10"), Fraction("0.03"), Fraction("0.06"), D("0.10"), ORDEN_TECHO
    )


def _parejas(n: int, media: str, bajo: str, alto_dif: str) -> str:
    return tp.lectura_parejas(
        n, 19, D(media), D(bajo), D(alto_dif), D("0.10"), D("0"), D("0"), ORDEN_PAREJAS
    )


# --------------------------------------------------------------------- las cuatro salidas


def test_salida_a() -> None:
    assert _techo(_medida()) == "gana"
    assert _parejas(25, "0.15", "0.01", "0.10") == "ganan"
    assert tp.salida_de("gana", "ganan") == "A"


def test_salida_b() -> None:
    assert _parejas(25, "-0.10", "-0.30", "-0.05") == "pierden"
    assert tp.salida_de(_techo(_medida()), "pierden") == "B"


def test_salida_c() -> None:
    assert _techo(_medida(diaria="0.035")) == "no_gana"  # d) incumplido
    assert _techo(_medida(equity="0.93")) == "no_gana"  # e) incumplido
    assert _techo(_medida(suspendidas=("2030-01",))) == "no_gana"  # f)
    assert _techo(_medida(n=50, esperanza="-0.01")) == "no_gana"  # N < 100 y esperanza < 0
    assert _techo(_medida(n=150, esperanza="0.05", alto="0.09")) == "no_gana"  # percentil alto
    assert tp.salida_de("no_gana", "ganan") == "C"


def test_salida_d() -> None:
    assert _techo(_medida(n=50, esperanza="0.05")) == "no_concluyente"
    assert tp.salida_de("no_concluyente", "ganan") == "D"
    assert _parejas(18, "0.50", "0.30", "0.40") == "no_concluyente"  # N < 19, sin mirar mas
    assert tp.salida_de("gana", "no_concluyente") == "D"
    assert _parejas(25, "0.05", "0.01", "0.10") == "ni_una_cosa_ni_otra"
    assert tp.salida_de("gana", "ni_una_cosa_ni_otra") == "D"


def test_las_fronteras_rompen_en_el_otro_sentido() -> None:
    """Un percentil 5 de 0 no gana (tiene que ser mayor), y una esperanza de 0,10 si."""
    assert _techo(_medida(bajo="0")) == "no_concluyente"
    assert _techo(_medida(esperanza="0.10")) == "gana"
    assert _techo(_medida(esperanza="0.099")) == "no_concluyente"
    assert _parejas(19, "0.10", "0.001", "0.10") == "ganan"
    assert _parejas(25, "-0.01", "-0.30", "0") == "ni_una_cosa_ni_otra"  # alto de la dif. = 0


# --------------------------------------------------------------------------- el control


def _fila(neto: str = "-100.00") -> tp.FilaControl:
    return tp.FilaControl("o1", "1.00", "stop", "2030-01-02T10:00:59.999000+00:00", neto)


def test_el_control_pasa_con_las_mismas_posiciones() -> None:
    assert (
        tp.comparar_control({("2030-01-02", "o1"): _fila()}, {("2030-01-02", "o1"): _fila()}) == []
    )


def test_el_control_falla_con_un_centimo() -> None:
    dif = tp.comparar_control(
        {("2030-01-02", "o1"): _fila("-100.00")}, {("2030-01-02", "o1"): _fila("-100.01")}
    )
    assert dif == ["2030-01-02 o1: neto -100.00 frente a -100.01"]


def test_el_control_falla_si_falta_o_sobra_una() -> None:
    assert tp.comparar_control({("2030-01-02", "o1"): _fila()}, {}) == [
        "2030-01-02 o1: la repeticion no la llena"
    ]
    assert tp.comparar_control({}, {("2030-01-02", "o1"): _fila()}) == [
        "2030-01-02 o1: la repeticion llena una que el motor no"
    ]


# ------------------------------------------------------------- el remuestreo, a mano


def test_un_solo_dia_da_la_media_de_sus_diferencias() -> None:
    p, descartadas = tp.percentil_de_diferencias(
        [("2030-01-02", D(2)), ("2030-01-02", D(4))], ["2030-01-02"], replicas=7, semilla=1,
        percentil=95,
    )  # fmt: skip
    assert (p, descartadas) == (D(3), 0)


def test_tres_dias_como_la_cuenta_a_mano() -> None:
    dias = ["2030-01-02", "2030-01-03", "2030-01-04"]
    difs = [("2030-01-02", D(1)), ("2030-01-03", D(3)), ("2030-01-03", D(5))]
    # a mano: cada replica sortea tres dias con reemplazo y agrupa sus diferencias
    sumas = {"2030-01-02": (D(1), 1), "2030-01-03": (D(8), 2), "2030-01-04": (D(0), 0)}
    azar = random.Random(20261107)
    medias = []
    for _ in range(50):
        t, k = D(0), 0
        for _ in dias:
            s, c = sumas[dias[azar.randrange(3)]]
            t, k = t + s, k + c
        if k:
            medias.append(t / k)
    medias.sort()
    for percentil in (5, 95):
        p, _ = tp.percentil_de_diferencias(
            difs, dias, replicas=50, semilla=20261107, percentil=percentil
        )
        assert p == medias[(percentil * (len(medias) - 1)) // 100]


# ------------------------------------------------------------------- las piezas del modelo


def test_la_caja_del_trader_y_su_objetivo() -> None:
    assert tp.caja_derivada(10, D("0.8"), ROUND_UP) == 13  # 12,5 alejandose de la entrada
    assert tp.caja_derivada(8, D("0.8"), ROUND_UP) == 10
    assert tp.objetivo_de(117206, "compra", 13, D(3)) == 117245
    assert tp.objetivo_de(117206, "venta", 13, D(3)) == 117167


def test_el_lote_del_riesgo() -> None:
    # 0,5 % de 100.000 = 500 USD; 10 puntos de escala 100.000 con contrato 100.000 = 10 USD/lote
    assert tp.lote_del_riesgo(D(100000), D("0.5"), 10, 100000, D(100000), D("0.01")) == D("50.00")
    assert tp.lote_del_riesgo(D(100000), D("0.5"), 19, 100000, D(100000), D("0.01")) == D("26.31")


def test_un_precio_fuera_del_punto_rompe() -> None:
    assert tp.a_puntos(D("1.17206"), 100000) == 117206
    try:
        tp.a_puntos(D("1.172065"), 100000)
    except ValueError:
        return
    raise AssertionError("un precio fuera del punto tenia que romper")


def test_la_salida_del_pivote() -> None:
    assert tp.salida_del_pivote(10, 20, 19, 33) == "se_cumple_uno"
    assert tp.salida_del_pivote(19, 33, 19, 33) == "se_cumplen_los_dos"
    assert tp.salida_del_pivote(18, 34, 19, 33) == "no_se_cumple_ninguno"
