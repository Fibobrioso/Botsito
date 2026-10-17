"""El sesgo H4 (RN-003, ADR-0044, ADR-0080), sobre velas SINTETICAS: cada rama, sin mirar el futuro,
y los cambios de hora de EE. UU. con la H4 de mitad de sesion contando en la siguiente.

Desde ADR-0080 (WhatsApp del trader del 2026-10-14) una H4 cambia el sesgo solo si rompe el
extremo de la anterior Y cierra del color de esa ruptura; por eso cada vela que rompe lleva aqui
su color EXPLICITO (el ayudante `h4` cierra verde por defecto)."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from botsito.config.registro import cargar_registro
from botsito.data.agregacion import agregar
from botsito.data.velas import a_minuto
from botsito.domain.sesgo import CUERPO, MECHA, ResultadoSesgo, Sesgo, SesgoError, sesgo_h4
from botsito.domain.valores import HoraLocal, Puntos
from botsito.domain.velas import MinutoUtc, Vela

REPO = Path(__file__).resolve().parents[2]
H4 = 240
TOPE = 60
SERVIDOR = HoraLocal("17:00", "America/New_York")
MADRID = ZoneInfo("Europe/Madrid")


def h4(k: int, alto: int, bajo: int, abierta: int | None = None, cierre: int | None = None) -> Vela:
    """La k-esima vela H4 de una rejilla sintetica que empieza en el minuto 0. Sin `abierta` ni
    `cierre` abre en el bajo y cierra en el alto: VERDE."""
    a = bajo if abierta is None else abierta
    c = alto if cierre is None else cierre
    return Vela(MinutoUtc(k * H4), Puntos(a), Puntos(alto), Puntos(bajo), Puntos(c), 0, H4, H4)


def s(velas: list[Vela], apertura: int, tope: int = TOPE, criterio: str = MECHA) -> Sesgo:
    return sesgo_h4(velas, MinutoUtc(apertura), tope, criterio).sesgo


FIN = 3 * H4  # la apertura cae justo en el fin de la tercera vela


# ---- la regla del WhatsApp del 2026-10-14 (ADR-0080): los cuatro casos del grafico que el
# trader confirmo («Si, esta bien bro»), en los dos sentidos


def test_caso_1_rompe_el_bajo_y_cierra_roja_es_bajista() -> None:
    velas = [h4(0, 110, 100), h4(1, 112, 101), h4(2, 111, 99, abierta=110, cierre=102)]
    r = sesgo_h4(velas, MinutoUtc(FIN), TOPE, MECHA)
    assert r.sesgo is Sesgo.BAJISTA and r.ruptura_puntos == 2 and r.velas_miradas == 1
    assert not r.doble_ruptura and r.saltadas_color_contrario == 0


def test_caso_2_rompe_el_maximo_y_cierra_verde_es_alcista() -> None:
    velas = [
        h4(0, 110, 100),
        h4(1, 108, 98, abierta=107, cierre=99),
        h4(2, 111, 103, abierta=104, cierre=109),
    ]
    r = sesgo_h4(velas, MinutoUtc(FIN), TOPE, MECHA)
    assert r.sesgo is Sesgo.ALCISTA and r.ruptura_puntos == 3 and r.velas_miradas == 1
    assert not r.doble_ruptura  # con un solo extremo roto la ruptura no es doble


def test_caso_3_rompe_el_maximo_y_cierra_roja_sigue_el_sesgo_que_habia() -> None:
    """La H4 detras fijo BAJISTA (rompio el bajo y cerro roja); la ultima rompe el maximo pero
    cierra roja: no decide, y el sesgo sigue bajista. Es la vela de v6 1:04:30 con el resultado
    del WhatsApp (contradiccion abierta, SESGO-H4-COLOR.md §1.c)."""
    velas = [
        h4(0, 110, 100),
        h4(1, 108, 98, abierta=107, cierre=99),
        h4(2, 111, 103, abierta=109, cierre=104),
    ]
    r = sesgo_h4(velas, MinutoUtc(FIN), TOPE, MECHA)
    assert r.sesgo is Sesgo.BAJISTA and r.ruptura_puntos == 2 and r.velas_miradas == 2
    assert r.saltadas_color_contrario == 1 and not r.doble_ruptura


def test_caso_4_rompe_el_bajo_y_cierra_verde_sigue_el_sesgo_que_habia() -> None:
    velas = [
        h4(0, 110, 100),
        h4(1, 112, 101, abierta=102, cierre=111),
        h4(2, 111, 99, abierta=100, cierre=110),
    ]
    r = sesgo_h4(velas, MinutoUtc(FIN), TOPE, MECHA)
    assert r.sesgo is Sesgo.ALCISTA and r.ruptura_puntos == 2 and r.velas_miradas == 2
    assert r.saltadas_color_contrario == 1


def test_los_cuatro_casos_al_reves_para_el_alcista() -> None:
    """Los mismos cuatro con el sesgo previo alcista: 1 y 2 deciden por su color; 3 y 4 no."""
    previa = [h4(0, 110, 100), h4(1, 112, 101, abierta=102, cierre=111)]  # fija ALCISTA
    rompe_bajo_roja = h4(2, 111, 99, abierta=110, cierre=102)
    rompe_max_verde = h4(2, 113, 103, abierta=104, cierre=112)
    rompe_max_roja = h4(2, 113, 103, abierta=112, cierre=104)
    rompe_bajo_verde = h4(2, 111, 99, abierta=100, cierre=110)
    assert s([*previa, rompe_bajo_roja], FIN) is Sesgo.BAJISTA
    assert s([*previa, rompe_max_verde], FIN) is Sesgo.ALCISTA
    sigue = sesgo_h4([*previa, rompe_max_roja], MinutoUtc(FIN), TOPE, MECHA)
    assert sigue.sesgo is Sesgo.ALCISTA and sigue.velas_miradas == 2
    sigue = sesgo_h4([*previa, rompe_bajo_verde], MinutoUtc(FIN), TOPE, MECHA)
    assert sigue.sesgo is Sesgo.ALCISTA and sigue.velas_miradas == 2


def test_ruptura_simple_sin_cuerpo_no_decide_y_la_busqueda_sigue() -> None:
    """D3 (decision del consultor, pendiente de la sesion 5): rompe un extremo y cierra donde
    abrio; no tiene color, no decide, y manda la H4 anterior que rompio con su color."""
    bajista_detras = [
        h4(0, 110, 100),
        h4(1, 108, 98, abierta=107, cierre=99),
        h4(2, 112, 103, abierta=105, cierre=105),
    ]
    r = sesgo_h4(bajista_detras, MinutoUtc(FIN), TOPE, MECHA)
    assert r.sesgo is Sesgo.BAJISTA and r.velas_miradas == 2
    assert r.saltadas_neutras_simples == 1 and r.saltadas_color_contrario == 0
    alcista_detras = [
        h4(0, 110, 100),
        h4(1, 112, 101, abierta=102, cierre=111),
        h4(2, 111, 99, abierta=105, cierre=105),
    ]
    r = sesgo_h4(alcista_detras, MinutoUtc(FIN), TOPE, MECHA)
    assert r.sesgo is Sesgo.ALCISTA and r.velas_miradas == 2 and r.saltadas_neutras_simples == 1


def test_color_contrario_sin_nada_detras_dentro_del_tope_es_insuficiente() -> None:
    velas = [h4(0, 110, 100), h4(1, 108, 102), h4(2, 111, 103, abierta=109, cierre=104)]
    r = sesgo_h4(velas, MinutoUtc(FIN), TOPE, MECHA)
    assert r.sesgo is Sesgo.INSUFICIENTE and r.ruptura_puntos is None and r.velas_miradas == 2
    assert r.saltadas_color_contrario == 1
    # y con el tope en 1 la busqueda ni llega a la de detras, aunque rompiera con color
    con_color_detras = [h4(0, 110, 100), h4(1, 108, 98, abierta=107, cierre=99), velas[2]]
    assert sesgo_h4(con_color_detras, MinutoUtc(FIN), 1, MECHA).sesgo is Sesgo.INSUFICIENTE


def test_varias_seguidas_de_color_contrario_se_saltan_todas() -> None:
    velas = [
        h4(0, 110, 100),
        h4(1, 108, 98, abierta=107, cierre=99),  # fija BAJISTA
        h4(2, 111, 103, abierta=109, cierre=104),  # rompe arriba, roja
        h4(3, 113, 104, abierta=112, cierre=105),  # rompe arriba, roja
        h4(4, 112, 103, abierta=104, cierre=111),  # rompe abajo, verde
    ]
    r = sesgo_h4(velas, MinutoUtc(5 * H4), TOPE, MECHA)
    assert r.sesgo is Sesgo.BAJISTA and r.velas_miradas == 4 and r.saltadas_color_contrario == 3
    # el tope cuenta las saltadas: con tope 3 no se llega a la que fijo
    r = sesgo_h4(velas, MinutoUtc(5 * H4), 3, MECHA)
    assert r.sesgo is Sesgo.INSUFICIENTE and r.saltadas_color_contrario == 3


def test_la_doble_ruptura_no_cambia_con_la_regla_nueva() -> None:
    """D2: ADR-0060 §1 (decide el color) y la neutra de ADR-0075 ya son casos de la regla."""
    verde = [h4(0, 110, 100), h4(1, 112, 99, abierta=101, cierre=108)]
    r = sesgo_h4(verde, MinutoUtc(2 * H4), TOPE, MECHA)
    assert r.sesgo is Sesgo.ALCISTA and r.doble_ruptura and r.saltadas_color_contrario == 0
    roja = [h4(0, 110, 100), h4(1, 112, 99, abierta=108, cierre=101)]
    assert sesgo_h4(roja, MinutoUtc(2 * H4), TOPE, MECHA).sesgo is Sesgo.BAJISTA
    neutra = [
        h4(0, 110, 100),
        h4(1, 108, 98, abierta=107, cierre=99),
        h4(2, 115, 96, abierta=105, cierre=105),
    ]
    r = sesgo_h4(neutra, MinutoUtc(FIN), TOPE, MECHA)
    assert r.sesgo is Sesgo.BAJISTA and r.velas_miradas == 2
    assert r.saltadas_neutras_dobles == 1 and r.saltadas_neutras_simples == 0


def test_con_criterio_de_cuerpo_la_regla_del_color_tambien_vale() -> None:
    # con `cuerpo` los extremos son los del cuerpo; el color sigue siendo cierre contra apertura
    previa = [
        h4(0, 110, 100, abierta=103, cierre=107),
        h4(1, 112, 101, abierta=102, cierre=109),
    ]  # alcista
    rompe_arriba_roja = h4(2, 114, 104, abierta=112, cierre=105)  # cuerpo 105-112 rompe 109, roja
    r = sesgo_h4([*previa, rompe_arriba_roja], MinutoUtc(FIN), TOPE, CUERPO)
    assert r.sesgo is Sesgo.ALCISTA and r.velas_miradas == 2 and r.saltadas_color_contrario == 1
    rompe_arriba_verde = h4(2, 114, 104, abierta=105, cierre=112)
    r = sesgo_h4([*previa, rompe_arriba_verde], MinutoUtc(FIN), TOPE, CUERPO)
    assert r.sesgo is Sesgo.ALCISTA and r.velas_miradas == 1 and r.ruptura_puntos == 3


def test_las_saltadas_llevan_valor_por_defecto_cero() -> None:
    r = ResultadoSesgo(Sesgo.ALCISTA, 1, 1)
    assert (r.saltadas_color_contrario, r.saltadas_neutras_simples, r.saltadas_neutras_dobles) == (
        0,
        0,
        0,
    )
    assert not r.doble_ruptura


# ---- lo de antes de ADR-0080, con el color explicito donde la regla nueva lo exige


def test_rompe_arriba_y_cierra_verde_es_alcista() -> None:
    """Hasta ADR-0080 esta vela cerraba ROJA y daba ALCISTA («el color no decide»); ahora el
    color es el de la ruptura. Lo que comprobaba -puntos, velas miradas, no doble- sigue igual."""
    velas = [h4(0, 110, 100), h4(1, 108, 102), h4(2, 111, 103, abierta=104, cierre=109)]
    r = sesgo_h4(velas, MinutoUtc(FIN), TOPE, MECHA)
    assert r.sesgo is Sesgo.ALCISTA and r.ruptura_puntos == 3 and r.velas_miradas == 1
    assert not r.doble_ruptura


def test_rompe_abajo_y_cierra_roja_es_bajista() -> None:
    velas = [h4(0, 110, 100), h4(1, 108, 102), h4(2, 107, 101, abierta=106, cierre=102)]
    assert s(velas, FIN) is Sesgo.BAJISTA


def test_no_rompe_y_el_sesgo_se_arrastra() -> None:
    velas = [h4(0, 110, 100), h4(1, 112, 104), h4(2, 111, 105)]  # la ultima, dentro
    r = sesgo_h4(velas, MinutoUtc(FIN), TOPE, MECHA)
    assert r.sesgo is Sesgo.ALCISTA and r.velas_miradas == 2


def test_un_equal_no_rompe() -> None:
    # la ultima iguala los dos extremos; manda la anterior, que rompio abajo cerrando roja
    velas = [h4(0, 110, 100), h4(1, 107, 99, abierta=106, cierre=100), h4(2, 107, 99)]
    r = sesgo_h4(velas, MinutoUtc(FIN), TOPE, MECHA)
    assert r.sesgo is Sesgo.BAJISTA and r.velas_miradas == 2


def test_romper_por_un_punto_basta() -> None:
    velas = [h4(0, 110, 100), h4(1, 111, 101)]
    r = sesgo_h4(velas, MinutoUtc(2 * H4), TOPE, MECHA)
    assert r.sesgo is Sesgo.ALCISTA and r.ruptura_puntos == 1


def test_rompe_ambos_extremos_y_decide_el_color_de_la_vela() -> None:
    """Sesion 3, A-34 RESUELTA: «si rompe por los dos [...] importa el color de la vela»."""
    verde = [h4(0, 110, 100), h4(1, 112, 99, abierta=101, cierre=108)]
    r = sesgo_h4(verde, MinutoUtc(2 * H4), TOPE, MECHA)
    assert r.sesgo is Sesgo.ALCISTA and r.ruptura_puntos == 2 and r.doble_ruptura
    roja = [h4(0, 110, 100), h4(1, 112, 99, abierta=108, cierre=101)]
    r = sesgo_h4(roja, MinutoUtc(2 * H4), TOPE, MECHA)
    assert r.sesgo is Sesgo.BAJISTA and r.ruptura_puntos == 1 and r.doble_ruptura


def test_doble_ruptura_sin_cuerpo_no_decide_y_sin_nada_detras_es_insuficiente() -> None:
    """Cambia de sentido A PROPOSITO (sesion 4, S-13; ADR-0075, enmienda ADR-0060 §2): hasta
    entonces daba AMBIGUO. Sin cuerpo no hay color y la vela no fija nada: se sigue hacia atras, y
    si no hay nada detras, INSUFICIENTE."""
    velas = [h4(0, 110, 100), h4(1, 112, 99, abierta=105, cierre=105)]
    r = sesgo_h4(velas, MinutoUtc(2 * H4), TOPE, MECHA)
    assert r.sesgo is Sesgo.INSUFICIENTE and r.ruptura_puntos is None and r.velas_miradas == 1
    assert not r.doble_ruptura and r.saltadas_neutras_dobles == 1


def test_una_neutra_mantiene_el_sesgo_anterior_alcista_y_bajista() -> None:
    """S-13: «si esta es una vela neutra, no tiene ningún color, nosotros seguiríamos operando
    alcistas» (ev-v10-014005-7e2228f4). El trader lo dijo con sesgo previo alcista; el caso bajista
    se deduce y su confirmacion va a la sesion 5 (ADR-0075). Desde ADR-0080 la H4 que fija lleva
    su color: la bajista cierra roja."""
    alcista = [h4(0, 110, 100), h4(1, 112, 101), h4(2, 115, 96, abierta=105, cierre=105)]
    r = sesgo_h4(alcista, MinutoUtc(3 * H4), TOPE, MECHA)
    assert r.sesgo is Sesgo.ALCISTA and r.ruptura_puntos == 2 and r.velas_miradas == 2
    assert not r.doble_ruptura  # la que fija es la de un solo extremo, no la neutra
    bajista = [
        h4(0, 110, 100),
        h4(1, 108, 98, abierta=107, cierre=99),
        h4(2, 115, 96, abierta=105, cierre=105),
    ]
    r = sesgo_h4(bajista, MinutoUtc(3 * H4), TOPE, MECHA)
    assert r.sesgo is Sesgo.BAJISTA and r.ruptura_puntos == 2 and r.velas_miradas == 2


def test_dos_neutras_seguidas_mantienen_el_sesgo() -> None:
    velas = [
        h4(0, 110, 100),
        h4(1, 112, 101),
        h4(2, 115, 98, abierta=105, cierre=105),
        h4(3, 118, 95, abierta=106, cierre=106),
    ]
    r = sesgo_h4(velas, MinutoUtc(4 * H4), TOPE, MECHA)
    assert r.sesgo is Sesgo.ALCISTA and r.velas_miradas == 3 and r.saltadas_neutras_dobles == 2
    # y el tope cuenta las neutras saltadas: con tope 2 no se llega a la que rompio
    assert sesgo_h4(velas, MinutoUtc(4 * H4), 2, MECHA).sesgo is Sesgo.INSUFICIENTE


def test_con_un_cuerpo_de_un_punto_la_doble_ruptura_ya_decide() -> None:
    """No hay umbral en H4: con un cuerpo de un punto la doble ruptura toma su color
    (S-13, v10 1:41:01-1:41:29; ADR-0075)."""
    velas = [h4(0, 110, 100), h4(1, 108, 98), h4(2, 115, 96, abierta=105, cierre=106)]
    r = sesgo_h4(velas, MinutoUtc(3 * H4), TOPE, MECHA)
    assert r.sesgo is Sesgo.ALCISTA and r.doble_ruptura and r.velas_miradas == 1


def test_la_doble_ruptura_fija_el_sesgo_y_no_se_sigue_mirando_hacia_atras() -> None:
    # la primera rompio abajo (bajista); la segunda rompe los dos y cierra verde; la tercera,
    # dentro: manda la segunda, con su color, y la busqueda para en ella
    velas = [
        h4(0, 110, 100),
        h4(1, 109, 95),
        h4(2, 112, 90, abierta=92, cierre=110),
        h4(3, 111, 91),
    ]
    r = sesgo_h4(velas, MinutoUtc(4 * H4), TOPE, MECHA)
    assert r.sesgo is Sesgo.ALCISTA and r.velas_miradas == 2 and r.doble_ruptura


def test_con_criterio_de_cuerpo_la_doble_ruptura_tambien_la_decide_el_color() -> None:
    # con `cuerpo`, los extremos son los del cuerpo; una vela los rompe los dos solo si su
    # cuerpo envuelve al anterior, y el color sigue siendo el de su cierre contra su apertura
    velas = [
        h4(0, 110, 100, abierta=103, cierre=107),
        h4(1, 115, 95, abierta=109, cierre=101),
    ]
    r = sesgo_h4(velas, MinutoUtc(2 * H4), TOPE, CUERPO)
    assert r.sesgo is Sesgo.BAJISTA and r.doble_ruptura


def test_sin_ruptura_dentro_del_tope_es_insuficiente() -> None:
    velas = [h4(0, 110, 100), h4(1, 112, 101), h4(2, 111, 102), h4(3, 111, 102)]
    assert s(velas, 4 * H4) is Sesgo.ALCISTA  # la ruptura esta tres velas atras
    r = sesgo_h4(velas, MinutoUtc(4 * H4), 2, MECHA)
    assert r.sesgo is Sesgo.INSUFICIENTE and r.ruptura_puntos is None and r.velas_miradas == 2


def test_menos_de_dos_velas_es_insuficiente() -> None:
    assert s([], FIN) is Sesgo.INSUFICIENTE
    assert s([h4(0, 110, 100)], FIN) is Sesgo.INSUFICIENTE


def test_con_cuerpo_la_mecha_no_rompe() -> None:
    velas = [h4(0, 110, 100, abierta=101, cierre=109), h4(1, 115, 102, abierta=103, cierre=108)]
    assert s(velas, 2 * H4, criterio=MECHA) is Sesgo.ALCISTA
    assert s(velas, 2 * H4, criterio=CUERPO) is Sesgo.INSUFICIENTE


def test_argumentos_invalidos() -> None:
    with pytest.raises(SesgoError):
        sesgo_h4([], MinutoUtc(0), 0, MECHA)
    with pytest.raises(SesgoError):
        sesgo_h4([h4(0, 1, 0), h4(1, 2, 0)], MinutoUtc(2 * H4), 1, "cierre")


def test_anti_look_ahead_velas_posteriores_y_la_vela_en_curso() -> None:
    base = [h4(0, 110, 100), h4(1, 112, 102)]
    apertura = 2 * H4
    antes = sesgo_h4(base, MinutoUtc(apertura), TOPE, MECHA)
    # una vela posterior que rompe abajo cerrando roja, y una en curso (fin > apertura) marcada
    # `completa` que rompe arriba y cierra roja (la que la regla nueva saltaria)
    despues = [
        *base,
        h4(2, 105, 90, abierta=104, cierre=91),
        h4(3, 104, 80, abierta=103, cierre=81),
    ]
    en_curso = Vela(
        MinutoUtc(apertura - 60),
        Puntos(111),
        Puntos(115),
        Puntos(101),
        Puntos(102),
        0,
        H4,
        H4,
        True,
    )
    assert sesgo_h4(despues, MinutoUtc(apertura), TOPE, MECHA) == antes
    assert sesgo_h4([*base, en_curso], MinutoUtc(apertura), TOPE, MECHA) == antes
    assert antes.sesgo is Sesgo.ALCISTA and antes.saltadas_color_contrario == 0


# ---- cambio de hora de EE. UU.: rejilla del servidor (17:00 America/New_York) y sesiones en
# el reloj del trader. Las semanas en que la UE y EE. UU. no cambian la hora el mismo dia, una H4
# cierra a mitad de la sesion de las 07; tiene que contar en la de las 11, no en la de las 07.


def _m1_del_dia(dia: str, bloques: dict[str, tuple[int, int, bool]]) -> list[Vela]:
    """M1 continuas de un dia UTC. `bloques` es 'HH' de inicio UTC de la H4 -> (bajo, alto, roja):
    el primer minuto del bloque marca un extremo, el segundo el otro, el resto queda en medio. Con
    `roja` el primer minuto es el alto y el bloque abre arriba y cierra en medio (H4 roja); si no,
    abre en el bajo y cierra en medio (H4 verde). El color lo exige ADR-0080."""
    velas: list[Vela] = []
    inicio = a_minuto(datetime.fromisoformat(f"{dia}T00:00+00:00"))
    actual = (100, 110, False)
    for m in range(inicio - 4 * 60, inicio + 24 * 60):
        hora = datetime.fromtimestamp(m * 60, tz=ZoneInfo("UTC")).strftime("%H")
        if datetime.fromtimestamp(m * 60, tz=ZoneInfo("UTC")).minute == 0 and hora in bloques:
            actual = bloques[hora]
        bajo, alto, roja = actual
        dentro = (m % 60) if hora in bloques else 2
        primero, segundo = (alto, bajo) if roja else (bajo, alto)
        precio = primero if dentro == 0 else segundo if dentro == 1 else (bajo + alto) // 2
        velas.append(Vela(MinutoUtc(m), Puntos(precio), Puntos(precio), Puntos(precio),
                          Puntos(precio), 1))  # fmt: skip
    return velas


def _apertura(dia: str, hora_madrid: str) -> MinutoUtc:
    local = datetime.fromisoformat(f"{dia}T{hora_madrid}:00").replace(tzinfo=MADRID)
    return a_minuto(local.astimezone(ZoneInfo("UTC")))


# Rejilla del servidor en las semanas de desfase: la H4 empieza a las 21, 01, 05, 09... UTC. La de
# las 01 rompe arriba a la de las 21 y cierra verde; la de las 05 -que cierra a las 09 UTC = 10:00
# en Madrid, a mitad de la sesion de las 07- rompe abajo y cierra ROJA.
BLOQUES = {
    "21": (100, 110, False),
    "01": (105, 120, False),
    "05": (90, 115, True),
    "09": (95, 112, False),
}


@pytest.mark.parametrize("dia", ["2026-03-10", "2026-10-27"])  # primavera y otono de EE. UU.
def test_semana_de_desfase_la_h4_de_mitad_de_sesion_cuenta_en_la_siguiente(dia: str) -> None:
    velas_h4 = agregar(_m1_del_dia(dia, BLOQUES), H4, SERVIDOR)
    a_las_07, a_las_11 = _apertura(dia, "07:00"), _apertura(dia, "11:00")
    # la H4 de las 05 UTC termina a las 09 UTC: despues de las 07 de Madrid, antes de las 11
    cierre_mitad = a_minuto(datetime.fromisoformat(f"{dia}T09:00+00:00"))
    assert a_las_07 < cierre_mitad <= a_las_11
    assert sesgo_h4(velas_h4, a_las_07, TOPE, MECHA).sesgo is Sesgo.ALCISTA
    assert sesgo_h4(velas_h4, a_las_11, TOPE, MECHA).sesgo is Sesgo.BAJISTA


def test_semana_normal_las_h4_cierran_a_la_hora_de_las_sesiones() -> None:
    """En verano de los dos lados la H4 del servidor cierra a las 07 y a las 11 de Madrid: una vela
    que termina EXACTAMENTE en la apertura cuenta (fin <= apertura)."""
    dia = "2026-07-07"
    velas_h4 = agregar(_m1_del_dia(dia, BLOQUES), H4, SERVIDOR)
    fin_05 = a_minuto(datetime.fromisoformat(f"{dia}T09:00+00:00"))
    assert _apertura(dia, "11:00") == fin_05
    assert sesgo_h4(velas_h4, _apertura(dia, "11:00"), TOPE, MECHA).sesgo is Sesgo.BAJISTA
    assert sesgo_h4(velas_h4, _apertura(dia, "07:00"), TOPE, MECHA).sesgo is Sesgo.ALCISTA


def test_el_registro_da_el_tope_y_el_criterio_de_adr_0044() -> None:
    r = cargar_registro(REPO / "knowledge" / "spec" / "parametros.yaml")
    assert r.entero("sesgo_h4_tope_velas") == TOPE
    assert r.opcion("sesgo_h4_criterio_ruptura") == MECHA
