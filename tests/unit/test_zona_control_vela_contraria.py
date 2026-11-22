"""La zona de control pide una vela contraria al impulso (sesion 7b, bloque de dias, sesion 3,
2026-04-27; v21 1:26:23, `ev-v21-012623-bbdaf48a`: «Cuando todas las velas son verdes, no existe
zona de control. Tiene que haber una vela roja contraria al impulso que se está dando para yo poder
validarlo.»). Rama `trabajo/activar-sesion-08`, F4.

El motor YA lo cumple (ACTIVAR-SESION-08.md, 0.6: 0 de 57.643 pivotes de M1 de la construccion sin
vela contraria en su racha): `pivotes_de_control` solo cuenta pivotes de `_pivotes_m1`, y un pivote
se forma con una vela de color tras una racha del color contrario. Este test lo CONGELA, sin tocar
el motor ni RN-009: para TODAS las secuencias de colores de hasta 7 velas tras la toma (verde,
roja y sin cuerpo), en compra y en venta, cada zona de control que cuenta el motor tiene al menos
una vela contraria al impulso entre la primera vela del impulso y la que la forma; y todas del
color del impulso no dan ninguna zona. Pasa en `main` y en la rama: congela, no cambia nada."""

from __future__ import annotations

from itertools import product

import pytest

from botsito.domain.estructura_m1 import COMPRA, VENTA, pivotes_de_control
from botsito.domain.pivotes_m15 import color
from botsito.domain.valores import Puntos
from botsito.domain.velas import MinutoUtc, Vela

COLORES = (1, -1, 0)  # verde, roja, sin cuerpo
LARGO_MAX = 7


def _serie(colores: tuple[int, ...]) -> list[Vela]:
    """Una vela de toma sin cuerpo y luego una vela por color: cada una abre donde cerro la
    anterior y se mueve 10 puntos en su color (las sin cuerpo, una cruz de 2)."""
    velas = [Vela(MinutoUtc(1000), Puntos(1000), Puntos(1001), Puntos(999), Puntos(1000), 1)]
    precio = 1000
    for i, c in enumerate(colores, start=1):
        cierre = precio + 10 * c
        velas.append(
            Vela(
                MinutoUtc(1000 + i),
                Puntos(precio),
                Puntos(max(precio, cierre) + 2),
                Puntos(min(precio, cierre) - 2),
                Puntos(cierre),
                1,
            )
        )
        precio = cierre
    return velas


def _contrarias_antes_de(m1: list[Vela], hasta_inicio: int, signo: int) -> int:
    """Cuantas velas contrarias al impulso hay entre la primera vela del impulso tras la toma y la
    vela que forma el pivote (sin incluirla)."""
    k = next(i for i in range(1, len(m1)) if color(m1[i]) == signo)
    return sum(1 for v in m1[k:] if int(v.inicio) < hasta_inicio and color(v) == -signo)


@pytest.mark.parametrize(("lado", "signo"), [(COMPRA, 1), (VENTA, -1)])
def test_ninguna_zona_de_control_sin_una_vela_contraria_al_impulso(lado: str, signo: int) -> None:
    vistas = 0
    for largo in range(1, LARGO_MAX + 1):
        for colores in product(COLORES, repeat=largo):
            m1 = _serie(colores)
            for p in pivotes_de_control(m1, 0, len(m1) - 1, lado):
                vistas += 1
                assert _contrarias_antes_de(m1, int(p.contraria_inicio), signo) >= 1, colores
    assert vistas > 0  # el barrido llega a contar zonas


@pytest.mark.parametrize(("lado", "signo"), [(COMPRA, 1), (VENTA, -1)])
def test_todas_del_color_del_impulso_es_un_impulso_sin_zona_de_control(
    lado: str, signo: int
) -> None:
    for largo in range(1, LARGO_MAX + 1):
        m1 = _serie((signo,) * largo)
        assert pivotes_de_control(m1, 0, len(m1) - 1, lado) == ()
