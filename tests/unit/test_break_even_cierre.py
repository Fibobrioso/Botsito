"""El break even de RN-014 al CIERRE y con CUERPO (sesion 7a, S-2; trabajo/activar-sesion-07, F2).

Lo que dijo el trader: ni al toque ni a secas; cuando se desarrolla y se valida una zona de control,
esperando al cierre de la vela («nosotros esperamos a que cierre la vela y si cierra por debajo no
vamos a poder», ev-v18-001327-70f1d014; «pasas el stop de la entrada cuando se se desarrolla una
zona de control completamente validada», ev-v18-001900-1581efbe); en una venta, al revés. La zona
es la de siempre (RN-014, ADR-0061 §4: el extremo de la racha a favor que deja la primera vela
contraria despues de la entrada); cambia cuando se da por rota: una M1 tiene que CERRAR mas alla.

Con lo fijado hasta esta rama (`break_even_condicion` = tocar y `break_even_criterio_ruptura` =
mecha) la M1 que pasa el nivel solo con la mecha mueve el stop: estos tests leen los dos
parametros del registro real y rompen en `main`."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pytest

from botsito.cases.paquete import cargar_config
from botsito.config.ajustes import carpeta_datos
from botsito.config.registro import Registro, cargar_registro
from botsito.data.dataset import DatasetError, buscar_manifiesto, cargar_manifiesto, cargar_serie
from botsito.domain.estructura_m1 import (
    COMPRA,
    CUERPO,
    MECHA,
    VENTA,
    zona_posterior_completada,
)
from botsito.domain.valores import Puntos
from botsito.domain.velas import MinutoUtc, Vela

RAIZ = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def registro() -> Registro:
    return cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")


def _v(k: int, abierta: int, alto: int, bajo: int, cierre: int) -> Vela:
    return Vela(MinutoUtc(k), Puntos(abierta), Puntos(alto), Puntos(bajo), Puntos(cierre), 1)


# Una compra: dos verdes a favor (la racha llega a 1010), una roja que deja el punto alto en 1010,
# y despues la M1 que mira el break even
RACHA_COMPRA = [
    _v(0, 1000, 1005, 999, 1004),
    _v(1, 1004, 1010, 1003, 1009),
    _v(2, 1009, 1009, 1001, 1002),
]
# Una venta, al reves: la racha baja a 990, una verde deja el punto bajo en 990
RACHA_VENTA = [_v(0, 1000, 1001, 995, 996), _v(1, 996, 997, 990, 991), _v(2, 991, 999, 991, 998)]


def test_el_registro_dice_al_cierre_y_con_cuerpo(registro: Registro) -> None:
    assert registro.opcion("break_even_condicion") == "cierre"
    assert registro.opcion("break_even_criterio_ruptura") == CUERPO


@pytest.mark.parametrize(
    ("racha", "lado", "mecha_sin_cierre", "cierre_mas_alla"),
    [
        # pasa 1010 con la mecha y cierra por debajo; cierra con cuerpo por encima
        (RACHA_COMPRA, COMPRA, _v(3, 1002, 1012, 1001, 1008), _v(3, 1002, 1013, 1001, 1011)),
        # pasa 990 con la mecha y cierra por encima; cierra con cuerpo por debajo
        (RACHA_VENTA, VENTA, _v(3, 998, 999, 988, 992), _v(3, 998, 999, 987, 989)),
    ],
)
def test_la_mecha_que_pasa_el_nivel_no_rompe_la_zona_y_el_cierre_mas_alla_si(
    registro: Registro,
    racha: list[Vela],
    lado: str,
    mecha_sin_cierre: Vela,
    cierre_mas_alla: Vela,
) -> None:
    criterio = registro.opcion("break_even_criterio_ruptura")
    # la mecha pasa el nivel y la vela cierra sin pasarlo: no hay break even (con `mecha`, si)
    assert zona_posterior_completada([*racha, mecha_sin_cierre], lado, criterio) is None
    assert zona_posterior_completada([*racha, mecha_sin_cierre], lado, MECHA) == 3
    # cierra con cuerpo mas alla del nivel: la zona se da por rota en esa vela, a su cierre
    assert zona_posterior_completada([*racha, cierre_mas_alla], lado, criterio) == 3


def test_sobre_las_m1_reales_el_toque_del_16_de_julio_ya_no_mueve_el_stop(
    registro: Registro,
) -> None:
    """2026-07-16, sesion de 11 a 15 (construccion): la compra o12 de la corrida de julio de la
    linea base (llenada a las 09:35:57 UTC) movia el stop a la entrada a las 09:39:10, al tocar el
    punto alto de la zona posterior (1.14634) con una M1 que cierra en 1.14629, sin pasarlo
    (ACTIVAR-SESION-07.md, F2). Con el cierre y el cuerpo, esa M1 no rompe la zona. Necesita las
    M1 de `data/`, fuera de git: sin ellas (la CI), se salta."""
    config = cargar_config(RAIZ / "knowledge" / "cases" / "kit" / "config.yaml")
    try:
        serie = cargar_serie(
            cargar_manifiesto(buscar_manifiesto(RAIZ, f"{config.dataset_prefijo}2026-07")),
            carpeta_datos(RAIZ),
        )
    except (DatasetError, FileNotFoundError, OSError) as exc:
        pytest.skip(f"sin las M1 de data/: {exc}")
    desde = int(datetime.fromisoformat("2026-07-16T09:35:00+00:00").timestamp()) // 60
    toque = int(datetime.fromisoformat("2026-07-16T09:39:00+00:00").timestamp()) // 60
    m1 = [v for v in serie.velas if desde <= int(v.inicio) <= toque]
    if len(m1) != toque - desde + 1:
        pytest.skip("faltan M1 de data/ en ese tramo")
    k = len(m1) - 1  # la M1 del toque
    assert zona_posterior_completada(m1, COMPRA, MECHA) == k  # lo de antes: la mecha la rompia
    assert (
        zona_posterior_completada(m1, COMPRA, registro.opcion("break_even_criterio_ruptura")) != k
    )
