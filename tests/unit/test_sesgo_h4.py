"""El sesgo H4 (RN-003, ADR-0044), sobre velas SINTETICAS: cada rama, sin mirar el futuro, y los
cambios de hora de EE. UU. con la H4 de mitad de sesion contando en la siguiente."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from botsito.config.registro import cargar_registro
from botsito.data.agregacion import agregar
from botsito.data.velas import a_minuto
from botsito.domain.sesgo import CUERPO, MECHA, Sesgo, SesgoError, sesgo_h4
from botsito.domain.valores import HoraLocal, Puntos
from botsito.domain.velas import MinutoUtc, Vela

REPO = Path(__file__).resolve().parents[2]
H4 = 240
TOPE = 60
SERVIDOR = HoraLocal("17:00", "America/New_York")
MADRID = ZoneInfo("Europe/Madrid")


def h4(k: int, alto: int, bajo: int, abierta: int | None = None, cierre: int | None = None) -> Vela:
    """La k-esima vela H4 de una rejilla sintetica que empieza en el minuto 0."""
    a = bajo if abierta is None else abierta
    c = alto if cierre is None else cierre
    return Vela(MinutoUtc(k * H4), Puntos(a), Puntos(alto), Puntos(bajo), Puntos(c), 0, H4, H4)


def s(velas: list[Vela], apertura: int, tope: int = TOPE, criterio: str = MECHA) -> Sesgo:
    return sesgo_h4(velas, MinutoUtc(apertura), tope, criterio).sesgo


FIN = 3 * H4  # la apertura cae justo en el fin de la tercera vela


def test_rompe_arriba_es_alcista_y_el_color_no_decide() -> None:
    velas = [h4(0, 110, 100), h4(1, 108, 102), h4(2, 111, 103, abierta=109, cierre=104)]
    r = sesgo_h4(velas, MinutoUtc(FIN), TOPE, MECHA)
    assert r.sesgo is Sesgo.ALCISTA and r.ruptura_puntos == 3 and r.velas_miradas == 1


def test_rompe_abajo_es_bajista() -> None:
    velas = [h4(0, 110, 100), h4(1, 108, 102), h4(2, 107, 101)]
    assert s(velas, FIN) is Sesgo.BAJISTA


def test_no_rompe_y_el_sesgo_se_arrastra() -> None:
    velas = [h4(0, 110, 100), h4(1, 112, 104), h4(2, 111, 105)]  # la ultima, dentro
    r = sesgo_h4(velas, MinutoUtc(FIN), TOPE, MECHA)
    assert r.sesgo is Sesgo.ALCISTA and r.velas_miradas == 2


def test_un_equal_no_rompe() -> None:
    velas = [h4(0, 110, 100), h4(1, 107, 99), h4(2, 107, 99)]  # la ultima iguala los dos extremos
    r = sesgo_h4(velas, MinutoUtc(FIN), TOPE, MECHA)
    assert r.sesgo is Sesgo.BAJISTA and r.velas_miradas == 2  # manda la anterior, que si rompio


def test_romper_por_un_punto_basta() -> None:
    velas = [h4(0, 110, 100), h4(1, 111, 101)]
    r = sesgo_h4(velas, MinutoUtc(2 * H4), TOPE, MECHA)
    assert r.sesgo is Sesgo.ALCISTA and r.ruptura_puntos == 1


def test_rompe_ambos_extremos_es_ambiguo() -> None:
    velas = [h4(0, 110, 100), h4(1, 112, 99)]
    r = sesgo_h4(velas, MinutoUtc(2 * H4), TOPE, MECHA)
    assert r.sesgo is Sesgo.AMBIGUO and r.ruptura_puntos == 1


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
    # una vela posterior que rompe abajo, y una en curso (fin > apertura) marcada `completa`
    despues = [*base, h4(2, 105, 90), h4(3, 104, 80)]
    en_curso = Vela(
        MinutoUtc(apertura - 60), Puntos(95), Puntos(111), Puntos(80), Puntos(90), 0, H4, H4, True
    )
    assert sesgo_h4(despues, MinutoUtc(apertura), TOPE, MECHA) == antes
    assert sesgo_h4([*base, en_curso], MinutoUtc(apertura), TOPE, MECHA) == antes
    assert antes.sesgo is Sesgo.ALCISTA


# ---- cambio de hora de EE. UU.: rejilla del servidor (17:00 America/New_York) y sesiones en
# el reloj del trader. Las semanas en que la UE y EE. UU. no cambian la hora el mismo dia, una H4
# cierra a mitad de la sesion de las 07; tiene que contar en la de las 11, no en la de las 07.


def _m1_del_dia(dia: str, bloques: dict[str, tuple[int, int]]) -> list[Vela]:
    """M1 continuas de un dia UTC. `bloques` es 'HH' de inicio UTC de la H4 -> (bajo, alto): el
    primer minuto del bloque marca el bajo, el segundo el alto, el resto queda en medio."""
    velas: list[Vela] = []
    inicio = a_minuto(datetime.fromisoformat(f"{dia}T00:00+00:00"))
    actual = (100, 110)
    for m in range(inicio - 4 * 60, inicio + 24 * 60):
        hora = datetime.fromtimestamp(m * 60, tz=ZoneInfo("UTC")).strftime("%H")
        if datetime.fromtimestamp(m * 60, tz=ZoneInfo("UTC")).minute == 0 and hora in bloques:
            actual = bloques[hora]
        bajo, alto = actual
        dentro = (m % 60) if hora in bloques else 2
        precio = bajo if dentro == 0 else alto if dentro == 1 else (bajo + alto) // 2
        velas.append(Vela(MinutoUtc(m), Puntos(precio), Puntos(precio), Puntos(precio),
                          Puntos(precio), 1))  # fmt: skip
    return velas


def _apertura(dia: str, hora_madrid: str) -> MinutoUtc:
    local = datetime.fromisoformat(f"{dia}T{hora_madrid}:00").replace(tzinfo=MADRID)
    return a_minuto(local.astimezone(ZoneInfo("UTC")))


# Rejilla del servidor en las semanas de desfase: la H4 empieza a las 21, 01, 05, 09... UTC. La de
# las 01 rompe arriba a la de las 21; la de las 05 -que cierra a las 09 UTC = 10:00 en Madrid,
# a mitad de la sesion de las 07- rompe abajo.
BLOQUES = {"21": (100, 110), "01": (105, 120), "05": (90, 115), "09": (95, 112)}


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
