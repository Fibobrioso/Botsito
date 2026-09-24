"""La medida del instante del xlsx (`scripts/instante_llenado.py`), sobre velas SINTETICAS."""

from __future__ import annotations

import importlib.util
import sys
from datetime import UTC, datetime
from pathlib import Path
from types import ModuleType

import pytest

RAIZ = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def m() -> ModuleType:
    nombre = "instante_llenado"
    if nombre in sys.modules:
        return sys.modules[nombre]
    spec = importlib.util.spec_from_file_location(nombre, RAIZ / "scripts" / f"{nombre}.py")
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


T = datetime(2030, 1, 7, 9, 15, 42, tzinfo=UTC)


def _velas(m: ModuleType, rangos: dict[datetime, tuple[int, int]]):  # type: ignore[no-untyped-def]
    def vela_de(mes: str, instante: datetime) -> object:
        r = rangos.get(instante)
        return m.Rango(*r) if r else None

    return vela_de


def test_dentro_con_margen_y_el_minuto_se_redondea_hacia_abajo(m: ModuleType) -> None:
    minuto = T.replace(second=0)
    velas = _velas(m, {minuto: (100, 110)})
    for entrada, dentro in ((98, 1), (112, 1), (97, 0), (113, 0)):
        op = m.Operacion("2030-01", T, entrada)
        cuenta = m.tasas([op], velas, desplazamientos={"instante": 0})
        assert cuenta[("total", "instante")][0] == dentro


def test_sin_vela_se_cuenta_aparte_y_no_como_dentro(m: ModuleType) -> None:
    cuenta = m.tasas([m.Operacion("2030-01", T, 100)], _velas(m, {}))
    assert cuenta[("total", "instante")] == (0, 1, 1)


def _cuenta(dentro: int, controles: tuple[int, int], n: int = 10):  # type: ignore[no-untyped-def]
    menos, mas = controles
    return {
        ("total", "instante"): (dentro, n, 0),
        ("total", "-30 min"): (menos, n, 0),
        ("total", "+30 min"): (mas, n, 0),
    }


@pytest.mark.parametrize(
    ("dentro", "controles", "esperado"),
    [
        (10, (0, 1), "LLENADO"),
        (9, (1, 1), "LLENADO"),
        (5, (0, 0), "COLOCACION"),
        (7, (0, 1), "INDECISO"),
        (10, (6, 1), "NO VALE"),  # un control por encima de 50 %: no discrimina
        (4, (4, 0), "NO VALE"),  # un control igual a la tasa: no cae
    ],
)
def test_la_regla_fijada_y_el_control_manda(
    m: ModuleType, dentro: int, controles: tuple[int, int], esperado: str
) -> None:
    assert esperado in m.veredicto(_cuenta(dentro, controles))


def test_la_salida_no_trae_precios_ni_instantes(m: ModuleType) -> None:
    op = m.Operacion("2030-01", T, 123456)
    velas = _velas(m, {T.replace(second=0): (123450, 123460)})
    texto = "\n".join(m.lineas(m.tasas([op], velas)))
    assert "123456" not in texto and "09:15" not in texto and "2030-01-07" not in texto
