"""El criterio de fidelidad en desarrollo (ADR-0043), SIN motor: solo operaciones sinteticas."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

from botsito.cases.criterio_fidelidad import (
    Operacion,
    Tolerancias,
    cargar_criterio,
    emparejar,
    medir,
)

REPO = Path(__file__).resolve().parents[2]
TOL = Tolerancias(entrada_puntos=3, instante_min=15, escala=100000)
T0 = datetime(2030, 1, 7, 9, 0, 0, tzinfo=UTC)


def op(
    minutos: float = 0,
    entrada: str = "1.10000",
    direccion: str = "venta",
    dia: str = "2030-01-07",
    sesion: str = "07-11",
) -> Operacion:
    return Operacion(dia, sesion, direccion, T0 + timedelta(minutes=minutos), Decimal(entrada))


def test_emparejamiento_exacto() -> None:
    m = medir([op()], [op()], TOL)
    assert len(m.parejas) == 1
    assert m.cobertura == 1 and m.precision == 1
    assert m.mismo_minuto == 1
    assert m.delta_instante_min == {0: 1} and m.delta_entrada_puntos == {Decimal(0): 1}


def test_fuera_de_tolerancia_de_entrada() -> None:
    assert len(emparejar([op()], [op(entrada="1.10003")], TOL)) == 1  # 3 puntos: dentro
    m = medir([op()], [op(entrada="1.10004")], TOL)  # 4 puntos: fuera
    assert m.parejas == () and m.cobertura == 0 and m.precision == 0


def test_fuera_de_tolerancia_de_tiempo() -> None:
    assert len(emparejar([op()], [op(minutos=15)], TOL)) == 1  # 15 min: dentro
    assert emparejar([op()], [op(minutos=15.5)], TOL) == ()  # mas de 15: fuera


def test_direccion_contraria_no_empareja() -> None:
    assert emparejar([op(direccion="venta")], [op(direccion="compra")], TOL) == ()


def test_otra_sesion_u_otro_dia_no_empareja() -> None:
    assert emparejar([op()], [op(sesion="11-15")], TOL) == ()
    assert emparejar([op()], [op(dia="2030-01-08")], TOL) == ()


def test_dos_candidatas_gana_la_de_menor_delta_instante() -> None:
    trader = [op(minutos=0)]
    lejos, cerca = op(minutos=10), op(minutos=2)
    (p,) = emparejar(trader, [lejos, cerca], TOL)
    assert p.bot == cerca


def test_empate_en_instante_gana_la_de_menor_delta_entrada_y_luego_la_mas_temprana() -> None:
    trader = [op(minutos=5)]
    a, b = op(minutos=3, entrada="1.10002"), op(minutos=7, entrada="1.10001")
    (p,) = emparejar(trader, [a, b], TOL)
    assert p.bot == b  # mismo |Δinstante| (2 min): gana la de menor |Δentrada|
    c, d = op(minutos=3, entrada="1.10001"), op(minutos=7, entrada="1.10001")
    (p,) = emparejar(trader, [d, c], TOL)
    assert p.bot == c  # empate en todo: la mas temprana, sea cual sea el orden de entrada


def test_uno_a_uno_no_reutiliza_una_operacion() -> None:
    trader = [op(minutos=0), op(minutos=1)]
    bot = [op(minutos=0)]
    m = medir(trader, bot, TOL)
    assert len(m.parejas) == 1 and m.cobertura == Fraction(1, 2) and m.precision == 1


def test_una_operacion_del_bot_en_un_dia_sin_trader_se_informa_aparte_y_no_puntua() -> None:
    trader = [op()]
    bot = [op(), op(dia="2030-01-08")]
    m = medir(trader, bot, TOL)
    assert m.n_bot_fuera == 1 and m.n_bot_puntuables == 1
    assert m.precision == 1  # la del dia sin trader no cuenta


def test_cero_operaciones_del_bot_cobertura_cero_y_precision_sin_definir() -> None:
    m = medir([op(), op(minutos=30)], [], TOL)
    assert m.cobertura == 0
    assert m.precision is None  # sin dividir por cero


def test_cero_operaciones_del_trader_cobertura_sin_definir() -> None:
    m = medir([], [op()], TOL)
    assert m.cobertura is None and m.n_bot_fuera == 1 and m.precision is None


def test_el_fichero_del_criterio_dice_lo_que_dice_adr_0043() -> None:
    c = cargar_criterio(REPO)
    assert (c.tolerancias.entrada_puntos, c.tolerancias.instante_min) == (3, 15)
    assert (c.umbral_cobertura, c.umbral_precision) == (Fraction(7, 10), Fraction(6, 10))
    assert c.construccion == ("2026-04", "2026-08") and c.medida == ("2026-05",)
