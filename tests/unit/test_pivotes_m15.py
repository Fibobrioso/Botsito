"""El pivote de M15 formado, con las DOS lecturas documentadas de A-35 como selector: sobre M15
SINTETICAS. Cada lectura da el pivote en el instante que define y ni un minuto antes; las dos
lecturas dan resultados distintos y predecibles sobre la misma secuencia; el mas reciente manda; y
lo que no esta documentado queda fijo y visible (doji, mecha de la contraria, vela en curso que
vuelve a su color)."""

from __future__ import annotations

import pytest

from botsito.domain.pivotes_m15 import (
    ALTO,
    BAJO,
    CIERRE_VELA_CONTRARIA,
    INICIO_VELA_CONTRARIA,
    LECTURAS,
    PivoteError,
    color,
    cruza,
    pivote_mas_reciente,
    pivotes_formados,
    toca,
)
from botsito.domain.valores import Puntos
from botsito.domain.velas import MinutoUtc, Vela

T0 = 31_500_000  # un minuto UTC cualquiera, multiplo de 15
M15 = 15


def _m15(n: int, a: int, c: int, alto: int | None = None, bajo: int | None = None) -> Vela:
    """La M15 numero `n` desde T0, con apertura `a` y cierre `c`."""
    hi = alto if alto is not None else max(a, c) + 2
    lo = bajo if bajo is not None else min(a, c) - 2
    return Vela(MinutoUtc(T0 + M15 * n), Puntos(a), Puntos(hi), Puntos(lo), Puntos(c), 1, M15, M15)


def _parcial(n: int, a: int, c: int, m1: int) -> Vela:
    """La M15 numero `n` en curso, con `m1` M1 cerradas dentro."""
    return Vela(
        MinutoUtc(T0 + M15 * n),
        Puntos(a),
        Puntos(max(a, c) + 1),
        Puntos(min(a, c) - 1),
        Puntos(c),
        1,
        M15,
        m1,
        False,
    )


# tres verdes (flujo alcista) y despues una roja: la roja marca el ALTO de la racha
FLUJO_ALCISTA = [_m15(0, 100, 110), _m15(1, 110, 120), _m15(2, 120, 130, alto=134)]
ROJA = _m15(3, 130, 118)
DESPUES = _m15(4, 118, 125)


def test_el_color_de_una_vela() -> None:
    assert color(_m15(0, 100, 110)) == 1
    assert color(_m15(0, 110, 100)) == -1
    assert color(_m15(0, 100, 100)) == 0


def test_la_vela_contraria_marca_el_extremo_de_la_racha_anterior() -> None:
    fin = int(ROJA.fin)
    (p,) = pivotes_formados([*FLUJO_ALCISTA, ROJA], None, CIERRE_VELA_CONTRARIA, fin)
    assert p.lado == ALTO and p.nivel == 134  # el maximo de la racha verde, no el de la roja
    assert p.contraria_inicio == ROJA.inicio and p.formado_en == ROJA.fin
    # y al reves: rojas y despues una verde marcan un BAJO
    bajista = [_m15(0, 130, 120), _m15(1, 120, 110, bajo=104), _m15(2, 110, 118)]
    (q,) = pivotes_formados(bajista, None, CIERRE_VELA_CONTRARIA, int(bajista[-1].fin))
    assert q.lado == BAJO and q.nivel == 104


def test_lectura_cierre_ni_un_minuto_antes_del_cierre_de_la_contraria() -> None:
    """Con `cierre_vela_contraria`: en el ultimo cierre de M1 dentro de la roja, la roja esta en
    curso y NO hay pivote; en su cierre, si."""
    antes = int(ROJA.fin) - 1
    en_curso = _parcial(3, 130, 118, 14)  # la roja con 14 M1 cerradas
    assert pivotes_formados(FLUJO_ALCISTA, en_curso, CIERRE_VELA_CONTRARIA, antes) == []
    (p,) = pivotes_formados([*FLUJO_ALCISTA, ROJA], None, CIERRE_VELA_CONTRARIA, int(ROJA.fin))
    assert p.formado_en == ROJA.fin


def test_lectura_inicio_desde_el_primer_cierre_de_m1_contrario_y_ni_uno_antes() -> None:
    """Con `inicio_vela_contraria`: al cerrar la ultima verde no hay pivote (la roja no tiene ni
    una M1); con la primera M1 de la roja cerrada y contraria, ya lo hay."""
    cierre_verde = int(FLUJO_ALCISTA[-1].fin)
    assert pivotes_formados(FLUJO_ALCISTA, None, INICIO_VELA_CONTRARIA, cierre_verde) == []
    primera_m1 = _parcial(3, 130, 128, 1)
    (p,) = pivotes_formados(FLUJO_ALCISTA, primera_m1, INICIO_VELA_CONTRARIA, cierre_verde + 1)
    assert p.lado == ALTO and p.nivel == 134 and p.formado_en == MinutoUtc(cierre_verde + 1)
    # una primera M1 que NO va contraria no forma nada
    primera_m1_verde = _parcial(3, 130, 131, 1)
    assert (
        pivotes_formados(FLUJO_ALCISTA, primera_m1_verde, INICIO_VELA_CONTRARIA, cierre_verde + 1)
        == []
    )


def test_las_dos_lecturas_difieren_de_forma_predecible_sobre_la_misma_secuencia() -> None:
    """La misma secuencia, minuto a minuto: `inicio` ve el pivote catorce minutos antes que
    `cierre`; si la vela en curso vuelve a su color, `inicio` lo retira y `cierre` nunca lo tuvo."""
    cierre_verde = int(FLUJO_ALCISTA[-1].fin)
    disponibles: dict[str, list[bool]] = {lectura: [] for lectura in LECTURAS}
    for m1 in range(1, 15):
        en_curso = _parcial(3, 130, 118, m1)
        for lectura in LECTURAS:
            hay = bool(pivotes_formados(FLUJO_ALCISTA, en_curso, lectura, cierre_verde + m1))
            disponibles[lectura].append(hay)
    assert all(disponibles[INICIO_VELA_CONTRARIA]) and not any(disponibles[CIERRE_VELA_CONTRARIA])
    # al cierre, las dos lo ven
    for lectura in LECTURAS:
        assert pivotes_formados([*FLUJO_ALCISTA, ROJA], None, lectura, int(ROJA.fin))
    # la vela en curso que vuelve a su color: `inicio` lo retira
    vuelve_verde = _parcial(3, 130, 133, 9)
    assert (
        pivotes_formados(FLUJO_ALCISTA, vuelve_verde, INICIO_VELA_CONTRARIA, cierre_verde + 9) == []
    )


def test_el_mas_reciente_del_lado_pedido_manda() -> None:
    velas = [
        _m15(0, 100, 110),
        _m15(1, 110, 120, alto=125),
        _m15(2, 120, 112),  # roja: ALTO en 125
        _m15(3, 112, 104, bajo=101),
        _m15(4, 104, 109),  # verde: BAJO en 101
        _m15(5, 109, 117, alto=119),
        _m15(6, 117, 113),  # roja: ALTO en 119, el mas reciente
    ]
    t = int(velas[-1].fin)
    todos = pivotes_formados(velas, None, CIERRE_VELA_CONTRARIA, t)
    assert [(p.lado, p.nivel) for p in todos] == [(ALTO, 125), (BAJO, 101), (ALTO, 119)]
    alto = pivote_mas_reciente(velas, None, CIERRE_VELA_CONTRARIA, t, ALTO)
    bajo = pivote_mas_reciente(velas, None, CIERRE_VELA_CONTRARIA, t, BAJO)
    assert alto is not None and alto.nivel == 119
    assert bajo is not None and bajo.nivel == 101
    assert (
        pivote_mas_reciente(velas[:1], None, CIERRE_VELA_CONTRARIA, int(velas[0].fin), ALTO) is None
    )


def test_lo_fijo_y_visible_doji_y_mecha_de_la_contraria() -> None:
    """Un doji no es de ningun color: no es contraria y corta la racha. La mecha de la propia
    contraria no mueve el nivel (segunda pregunta de A-35, sin decidir)."""
    con_doji = [_m15(0, 100, 110), _m15(1, 110, 110), _m15(2, 110, 100)]
    assert pivotes_formados(con_doji, None, CIERRE_VELA_CONTRARIA, int(con_doji[-1].fin)) == []
    roja_con_mecha = _m15(3, 130, 118, alto=140)  # la mecha supera el 134 de la racha
    (p,) = pivotes_formados(
        [*FLUJO_ALCISTA, roja_con_mecha], None, CIERRE_VELA_CONTRARIA, int(roja_con_mecha.fin)
    )
    assert p.nivel == 134


def test_toca_y_cruza_con_cuerpo_o_con_mecha() -> None:
    (p,) = pivotes_formados([*FLUJO_ALCISTA, ROJA], None, CIERRE_VELA_CONTRARIA, int(ROJA.fin))
    assert p.nivel == 134
    roza = _m15(4, 118, 130, alto=134)  # llega al nivel, no lo cruza
    perfora = _m15(4, 118, 130, alto=136)  # la mecha lo pasa, el cuerpo no
    cierra_encima = _m15(4, 118, 136, alto=138)
    assert toca(roza, p) and not cruza(roza, p, "cuerpo") and not cruza(roza, p, "mecha")
    assert toca(perfora, p) and cruza(perfora, p, "mecha") and not cruza(perfora, p, "cuerpo")
    assert cruza(cierra_encima, p, "cuerpo") and cruza(cierra_encima, p, "mecha")
    assert not toca(_m15(4, 118, 125), p)
    with pytest.raises(PivoteError, match="criterio"):
        cruza(roza, p, "otro")


def test_las_guardias_del_modelo() -> None:
    with pytest.raises(PivoteError, match="lectura"):
        pivotes_formados(FLUJO_ALCISTA, None, "al_ojo", int(FLUJO_ALCISTA[-1].fin))
    with pytest.raises(PivoteError, match="futuro"):
        pivotes_formados([*FLUJO_ALCISTA, ROJA], None, CIERRE_VELA_CONTRARIA, int(ROJA.fin) - 1)
    with pytest.raises(PivoteError, match="orden"):
        pivotes_formados([FLUJO_ALCISTA[1], FLUJO_ALCISTA[0]], None, CIERRE_VELA_CONTRARIA, T0 + 60)
    with pytest.raises(PivoteError, match="en curso"):
        pivotes_formados(
            FLUJO_ALCISTA, _parcial(1, 1, 2, 1), INICIO_VELA_CONTRARIA, int(FLUJO_ALCISTA[-1].fin)
        )
    with pytest.raises(PivoteError, match="lado"):
        pivote_mas_reciente(
            FLUJO_ALCISTA, None, CIERRE_VELA_CONTRARIA, int(FLUJO_ALCISTA[-1].fin), "medio"
        )
