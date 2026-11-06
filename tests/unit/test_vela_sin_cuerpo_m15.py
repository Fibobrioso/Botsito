"""La vela sin cuerpo en M15 (sesion 6, S-4; ADR-0085, recuadro del 2026-11-05 en §2): con
`sin_cuerpo = no_corta_y_cuenta` no corta la racha, no es contraria y entra en ella, asi que su
mecha cuenta en el nivel, una o varias seguidas, en un alto y en un bajo; las de cuerpo cero por
delante de la primera vela con color no entran. Lo que dijo el trader: el alto puede ser la mecha
de la vela sin cuerpo (ev-v17-002155-f2c95111), tambien con dos o tres seguidas
(ev-v17-002250-d6ca3ef8), y en un bajo desde la mecha mas baja (ev-v17-002217-af442f84); que no
corte la racha es la conclusion de la extraccion y LECTURA DEL CONSULTOR (encargo de
trabajo/activar-sesion-06-motor, fase 2).

`test_por_el_camino_real_la_liquidez_de_m15_sale_de_la_mecha_del_doji` falla con el codigo de
`main`: alli el motor de M15 no pasa `sin_cuerpo` y el doji corta la racha. Todo sintetico."""

from __future__ import annotations

from pathlib import Path

import pytest

from botsito.config.registro import Registro, cargar_registro
from botsito.domain.estructura_m1 import COMPRA, ultimo_punto_de_ruptura
from botsito.domain.pivotes_m15 import (
    ALTO,
    BAJO,
    CIERRE_VELA_CONTRARIA,
    SIN_CUERPO_NO_CORTA_Y_CUENTA,
    pivotes_formados,
)
from botsito.domain.valores import Puntos
from botsito.domain.velas import MinutoUtc, Vela
from botsito.engine.motor import DatosMercado
from tests.unit.test_pivotes_m15 import _m15

RAIZ = Path(__file__).resolve().parents[2]
NUEVA = SIN_CUERPO_NO_CORTA_Y_CUENTA
VERDES = [_m15(0, 100, 110), _m15(1, 110, 120), _m15(2, 120, 130, alto=134)]
ROJAS = [_m15(0, 130, 120), _m15(1, 120, 110), _m15(2, 110, 100, bajo=96)]


@pytest.fixture(scope="module")
def registro() -> Registro:
    return cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")


def _doji(n: int, precio: int, alto: int | None = None, bajo: int | None = None) -> Vela:
    return _m15(n, precio, precio, alto=alto, bajo=bajo)


def _unico(velas: list[Vela]) -> tuple[str, int]:
    (p,) = pivotes_formados(
        velas, None, CIERRE_VELA_CONTRARIA, int(velas[-1].fin), sin_cuerpo=NUEVA
    )
    return p.lado, p.nivel


@pytest.mark.parametrize("n_dojis", [1, 2, 3])
def test_una_dos_o_tres_velas_sin_cuerpo_seguidas_su_mecha_es_el_alto(n_dojis: int) -> None:
    """V, V, V (alto 134), n velas sin cuerpo (la mas alta con la mecha en 140) y una roja: el ALTO
    es 140, la mecha de la vela sin cuerpo, con una, dos o tres seguidas."""
    dojis = [_doji(3 + k, 130, alto=140 if k == n_dojis - 1 else 133) for k in range(n_dojis)]
    roja = _m15(3 + n_dojis, 130, 118)
    assert _unico([*VERDES, *dojis, roja]) == (ALTO, 140)


@pytest.mark.parametrize("n_dojis", [1, 2, 3])
def test_en_un_bajo_igual_desde_la_mecha_mas_baja(n_dojis: int) -> None:
    """R, R, R (bajo 96), n velas sin cuerpo (una con la mecha en 90) y una verde: el BAJO es 90."""
    dojis = [_doji(3 + k, 100, bajo=90 if k == 0 else 97) for k in range(n_dojis)]
    verde = _m15(3 + n_dojis, 100, 112)
    assert _unico([*ROJAS, *dojis, verde]) == (BAJO, 90)


def test_la_vela_sin_cuerpo_en_medio_de_la_racha_tambien_entra() -> None:
    velas = [_m15(0, 100, 110), _doji(1, 110, alto=150), _m15(2, 110, 120), _m15(3, 120, 105)]
    assert _unico(velas) == (ALTO, 150)


def test_la_vela_sin_cuerpo_por_delante_de_la_racha_no_entra() -> None:
    """Una vela sin cuerpo con la mecha en 200 ANTES de la primera verde de la racha (tras una
    roja) no entra: la racha empieza en una vela con color. El ALTO es el de las verdes, 134."""
    velas = [_m15(0, 140, 130), _doji(1, 130, alto=200), *[_m15(2 + k, v.abierta, v.cierre,
             alto=int(v.maxima)) for k, v in enumerate(VERDES)], _m15(5, 130, 118)]  # fmt: skip
    pivotes = pivotes_formados(
        velas, None, CIERRE_VELA_CONTRARIA, int(velas[-1].fin), sin_cuerpo=NUEVA
    )
    assert [(p.lado, p.nivel) for p in pivotes if p.lado == ALTO] == [(ALTO, 134)]


def test_solo_velas_sin_cuerpo_antes_de_la_contraria_no_forman_pivote() -> None:
    velas = [_doji(0, 130, alto=140), _doji(1, 130, alto=141), _m15(2, 130, 118)]
    assert (
        pivotes_formados(velas, None, CIERRE_VELA_CONTRARIA, int(velas[-1].fin), sin_cuerpo=NUEVA)
        == []
    )


def _m1(k: int, a: int, c: int, alto: int | None = None) -> Vela:
    hi = alto if alto is not None else max(a, c) + 1
    return Vela(
        MinutoUtc(31_500_000 + k), Puntos(a), Puntos(hi), Puntos(min(a, c) - 1), Puntos(c), 1
    )


def test_m1_no_se_mueve_el_punto_no_lleva_la_mecha_de_la_vela_sin_cuerpo() -> None:
    """El test por marco de ADR-0085: en M1 la vela sin cuerpo sigue con `no_cuenta`, y su mecha no
    entra en el extremo del punto aunque en M15 si entre."""
    m1 = [_m1(0, 1000, 1050), _m1(1, 1050, 1100, alto=1110), _m1(2, 1100, 1100, alto=1200),
          _m1(3, 1100, 1060)]  # fmt: skip
    punto = ultimo_punto_de_ruptura(m1, COMPRA)
    assert punto is not None and punto.nivel == 1110


def test_por_el_camino_real_la_liquidez_de_m15_sale_de_la_mecha_del_doji(
    registro: Registro,
) -> None:
    """Por `DatosMercado.liquidez_m15` (engine/motor.py), con las lecturas del registro real: V, V,
    V (alto 134), una vela sin cuerpo con la mecha en 140 y una roja cerrada. La liquidez de M15 es
    el ALTO en 140. Falla con el codigo de `main`: alli el doji corta la racha y no hay ALTO."""
    velas = [*VERDES, _doji(3, 130, alto=140), _m15(4, 130, 118)]
    datos = DatosMercado(
        [],
        velas,
        [],
        registro.opcion("liquidez_m15_pivote_formado"),
        registro.opcion("liquidez_m15_mecha_que_vuelve"),
        registro.opcion("liquidez_m15_criterio_toma"),
    )
    p = datos.liquidez_m15(int(velas[-1].fin), ALTO)
    assert p is not None and p.nivel == 140
