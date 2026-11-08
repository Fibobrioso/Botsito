"""El metodo de ADR-0092, todo SINTETICO: la cascada de la fidelidad por criterios (§1 y §2), la
rentabilidad (§3), el deslizamiento pendiente de F17 (§4) y la salida del arnes, que solo se
ANADE al final del informe de la simulacion: lo que ya salia no cambia, y el emparejamiento por
operacion de ADR-0043 da lo mismo con el stop del caso que sin el. Ninguna corrida del arnes: el
motor corre sobre el dia sintetico de 2030 de `test_cableado.py`."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from botsito.cases.criterio_fidelidad import (
    COMPLETA,
    ENTRADA_FUERA,
    INSUFICIENTE,
    LLENADA_FUERA,
    NO_LLENADA,
    NO_PASA,
    PASA,
    PENDIENTE_F17,
    SIN_ORDEN,
    SIN_STOP,
    STOP_FUERA,
    CriterioError,
    CriterioRentabilidad,
    MedidaRentabilidad,
    Operacion,
    OrdenCriterio,
    PosicionCerrada,
    Tolerancias,
    cargar_criterio,
    cascada_por_criterios,
    cascada_por_mes,
    con_deslizamiento,
    curva_con_deslizamiento,
    equity_minima_del_tramo,
    esperanza_r,
    medir,
    medir_rentabilidad,
    percentil_por_dias,
    perdida_diaria_maxima,
    punto_de_equilibrio,
    r_neto,
    veredicto_con_f17,
    veredicto_rentabilidad,
)
from botsito.config.registro import Registro, cargar_registro
from botsito.engine import arnes, cableado
from botsito.engine.cuenta import EstadoCuenta
from botsito.engine.primitivas_broker import SALTO_EL_STOP
from botsito.spec.modelo import cargar_vocabulario
from tests.unit.test_cableado import (
    ENTRADA,
    RUTA_HUECO,
    RUTA_STOP,
    RUTA_VIVA,
    SPEC,
    _dia,
    _mercado,
    _motor,
)

REPO = Path(__file__).resolve().parents[2]
TOL = Tolerancias(entrada_puntos=3, instante_min=15, escala=100_000)
T0 = datetime(2030, 1, 15, 8, 0, tzinfo=UTC)
CRITERIO_REAL = cargar_criterio(REPO)


def _rentabilidad_real() -> CriterioRentabilidad:
    r = CRITERIO_REAL.rentabilidad
    assert r is not None
    return r


RENT = _rentabilidad_real()


def _t(
    entrada: str = "1.10000", stop: str | None = "1.09980", minutos: int = 0, sesion: str = "07-11"
) -> Operacion:
    return Operacion(
        "2030-01-15",
        sesion,
        "compra",
        T0 + timedelta(minutes=minutos),
        Decimal(entrada),
        Decimal(stop) if stop is not None else None,
    )


def _o(
    entrada: str = "1.10000",
    stop: str = "1.09980",
    colocada: int = -5,
    llenado: int | None = 0,
    sesion: str = "07-11",
    direccion: str = "compra",
) -> OrdenCriterio:
    return OrdenCriterio(
        "2030-01-15",
        sesion,
        direccion,
        T0 + timedelta(minutes=colocada),
        Decimal(entrada),
        Decimal(stop),
        T0 + timedelta(minutes=llenado) if llenado is not None else None,
    )


# ------------------------------------------------------------------------- la cascada (§2)


@pytest.mark.parametrize(
    ("orden", "trader", "escalon"),
    [
        (None, _t(), SIN_ORDEN),
        (_o(direccion="venta"), _t(), SIN_ORDEN),  # otra direccion no cuenta
        (_o(sesion="11-15"), _t(), SIN_ORDEN),  # otra sesion tampoco
        (_o(entrada="1.10004"), _t(), ENTRADA_FUERA),  # 4 puntos
        (_o(entrada="1.10003", stop="1.09976"), _t(), STOP_FUERA),  # entrada 3, stop 4
        (_o(entrada="1.10003"), _t(stop=None), SIN_STOP),
        (_o(entrada="1.10003", stop="1.09983", llenado=None), _t(), NO_LLENADA),
        (_o(llenado=16), _t(), LLENADA_FUERA),
        (_o(entrada="1.10003", stop="1.09977", llenado=15), _t(), COMPLETA),  # todo en el borde
    ],
)
def test_cada_operacion_del_trader_cae_en_el_ultimo_escalon_que_alcanza(
    orden: OrdenCriterio | None, trader: Operacion, escalon: str
) -> None:
    cascada = cascada_por_criterios([trader], [orden] if orden else [], TOL, 3)
    assert [p.escalon for p in cascada.pasos] == [escalon]


def test_se_toma_la_orden_mas_cercana_en_entrada_y_a_igualdad_la_de_colocacion_mas_cercana() -> (
    None
):
    lejos = _o(entrada="1.10010", colocada=0)
    cerca_tarde = _o(entrada="1.10001", colocada=-30, llenado=None)
    cerca_pronto = _o(entrada="1.09999", colocada=-2)
    cascada = cascada_por_criterios([_t()], [lejos, cerca_tarde, cerca_pronto], TOL, 3)
    assert cascada.pasos[0].orden == cerca_pronto
    assert cascada.pasos[0].escalon == COMPLETA


def test_las_ordenes_sin_trader_se_cuentan_aparte_y_por_mes_sale_el_total() -> None:
    sueltas = [_o(sesion="11-15"), _o(direccion="venta"), _o()]
    cascada = cascada_por_criterios([_t(), _t(minutos=60, entrada="1.20000")], sueltas, TOL, 3)
    assert cascada.ordenes_sin_trader == 2
    por_mes = cascada_por_mes(cascada)
    assert por_mes["2030-01"] == por_mes["total"]
    assert por_mes["total"][COMPLETA] == 1 and por_mes["total"][ENTRADA_FUERA] == 1


def test_el_emparejamiento_por_operacion_da_lo_mismo_con_el_stop_que_sin_el() -> None:
    bot = [
        Operacion("2030-01-15", "07-11", "compra", T0 + timedelta(minutes=1), Decimal("1.10001"))
    ]
    con = medir([_t()], bot, TOL)
    sin = medir([_t(stop=None)], bot, TOL)
    assert (con.cobertura, con.precision, con.mismo_minuto) == (
        sin.cobertura,
        sin.precision,
        sin.mismo_minuto,
    )
    assert len(con.parejas) == len(sin.parejas) == 1


def test_el_arnes_lleva_el_stop_del_caso_y_un_caso_sin_stop_queda_en_none() -> None:
    op = {"sesion": "07-11", "direccion": "venta", "instante_utc": T0.isoformat(), "entrada": 1.1}
    assert arnes._operacion("2030-01-15", {**op, "stop": 1.10016}).stop == Decimal("1.10016")
    assert arnes._operacion("2030-01-15", op).stop is None


# ----------------------------------------------------------------------- rentabilidad (§3)

VALOR_PUNTO = Decimal(1)  # contrato 100.000 / escala 100.000


def _p(
    dia: str, neto: str, riesgo: str = "100", stop: bool = True, cierre: str = "stop"
) -> PosicionCerrada:
    return PosicionCerrada(
        dia, Decimal(neto), Decimal(riesgo), stop, cierre, Decimal(1), VALOR_PUNTO
    )


def test_r_neto_y_esperanza() -> None:
    ps = [_p("d1", "300"), _p("d1", "-100"), _p("d2", "-50", "50")]
    assert [r_neto(p) for p in ps] == [Decimal(3), Decimal(-1), Decimal(-1)]
    assert esperanza_r(ps) == Decimal(1) / 3
    assert esperanza_r([]) is None
    with pytest.raises(CriterioError):
        r_neto(_p("d1", "10", "0"))


def test_el_remuestreo_por_dias_es_determinista_y_da_la_media_si_todos_los_dias_son_iguales() -> (
    None
):
    dias = ["d1", "d2", "d3"]
    iguales = [_p(d, "50") for d in dias]
    assert percentil_por_dias(iguales, dias, replicas=200, semilla=7, percentil=5) == Decimal("0.5")
    mezcla = [_p("d1", "300"), _p("d2", "-100"), _p("d3", "-100"), _p("d3", "50")]
    uno = percentil_por_dias(mezcla, [*dias, "d4"], replicas=500, semilla=20261107, percentil=5)
    otro = percentil_por_dias(mezcla, [*dias, "d4"], replicas=500, semilla=20261107, percentil=5)
    assert uno == otro and uno is not None
    # el percentil 5 queda por debajo de la media de la muestra, el 95 por encima
    p95 = percentil_por_dias(mezcla, [*dias, "d4"], replicas=500, semilla=20261107, percentil=95)
    assert p95 is not None and uno < esperanza_r(mezcla) < p95  # type: ignore[operator]
    with pytest.raises(CriterioError):
        percentil_por_dias([_p("d9", "1")], dias, replicas=10, semilla=1, percentil=5)


CAPITAL = Decimal(100_000)
DiaCurva = tuple[str, Decimal, Decimal, Decimal | None]
CURVA: list[DiaCurva] = [
    ("d1", Decimal(100_000), Decimal(99_000), Decimal(98_500)),  # pierde 1.500 en el dia
    ("d2", Decimal(99_000), Decimal(99_000), None),  # sin posicion
    ("d3", Decimal(99_000), Decimal(101_000), Decimal(96_000)),  # pierde 3.000 desde el corte
]


def test_la_perdida_diaria_y_la_equity_minima_salen_de_la_curva() -> None:
    assert perdida_diaria_maxima(CURVA, CAPITAL, "saldo_corte_diario") == Fraction(3, 100)
    # con la base en el capital, la del dia 3 cuenta desde 100.000: 4.000
    assert perdida_diaria_maxima(CURVA, CAPITAL, "saldo_inicial_cuenta") == Fraction(4, 100)
    assert equity_minima_del_tramo(CURVA, CAPITAL) == Fraction(96, 100)
    with pytest.raises(CriterioError):
        perdida_diaria_maxima(CURVA, CAPITAL, "otra")


CURVA_SIN_PERDIDA = CURVA[:2]  # el dia 1 pierde el 1,5 %; la equity no baja del 98,5 %
CURVA_E: list[DiaCurva] = [("d1", Decimal(100_000), Decimal(99_000), Decimal(93_500))]  # al 93,5 %


def _medida(
    n: int,
    neto: str = "50",
    curva: list[DiaCurva] = CURVA_SIN_PERDIDA,
    suspendida: bool = False,
) -> MedidaRentabilidad:
    ps = [_p("d1", neto) for _ in range(n)]
    dias = ["d1", "d2"]
    return medir_rentabilidad(ps, dias, curva, CAPITAL, "saldo_corte_diario", suspendida, RENT)


def test_sin_n_es_insuficiente_y_con_todo_es_pendiente_de_f17() -> None:
    poca = _medida(RENT.n_minimo - 1)
    assert veredicto_rentabilidad(poca, RENT).estado == INSUFICIENTE
    buena = _medida(RENT.n_minimo)
    v = veredicto_rentabilidad(buena, RENT)
    assert v.estado == PENDIENTE_F17, v
    # con el deslizamiento medido, la misma medida pasa
    assert veredicto_rentabilidad(buena, RENT, deslizamiento_medido=True).estado == PASA


@pytest.mark.parametrize(
    ("neto", "curva", "suspendida", "letra"),
    [
        ("5", CURVA_SIN_PERDIDA, False, "b)"),  # 0,05 R de esperanza
        ("-50", CURVA_SIN_PERDIDA, False, "c)"),  # y tambien b)
        ("50", CURVA, False, "d)"),  # el dia 3 pierde el 3 % desde su corte: llega al 3 %
        ("50", CURVA_E, False, "e)"),  # la equity baja al 93,5 %, por debajo del 94 %
        ("50", CURVA_SIN_PERDIDA, True, "f)"),
    ],
)
def test_cada_criterio_que_falta_da_no_pasa_con_su_motivo(
    neto: str, curva: list[DiaCurva], suspendida: bool, letra: str
) -> None:
    v = veredicto_rentabilidad(_medida(RENT.n_minimo, neto, curva, suspendida), RENT)
    assert v.estado == NO_PASA and any(m.startswith(letra) for m in v.motivos), v


def test_la_equity_al_96_por_ciento_cumple_e() -> None:
    v = veredicto_rentabilidad(_medida(RENT.n_minimo, "50", CURVA), RENT)
    assert not any(m.startswith("e)") for m in v.motivos)


def test_el_deslizamiento_se_resta_a_cada_llenado_afectado_sin_tocar_los_objetivos() -> None:
    entrada_stop_y_stop = _p("d1", "100")  # dos llenados afectados
    limite_y_objetivo = _p("d1", "300", stop=False, cierre="objetivo")  # ninguno
    limite_y_manual = _p("d1", "0", stop=False, cierre="manual")  # uno
    assert con_deslizamiento(entrada_stop_y_stop, Decimal(2)).pnl_neto == Decimal(96)
    assert con_deslizamiento(limite_y_objetivo, Decimal(2)).pnl_neto == Decimal(300)
    assert con_deslizamiento(limite_y_manual, Decimal(2)).pnl_neto == Decimal(-2)


def test_la_curva_se_recompone_sumando_el_ajuste_al_dia_de_cada_cierre() -> None:
    curva = [
        ("d1", Decimal(100), Decimal(90), Decimal(80)),
        ("d2", Decimal(90), Decimal(95), None),
    ]
    ps = [_p("d1", "-10")]  # dos llenados afectados: -4 con 2 puntos y 1 lote de 1 USD/punto
    assert curva_con_deslizamiento(curva, ps, Decimal(2)) == [
        ("d1", Decimal(100), Decimal(86), Decimal(76)),
        ("d2", Decimal(86), Decimal(91), None),
    ]


def test_el_punto_de_equilibrio_lleva_la_esperanza_al_objetivo() -> None:
    ps = [_p("d1", "50"), _p("d2", "10")]  # R 0,5 y 0,1: media 0,3
    s = punto_de_equilibrio(ps, Decimal("0.10"))
    assert s is not None
    assert esperanza_r([con_deslizamiento(p, s) for p in ps]) == Decimal("0.10")
    assert punto_de_equilibrio([_p("d1", "5", stop=False, cierre="objetivo")], Decimal(0)) is None


def test_con_f17_se_reevalua_con_la_mediana_y_el_percentil_tiene_que_dejar_esperanza_positiva() -> (
    None
):
    ps = [_p("d1", "50") for _ in range(RENT.n_minimo)]

    def con(mediana: int, percentil: int) -> tuple[str, ...]:
        v = veredicto_con_f17(
            ps,
            ["d1", "d2"],
            CURVA_SIN_PERDIDA,
            CAPITAL,
            "saldo_corte_diario",
            False,
            RENT,
            mediana=Decimal(mediana),
            percentil_f17=Decimal(percentil),
        )
        return (v.estado, *(m[:2] for m in v.motivos))

    assert con(1, 5) == (PASA,)
    # con 30 puntos de p90 por llenado (dos por operacion) la esperanza baja de 0,5 a -0,1
    assert con(1, 30) == (NO_PASA, "la")
    # con 20 de mediana la esperanza queda en 0,1 y llega justo a b); pero la curva recompuesta
    # resta 40 USD por operacion al dia 1 (4.000 en total): de 98.500 a 94.500 de equity minima,
    # el 5,5 % del capital desde el corte, y d) ya no se cumple. Con 21, tampoco b) (0,08 R), y
    # la esperanza con ese percentil sigue positiva: esa condicion se cumple
    assert con(20, 20) == (NO_PASA, "d)")
    assert con(21, 21) == (NO_PASA, "b)", "d)")


# -------------------------------------------- la salida del arnes: solo se ANADE al final


@pytest.fixture(scope="module")
def registro() -> Registro:
    return cargar_registro(REPO / "knowledge" / "spec" / "parametros.yaml")


@pytest.fixture(scope="module")
def vocabulario() -> dict[str, dict[str, Any]]:
    return cargar_vocabulario(SPEC)


def _corrido(registro: Registro, vocabulario: dict[str, dict[str, Any]]) -> cableado.MotorCableado:
    motor = _motor(registro, vocabulario, _mercado(RUTA_STOP))
    motor.correr_dia(_dia())
    return motor


GOLDEN = REPO / "tests" / "golden" / "informe_simulacion"


@pytest.mark.parametrize(
    ("nombre", "ruta"), [("hueco", RUTA_HUECO), ("stop", RUTA_STOP), ("viva", RUTA_VIVA)]
)
def test_lo_que_ya_salia_es_byte_a_byte_lo_de_main(
    registro: Registro, vocabulario: dict[str, dict[str, Any]], nombre: str, ruta: Any
) -> None:
    """Contra la salida de `main` (e01e28c) CONGELADA en `tests/golden/informe_simulacion/`: la
    misma corrida sintetica, con el codigo de la rama, da exactamente lo de `main` hasta la seccion
    de ADR-0092, que va despues. Un cambio de decision o de llenado en el dia sintetico cambiaria
    las ordenes, los eventos o la curva, y este test lo veria (revisor de la rama, b4)."""
    motor = _motor(registro, vocabulario, _mercado(ruta))
    motor.correr_dia(_dia())
    texto = cableado.informe_simulacion(motor)
    de_main = (GOLDEN / f"main-{nombre}.txt").read_text(encoding="utf-8")
    assert cableado.CABECERA_METODO not in de_main
    assert texto.startswith(de_main)
    assert texto[len(de_main) :].startswith("\n" + cableado.CABECERA_METODO)


def test_la_seccion_nueva_va_al_final_y_lo_que_ya_salia_no_cambia(
    registro: Registro, vocabulario: dict[str, dict[str, Any]], monkeypatch: pytest.MonkeyPatch
) -> None:
    motor = _corrido(registro, vocabulario)
    con = cableado.informe_simulacion(motor)
    monkeypatch.setattr(cableado, "_informe_metodo", lambda _m: [])
    sin = cableado.informe_simulacion(motor)
    assert con.startswith(sin.rstrip("\n") + "\n")
    nuevo = con[len(sin.rstrip("\n")) + 1 :]
    assert nuevo.lstrip("\n").startswith(cableado.CABECERA_METODO)
    assert cableado.CABECERA_METODO not in sin


def test_la_tabla_de_posiciones_cuadra_con_la_cuenta(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    motor = _corrido(registro, vocabulario)
    filas = cableado.posiciones_del_bot(motor)
    assert len(filas) == 1
    f = filas[0]
    assert (f.cierre, f.desenlace, f.lado) == ("stop", SALTO_EL_STOP, "compra")
    # se llena en la entrada y salta el stop un punto por debajo de su nivel: 17 puntos
    assert f.entrada == Decimal(ENTRADA) / 100_000
    assert f.bruto == -Decimal(17) * f.lotes
    assert f.riesgo == Decimal(16) * f.lotes  # lote x distancia al stop (16 puntos) x 1 USD
    # lo que la tabla dice que se gano es lo que la cuenta cambio
    assert motor.cuenta is not None
    assert f.neto == motor.cuenta.saldo - motor.reglas_fase.capital_inicial
    assert f.neto == f.bruto - f.comision - f.swaps
    assert r_neto(f.posicion) == f.neto / f.riesgo


def test_sin_criterio_la_seccion_lo_dice_y_con_el_saca_cascada_y_rentabilidad(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    motor = _corrido(registro, vocabulario)
    assert "sin el criterio de ADR-0092" in cableado.informe_simulacion(motor)
    p = cableado.posiciones_del_bot(motor)[0]
    o = cableado.ordenes_para_la_cascada(motor)[0]
    motor.criterio = CRITERIO_REAL
    motor.operaciones_trader = (Operacion(p.dia, p.sesion, "compra", p.llenada, o.entrada, o.stop),)
    texto = cableado.informe_simulacion(motor)
    fila_total = next(x for x in texto.splitlines() if x.startswith("total | "))
    # una operacion del trader con la misma entrada, el mismo stop y el mismo llenado: COMPLETA
    assert fila_total.split(" | ")[-2:] == ["1", "1"]
    assert "### Rentabilidad (ADR-0092 §3; DIAGNOSTICO" in texto
    assert "a) N (operaciones llenadas y cerradas): 1" in texto
    assert f"criterios a) a f): {INSUFICIENTE}" in texto
    assert motor.veredicto()[0] is EstadoCuenta.EN_CURSO
