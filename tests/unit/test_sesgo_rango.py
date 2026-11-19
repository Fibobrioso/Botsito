"""El sesgo de H4 por el RANGO VIGENTE (sesion 7a, S-1; ADR-0094), sobre velas SINTETICAS: las
reglas a) a e) del ADR, en los dos sentidos.

«El rango es la vela verde grande y sigo buscando compras» (ev-v18-000249-bb7b1c07): una H4 que
rompe solo a su anterior sin salir del rango no cambia el lado. Con la regla de antes (la H4
previa contra su anterior, ADR-0080) si lo cambiaba: estos tests rompen en `main`."""

from __future__ import annotations

import pytest

from botsito.domain.sesgo import MECHA, Sesgo, SesgoError, sesgo_h4
from botsito.domain.valores import Puntos
from botsito.domain.velas import MinutoUtc, Vela

H4 = 240
TOPE = 60


def h4(k: int, alto: int, bajo: int, abierta: int | None = None, cierre: int | None = None) -> Vela:
    """La k-esima H4 de una rejilla que empieza en el minuto 0; sin `abierta` ni `cierre`, VERDE
    (abre en el bajo y cierra en el alto)."""
    a = bajo if abierta is None else abierta
    c = alto if cierre is None else cierre
    return Vela(MinutoUtc(k * H4), Puntos(a), Puntos(alto), Puntos(bajo), Puntos(c), 0, H4, H4)


def roja(k: int, alto: int, bajo: int) -> Vela:
    return h4(k, alto, bajo, abierta=alto, cierre=bajo)


def neutra(k: int, alto: int, bajo: int) -> Vela:
    medio = (alto + bajo) // 2
    return h4(k, alto, bajo, abierta=medio, cierre=medio)


def r(velas: list[Vela], tope: int = TOPE):  # type: ignore[no-untyped-def]
    return sesgo_h4(velas, MinutoUtc(len(velas) * H4), tope, MECHA)


# La base: la del arranque (k0) y una verde grande que rompe su alto (k1): alcista, y el rango
# pasa a ser la verde grande, de 100 a 210.
BASE = [h4(0, 150, 120), h4(1, 210, 100)]


def test_base_la_verde_grande_es_el_rango() -> None:
    res = r(BASE)
    assert res.sesgo is Sesgo.ALCISTA
    assert (res.rango_alto, res.rango_bajo, res.rango_vela) == (210, 100, MinutoUtc(H4))
    assert res.vela_que_fija == MinutoUtc(H4)


# ---- a) dentro del rango no cambia nada


def test_a_la_roja_que_rompe_solo_a_su_anterior_dentro_del_rango_no_cambia_el_lado() -> None:
    """El caso de S-1: tras la verde grande, una roja que rompe el bajo de la vela anterior sin
    salir del rango. Con la regla de antes daba bajista."""
    velas = [*BASE, h4(2, 205, 160), roja(3, 190, 140)]
    res = r(velas)
    assert res.sesgo is Sesgo.ALCISTA
    assert (res.rango_alto, res.rango_bajo) == (210, 100)
    assert res.vela_que_fija == MinutoUtc(H4)
    assert res.saltadas_color_contrario == res.saltadas_neutras_simples == 0


def test_a_un_equal_del_extremo_del_rango_no_rompe() -> None:
    assert r([*BASE, roja(2, 200, 100)]).sesgo is Sesgo.ALCISTA
    assert r([*BASE, h4(2, 210, 150)]).sesgo is Sesgo.ALCISTA


def test_a_al_reves_en_un_rango_bajista() -> None:
    base = [h4(0, 150, 120), roja(1, 160, 50)]
    velas = [*base, roja(2, 140, 70), h4(3, 150, 80)]  # verde que rompe el alto de su anterior
    res = r(velas)
    assert res.sesgo is Sesgo.BAJISTA
    assert (res.rango_alto, res.rango_bajo) == (160, 50)


# ---- b) rompe un extremo y cierra de su color: lado, y el rango pasa a ser esa vela


def test_b_rompe_el_bajo_del_rango_y_cierra_roja_es_bajista_y_es_el_rango_nuevo() -> None:
    res = r([*BASE, roja(2, 180, 90)])
    assert res.sesgo is Sesgo.BAJISTA
    assert (res.rango_alto, res.rango_bajo, res.rango_vela) == (180, 90, MinutoUtc(2 * H4))
    assert res.ruptura_puntos == 10 and not res.doble_ruptura


def test_b_el_rango_nuevo_manda_para_las_siguientes() -> None:
    # tras la roja que fija bajista (90-180), una verde que rompe el alto de 180 vuelve a alcista;
    # una que solo rompe el alto de su anterior dentro de 90-180, no
    assert r([*BASE, roja(2, 180, 90), h4(3, 185, 95)]).sesgo is Sesgo.ALCISTA
    assert r([*BASE, roja(2, 180, 90), roja(3, 150, 95), h4(4, 170, 100)]).sesgo is Sesgo.BAJISTA


# ---- c) rompe los dos: decide el color; sin cuerpo no decide y el rango no cambia


def test_c_doble_ruptura_decide_el_color_y_es_el_rango_nuevo() -> None:
    res = r([*BASE, roja(2, 220, 90)])
    assert res.sesgo is Sesgo.BAJISTA and res.doble_ruptura
    assert (res.rango_alto, res.rango_bajo) == (220, 90)
    res = r([*BASE, h4(2, 220, 90)])
    assert res.sesgo is Sesgo.ALCISTA and res.doble_ruptura


def test_c_doble_ruptura_sin_cuerpo_no_decide_y_el_rango_no_cambia() -> None:
    res = r([*BASE, neutra(2, 220, 90)])
    assert res.sesgo is Sesgo.ALCISTA
    assert (res.rango_alto, res.rango_bajo) == (210, 100)
    assert res.saltadas_neutras_dobles == 1


# ---- d) rompe un extremo y cierra del color contrario, o sin cuerpo: no decide y el rango no
# cambia (A-58, lectura del consultor)


def test_d_rompe_el_bajo_y_cierra_verde_no_decide_y_el_rango_no_cambia() -> None:
    res = r([*BASE, h4(2, 150, 90)])
    assert res.sesgo is Sesgo.ALCISTA
    assert (res.rango_alto, res.rango_bajo) == (210, 100)
    assert res.saltadas_color_contrario == 1
    # el rango sigue siendo 100-210: una roja con bajo en 95 lo rompe, aunque no pase el 90 de
    # la verde que no decidio
    assert r([*BASE, h4(2, 150, 90), roja(3, 140, 95)]).sesgo is Sesgo.BAJISTA


def test_d_rompe_un_extremo_sin_cuerpo_no_decide() -> None:
    res = r([*BASE, neutra(2, 150, 90)])
    assert res.sesgo is Sesgo.ALCISTA and res.saltadas_neutras_simples == 1


def test_d_las_saltadas_son_las_de_despues_de_la_que_fija() -> None:
    velas = [h4(0, 150, 120), h4(1, 145, 90), roja(2, 200, 100), h4(3, 210, 100), h4(4, 205, 95)]
    res = r(velas)
    # k1 rompe el bajo del rango y cierra verde: saltada; k2 rompe los dos y cierra roja
    # (bajista); k3 rompe el alto y cierra verde (alcista, rango 100-210); k4 rompe el bajo y
    # cierra verde: saltada despues de la que fija. Solo cuenta k4.
    assert res.sesgo is Sesgo.ALCISTA and res.vela_que_fija == MinutoUtc(3 * H4)
    assert res.saltadas_color_contrario == 1
    assert res.h4_saltadas == ((MinutoUtc(4 * H4), "color_contrario"),)


# ---- e) el arranque


def test_e_el_rango_inicial_es_la_h4_tope_velas_antes_de_la_ultima_sin_lado() -> None:
    velas = [h4(0, 300, 10), h4(1, 150, 120), h4(2, 140, 125), h4(3, 135, 128)]
    # con tope 2 el rango inicial es k1 (120-150): nadie lo rompe, INSUFICIENTE
    res = r(velas, tope=2)
    assert res.sesgo is Sesgo.INSUFICIENTE
    assert (res.rango_alto, res.rango_bajo, res.rango_vela) == (150, 120, MinutoUtc(H4))
    assert res.velas_miradas == 2


def test_e_con_menos_velas_que_el_tope_arranca_en_la_primera() -> None:
    res = r(BASE, tope=TOPE)
    assert res.sesgo is Sesgo.ALCISTA and res.velas_miradas == 1
    res = r([h4(0, 150, 120)], tope=TOPE)
    assert res.sesgo is Sesgo.INSUFICIENTE and res.rango_vela == MinutoUtc(0)
    assert r([], tope=TOPE).sesgo is Sesgo.INSUFICIENTE


def test_e_una_ruptura_antes_del_arranque_no_cuenta() -> None:
    velas = [h4(0, 150, 120), h4(1, 210, 100), h4(2, 205, 110), h4(3, 200, 120)]
    assert r(velas, tope=TOPE).sesgo is Sesgo.ALCISTA
    assert r(velas, tope=1).sesgo is Sesgo.INSUFICIENTE  # el rango arranca en k2


def test_la_lectura_del_rango_nuevo_que_no_esta_escrita_se_niega() -> None:
    with pytest.raises(SesgoError):
        sesgo_h4(BASE, MinutoUtc(2 * H4), TOPE, MECHA, "otra")
