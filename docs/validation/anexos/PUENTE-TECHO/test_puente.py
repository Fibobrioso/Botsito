"""Tests de humo de `puente.py`, sobre datos sinteticos (fechas de 2030), en los dos sentidos.

`make check` no los recoge (`testpaths = ["tests"]`). Desde la raiz:
    uv run pytest docs/validation/anexos/PUENTE-TECHO/test_puente.py -p no:cacheprovider

Cubren lo que pide el encargo (fase 1): cada pieza cambia lo que dice y solo eso (el objetivo con
una base y con la otra; el break even que se mueve y que no; la operacion de mas de 100 lotes que
entra y que sale; el desfase; el ASK con k = 1, k = 2 y sin spread, sin cruzar nunca el BID; el
stop al 0,8; RN-002 con y sin el cierre de la H4); D2 c, la misma operacion por orden stop y por
`abrir_conocida` con el mismo riesgo y el mismo R; las tres lecturas por el R y las tres del
puente, con sus fronteras; y el cierre que cierra y que no cierra. Las cifras se leen de los yaml.
"""

from __future__ import annotations

import sys
from datetime import UTC, datetime
from decimal import ROUND_UP, Decimal
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))

import puente as pt  # noqa: E402

from botsito.comun.yaml_estricto import leer_yaml  # noqa: E402
from botsito.data.velas import a_minuto  # noqa: E402
from botsito.domain.ticks import MS_POR_MINUTO, MilisegundoUtc, Tick  # noqa: E402
from botsito.domain.valores import Puntos  # noqa: E402
from botsito.domain.velas import MinutoUtc, Vela  # noqa: E402
from botsito.engine.broker import Broker, ReglasBroker  # noqa: E402
from botsito.engine.cableado import posiciones_del_bot  # noqa: E402
from botsito.engine.llenado import Configuracion, Mercado  # noqa: E402

tp = pt.tp
PUENTE = leer_yaml(pt.RAIZ / "docs" / "plan" / "PUENTE-TECHO.yaml")
META = leer_yaml(pt.RAIZ / "docs" / "plan" / "META-TECHO-PAREJAS.yaml")
PROPIOS = PUENTE["propios"]
ORDEN_R = list(PUENTE["lectura_por_el_r"]["orden"])
ORDEN_PUENTE = list(PUENTE["lecturas_del_puente"]["orden"])
ALTO_MIN = Decimal(META["propios"]["techo_no_gana_si_percentil_alto_por_debajo_de_r"])
D = Decimal
OCHO = D("0.8")
NOMBRES = pt.nombres_de_las_piezas(PROPIOS)


def _p(*nombres: str) -> pt.Piezas:
    return pt.piezas_de(list(nombres), PROPIOS)


# ------------------------------------------------------------------------ las piezas


def test_las_piezas_del_yaml_son_las_del_guion() -> None:
    assert tuple(PUENTE["piezas"]) == NOMBRES
    assert pt.piezas_de([], PROPIOS) == pt.Piezas()


def test_una_pieza_desconocida_rompe() -> None:
    try:
        pt.piezas_de(["sin_comision"], PROPIOS)
    except ValueError as exc:
        assert "sin_comision" in str(exc)
    else:
        raise AssertionError("una pieza desconocida tiene que romper")


def test_el_objetivo_con_una_base_y_con_la_otra() -> None:
    # stop del caso a 12 puntos: caja derivada ceil(12 / 0,8) = 15; objetivo a 45 o a 36
    n = pt.niveles_del_caso(1000, 988, "compra", pt.Piezas(), OCHO, ROUND_UP)
    assert (n.entrada, n.stop, n.caja, n.base_stop) == (1000, 988, 15, 12)
    assert pt.base_del_objetivo(n, pt.Piezas(), "caja_completa") == 15
    assert pt.base_del_objetivo(n, _p("objetivo_sobre_el_stop"), "caja_completa") == 12
    assert tp.objetivo_de(1000, "compra", 15, D(3)) == 1045
    assert tp.objetivo_de(1000, "compra", 12, D(3)) == 1036
    # la pieza no toca el stop ni la caja
    m = pt.niveles_del_caso(1000, 988, "compra", _p("objetivo_sobre_el_stop"), OCHO, ROUND_UP)
    assert (m.stop, m.caja) == (n.stop, n.caja)


def test_el_desfase_baja_entrada_y_stop_en_los_dos_lados() -> None:
    k = int(PROPIOS["desfase_puntos"])
    pz = _p(NOMBRES[4])
    compra = pt.niveles_del_caso(1000, 988, "compra", pz, OCHO, ROUND_UP)
    venta = pt.niveles_del_caso(1000, 1012, "venta", pz, OCHO, ROUND_UP)
    assert (compra.entrada, compra.stop) == (1000 - k, 988 - k)
    assert (venta.entrada, venta.stop) == (1000 - k, 1012 - k)
    assert compra.caja == venta.caja == 15  # la distancia no cambia
    sin = pt.niveles_del_caso(1000, 988, "compra", pt.Piezas(), OCHO, ROUND_UP)
    assert (sin.entrada, sin.stop) == (1000, 988)


def test_el_stop_al_08_como_niveles() -> None:
    pz = _p("stop_en_el_08")
    compra = pt.niveles_del_caso(1000, 988, "compra", pz, OCHO, ROUND_UP)
    venta = pt.niveles_del_caso(1000, 1013, "venta", pz, OCHO, ROUND_UP)
    assert compra.stop == 1000 - 10  # 0,8 x 12 = 9,6 -> 10, al mas cercano
    assert venta.stop == 1000 + 10  # 0,8 x 13 = 10,4 -> 10
    # el objetivo no cambia: su base sigue saliendo del stop del caso
    assert (compra.caja, compra.base_stop) == (15, 12)
    assert pt.base_del_objetivo(compra, _p("stop_en_el_08", "objetivo_sobre_el_stop"), "x") == 12
    assert pt.niveles_del_caso(1000, 988, "compra", pt.Piezas(), OCHO, ROUND_UP).stop == 988


def test_el_tope_de_lotes_entra_y_sale() -> None:
    tope = pt.piezas_de([NOMBRES[3]], PROPIOS).tope_lotes
    assert tope == D(PROPIOS["lotes_fuera_si_el_lote_por_riesgo_pasa_de"])
    assert not pt.fuera_por_el_tope(tope, tope)
    assert pt.fuera_por_el_tope(tope + D("0.01"), tope)
    assert not pt.fuera_por_el_tope(tope + D(500), None)


def test_el_ask_con_k_1_con_k_2_y_sin_spread() -> None:
    k0, k1 = (int(k) for k in PROPIOS["spread_menos_puntos"])
    assert _p(NOMBRES[5]).spread == k0 and _p(NOMBRES[6]).spread == k1
    assert _p("sin_spread").spread is None and pt.Piezas().spread == 0
    assert pt.ask_con_spread(1004, 1000, k0) == 1004 - k0
    assert pt.ask_con_spread(1004, 1000, k1) == 1004 - k1
    assert pt.ask_con_spread(1004, 1000, None) == 1000
    assert pt.ask_con_spread(1001, 1000, k1) == 1000  # nunca cruza el BID
    assert pt.ask_con_spread(1000, 1000, k0) == 1000
    ticks = [Tick(MilisegundoUtc(1), Puntos(1004), Puntos(1000), 5, 6)]
    t = pt.ticks_con_spread(ticks, k1)[0]
    assert (t.ask, t.bid, t.volumen_ask, t.volumen_bid) == (1004 - k1, 1000, 5, 6)
    try:
        pt.piezas_de([NOMBRES[5], "sin_spread"], PROPIOS)
    except ValueError:
        pass
    else:
        raise AssertionError("dos piezas de spread a la vez tienen que romper")


# -------------------------------------------------- un mercado sintetico para el bucle

HUSO = ZoneInfo("America/New_York")
M0 = int(a_minuto(datetime(2030, 1, 15, 8, 0, tzinfo=UTC)))
SPREAD = 2


def _ms(minuto: int, segundo: int = 0) -> int:
    return minuto * MS_POR_MINUTO + segundo * 1000


def _reglas() -> ReglasBroker:
    return ReglasBroker(
        volumen_max_lotes=D(10),
        ordenes_simultaneas_max=3,
        posiciones_dia_max=2,
        huso_corte=HUSO,
        comision_por_lote=D(2),
        comision_por_lado=True,
        swap_largo_puntos=D(0),
        swap_corto_puntos=D(0),
        stops_level_puntos=0,
    )


def _mercado(bids: list[int]) -> Mercado:
    ticks = [
        Tick(MilisegundoUtc(_ms(M0 + i, 30)), Puntos(b + SPREAD), Puntos(b), 0, 0)
        for i, b in enumerate(bids)
    ]
    velas = [Vela(MinutoUtc(M0 + i), Puntos(b), Puntos(b), Puntos(b), Puntos(b), 1) for i, b in
             enumerate(bids)]  # fmt: skip
    return Mercado(ticks, velas)


def _rep(broker: Broker) -> pt.Repeticion:
    tb = tp.Traza((("s", M0, M0 + 100),))
    return pt.Repeticion({"2030-01-15": broker}, {"2030-01-15": tb}, [], pt.Recuentos(), D(1),
                         _reglas(), None)  # fmt: skip


def test_d2c_la_misma_operacion_por_orden_stop_y_por_abrir_conocida() -> None:
    # compra stop en 1002 (ASK = BID + 2): el tick del minuto 1 la llena a 1002; el del 3 da el
    # objetivo (1030) al BID
    bids = [990, 1000, 1010, 1031, 1031]
    a = Broker(_reglas(), Configuracion(False, 0, lambda _m: SPREAD), _mercado(bids), D(1), 1)
    a.colocar_stop("o1", "compra", 1002, D(3), 992, 1030, _ms(M0, 59))
    a.avanzar(_ms(M0 + 4))
    llenado = a.posiciones["pos-o1"]
    assert llenado.entrada == 1002 and llenado.motivo_cierre == "objetivo"
    b = Broker(_reglas(), Configuracion(False, 0, lambda _m: SPREAD), _mercado(bids), D(1), 1)
    b.avanzar(llenado.abierta_ms - 1)
    b.abrir_conocida("c1", "compra", 1002, D(3), 992, 1030, llenado.abierta_ms, "caso")
    b.avanzar(_ms(M0 + 4))
    fa = posiciones_del_bot(cast(Any, SimpleNamespace(
        reglas_broker=_reglas(), trazas_broker=_rep(a).trazas, brokers={"2030-01-15": a},
        contrato=D(1),
    )))  # fmt: skip
    fb = pt.filas_conocidas(_rep(b))
    assert len(fa) == 1 and len(fb) == 1
    x, y = fa[0], fb[0]
    assert (x.riesgo, x.bruto, x.neto, x.cierre, x.cerrada) == (
        y.riesgo, y.bruto, y.neto, y.cierre, y.cerrada,
    )  # fmt: skip
    assert x.riesgo == D(3) * 10 and x.bruto == D(3) * 28 and x.neto == x.bruto - 4 * 3
    # y el que rompe en el otro sentido: con otro stop, el riesgo ya no es el mismo
    c = Broker(_reglas(), Configuracion(False, 0, lambda _m: SPREAD), _mercado(bids), D(1), 1)
    c.avanzar(llenado.abierta_ms - 1)
    c.abrir_conocida("c1", "compra", 1002, D(3), 990, 1030, llenado.abierta_ms, "caso")
    c.avanzar(_ms(M0 + 4))
    assert pt.filas_conocidas(_rep(c))[0].riesgo != x.riesgo


def test_el_break_even_cerrado_se_reconoce_y_el_que_no_se_movio_no() -> None:
    bids = [990, 1000, 1010, 1001, 999]
    b = Broker(_reglas(), Configuracion(False, 0, lambda _m: SPREAD), _mercado(bids), D(1), 1)
    b.avanzar(_ms(M0 + 1, 29))
    b.abrir_conocida("c1", "compra", 1002, D(1), 992, 1030, _ms(M0 + 1, 30), "caso")
    b.avanzar(_ms(M0 + 3) - 1)
    b.mover_stop("c1", 1002, _ms(M0 + 3) - 1)  # el stop a la entrada
    b.avanzar(_ms(M0 + 5))
    f = pt.filas_conocidas(_rep(b))[0]
    assert pt.en_break_even(f) and f.cierre == "stop"
    # el mismo camino sin mover el stop: no salta (999 > 992) y se cierra a mercado; no es BE
    s = Broker(_reglas(), Configuracion(False, 0, lambda _m: SPREAD), _mercado(bids), D(1), 1)
    s.avanzar(_ms(M0 + 1, 29))
    s.abrir_conocida("c1", "compra", 1002, D(1), 992, 1030, _ms(M0 + 1, 30), "caso")
    s.cerrar_a_mercado("c1", _ms(M0 + 4, 40))
    g = pt.filas_conocidas(_rep(s))[0]
    assert g.cierre == "manual" and not pt.en_break_even(g)
    # y una que salta el stop original, sin moverlo: tampoco es BE
    bajan = [990, 1000, 1010, 991, 991]
    t = Broker(_reglas(), Configuracion(False, 0, lambda _m: SPREAD), _mercado(bajan), D(1), 1)
    t.avanzar(_ms(M0 + 1, 29))
    t.abrir_conocida("c1", "compra", 1002, D(1), 992, 1030, _ms(M0 + 1, 30), "caso")
    t.avanzar(_ms(M0 + 5))
    h = pt.filas_conocidas(_rep(t))[0]
    assert h.cierre == "stop" and not pt.en_break_even(h)


def test_la_esperanza_bruta_es_la_media_del_bruto_entre_el_riesgo() -> None:
    filas = [
        SimpleNamespace(bruto=D(30), riesgo=D(10)),
        SimpleNamespace(bruto=D(-10), riesgo=D(10)),
    ]
    assert pt.esperanza_bruta(filas) == D(1)
    assert pt.esperanza_bruta([]) is None


def test_rn002_con_y_sin_el_cierre_de_la_h4() -> None:
    from botsito.config.registro import cargar_registro

    registro = cargar_registro(pt.RAIZ / "knowledge" / "spec" / "parametros.yaml")
    entero = pt.predicado_rn002(registro, False)
    ventana = pt.predicado_rn002(registro, True)
    dia = [M0 - 8 * 60 + i for i in range(24 * 60)]  # un dia entero de 2030, minuto a minuto
    solo_h4 = [m for m in dia if entero(m) and not ventana(m)]
    assert all(entero(m) for m in dia if ventana(m))  # la ventana dispara en los dos
    assert solo_h4  # y hay minutos en que solo dispara el final de la H4
    assert any(ventana(m) for m in dia)


# ------------------------------------------------------------------------ las lecturas


def _lr(n: int, e: str, bajo: str, alto: str) -> str:
    return pt.lectura_por_el_r(n, D(e), D(bajo), D(alto), 100, D("0.10"), ALTO_MIN, ORDEN_R)


def test_las_tres_lecturas_por_el_r_y_sus_fronteras() -> None:
    assert _lr(100, "0.10", "0.01", "0.40") == "gana"
    assert _lr(99, "0.10", "0.01", "0.40") == "no_concluyente"  # N justo por debajo
    assert _lr(100, "0.0999", "0.01", "0.40") == "no_concluyente"
    assert _lr(100, "0.10", "0", "0.40") == "no_concluyente"  # el percentil 5 tiene que pasar de 0
    assert _lr(191, "-0.001", "-0.40", "0.30") == "no_gana"
    assert _lr(191, "0", "-0.40", "0.30") == "no_concluyente"  # 0 no es menor que 0
    assert _lr(191, "0.05", "-0.10", str(ALTO_MIN - D("0.001"))) == "no_gana"
    assert _lr(191, "0.05", "-0.10", str(ALTO_MIN)) == "no_concluyente"


def test_las_tres_lecturas_del_puente() -> None:
    nogana = {"a": "no_gana", "b": "no_gana"}
    una = {"a": "no_gana", "b": "no_concluyente"}
    assert pt.lectura_del_puente(una, "no_gana", ORDEN_PUENTE) == ("una_pieza_basta", ["b"])
    assert pt.lectura_del_puente(nogana, "no_concluyente", ORDEN_PUENTE) == ("solo_juntas", [])
    assert pt.lectura_del_puente(nogana, "gana", ORDEN_PUENTE) == ("solo_juntas", [])
    assert pt.lectura_del_puente(nogana, "no_gana", ORDEN_PUENTE) == ("ni_juntas", [])
    # una suelta basta aunque todo_junto no gane: el orden del yaml manda
    assert pt.lectura_del_puente(una, "no_concluyente", ORDEN_PUENTE)[0] == "una_pieza_basta"


def test_el_cierre_que_cierra_y_el_que_no() -> None:
    pub = PUENTE["cierre"]["publicadas_con_5_usd"]["v1"]
    tol_n = int(PROPIOS["cierre_tolerancia_operaciones"])
    tol_e = D(PROPIOS["cierre_tolerancia_esperanza_neta_r"])
    n, neta = int(pub["operaciones"]), D(pub["esperanza_neta_r"])
    assert pt.cierre_del_puente(n + tol_n, neta + tol_e, D(0), pub, tol_n, tol_e)[0]
    assert pt.cierre_del_puente(n - tol_n, neta - tol_e, D(0), pub, tol_n, tol_e)[0]
    assert not pt.cierre_del_puente(n + tol_n + 1, neta, D(0), pub, tol_n, tol_e)[0]
    assert not pt.cierre_del_puente(n, neta + tol_e + D("0.001"), D(0), pub, tol_n, tol_e)[0]
    assert not pt.cierre_del_puente(n, None, None, pub, tol_n, tol_e)[0]


def test_las_dieciseis_variantes_en_su_orden() -> None:
    vs = pt.variantes_del_yaml(PUENTE)
    assert len(vs) == 16
    assert [v.grupo for v in vs] == ["base"] + ["suelta"] * 8 + ["todo_junto"] + [
        "de_vuelta"
    ] * 4 + ["cierre"] * 2
    assert vs[-2].nombre == "v1_de_hoy" and vs[-1].nombre == "v2_de_hoy"
    for v in vs:
        pt.piezas_de(v.piezas, PROPIOS)  # todas se pueden construir
