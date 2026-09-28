"""Control sintetico del metodo de `scripts/orden_stop_o_limite.py` (Fase 2): con una serie de ticks
INVENTADA -precios y dia que no son de ningun dia real- el precio que SUBE hasta un nivel de venta
tiene que salir LIMITE, y el que BAJA hasta el, STOP. Y si cruza el nivel por los dos lados dentro
de la ventana, ambiguo. Pedido por el consultor el 2026-09-27 como control positivo, porque las
etiquetas reales de FX Replay con las que se contrasto eran todas stop."""

from __future__ import annotations

import importlib.util
import sys
from datetime import UTC, datetime
from pathlib import Path
from types import ModuleType

import pytest

from botsito.domain.ticks import MilisegundoUtc, Tick
from botsito.domain.valores import Puntos
from botsito.domain.velas import MinutoUtc, Vela

RAIZ = Path(__file__).resolve().parents[2]
SCRIPT = RAIZ / "scripts" / "orden_stop_o_limite.py"
DIA = "2030-01-07"  # un dia que no existe en ningun dataset del proyecto
NIVEL = 100000  # 1.00000: ningun precio real de EURUSD en 2026
TOL = 2


@pytest.fixture(scope="module")
def m() -> ModuleType:
    nombre = "orden_stop_o_limite"
    if nombre in sys.modules:
        return sys.modules[nombre]
    spec = importlib.util.spec_from_file_location(nombre, SCRIPT)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def _t(hhmmss: str) -> datetime:
    return datetime.fromisoformat(f"{DIA}T{hhmmss}+00:00")


def _serie(desfases: list[int], t_ms: int, spread: int = 1) -> list[Tick]:
    """Un tick cada dos segundos, del mas antiguo al mas reciente, con bid = NIVEL + desfase y ask
    = bid + spread; el ultimo cae en t."""
    n = len(desfases)
    return [
        Tick(
            MilisegundoUtc(t_ms - (n - 1 - i) * 2000),
            Puntos(NIVEL + d + spread),
            Puntos(NIVEL + d),
            1000,
            1000,
        )
        for i, d in enumerate(desfases)
    ]


SUBE = [-12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0]  # llega de ABAJO
BAJA = [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]  # llega de ARRIBA
CRUZA = [8, 6, 4, 2, 0, -4, -6, -3, 0, 3, 5, 2, 0]  # por los dos lados


def test_las_funciones_puras_distinguen_los_dos_lados(m: ModuleType) -> None:
    assert m.lado_llegada([NIVEL + d for d in SUBE], NIVEL, TOL) == m.ABAJO
    assert m.lado_llegada([NIVEL + d for d in BAJA], NIVEL, TOL) == m.ARRIBA
    assert m.lado_llegada([NIVEL + d for d in CRUZA], NIVEL, TOL) == m.AMBIGUO
    assert m.lado_llegada([NIVEL, NIVEL + 1, NIVEL - 1], NIVEL, TOL) is None
    # venta: de arriba STOP, de abajo LIMITE; compra al reves
    assert m.tipo_de("venta", m.ARRIBA) == m.STOP
    assert m.tipo_de("venta", m.ABAJO) == m.LIMITE
    assert m.tipo_de("compra", m.ABAJO) == m.STOP
    assert m.tipo_de("compra", m.ARRIBA) == m.LIMITE
    assert m.tipo_de("venta", m.AMBIGUO) == m.AMBIGUO
    assert m.tipo_de("venta", None) == m.SIN_DATOS


@pytest.mark.parametrize(
    ("direccion", "desfases", "esperado"),
    [
        ("venta", SUBE, "LIMITE"),  # el precio SUBE hasta el nivel de venta: orden limite
        ("venta", BAJA, "STOP"),  # el precio BAJA hasta el nivel de venta: orden stop
        ("compra", BAJA, "LIMITE"),  # una compra a la que el precio BAJA: limite
        ("compra", SUBE, "STOP"),  # una compra a la que el precio SUBE: stop
        ("venta", CRUZA, "ambiguo"),
        ("compra", CRUZA, "ambiguo"),
    ],
)
def test_la_fase_2_de_punta_a_punta_con_ticks_inventados(
    m: ModuleType, direccion: str, desfases: list[int], esperado: str
) -> None:
    instante = _t("10:30:00")
    t_ms = int(instante.astimezone(UTC).timestamp() * 1000)
    serie = _serie(desfases, t_ms)
    op = m.Op(DIA, "11-15", direccion, "1.00000", instante)
    m.fase2([op], lambda dia: serie if dia == DIA else [], {}, TOL)
    assert (op.fuente, op.ventana, op.tipo) == ("ticks", "60 s", esperado)


def test_sin_ticks_en_la_ventana_cae_a_m1_y_lo_dice(m: ModuleType) -> None:
    instante = _t("10:30:00")
    minuto = int(instante.timestamp() // 60)
    # la vela anterior cierra por encima del nivel: una venta que llega de arriba es STOP
    velas = [
        Vela(
            MinutoUtc(minuto - 1),
            Puntos(NIVEL + 9),
            Puntos(NIVEL + 10),
            Puntos(NIVEL + 5),
            Puntos(NIVEL + 8),
            1,
        ),
        Vela(
            MinutoUtc(minuto),
            Puntos(NIVEL + 7),
            Puntos(NIVEL + 8),
            Puntos(NIVEL - 2),
            Puntos(NIVEL),
            1,
        ),
    ]
    op = m.Op(DIA, "07-11", "venta", "1.00000", instante)
    m.fase2([op], lambda dia: [], {DIA[:7]: velas}, TOL)
    assert (op.fuente, op.ventana, op.tipo) == ("M1", "vela anterior", "STOP")
