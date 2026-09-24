"""La busqueda de A-24, A-21, A-26 y A-34 (`scripts/buscar_ambiguedades.py`): el corte a 180 s, la
lista cerrada de terminos y los controles positivos, sin leer ninguna transcripcion real."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

RAIZ = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def m() -> ModuleType:
    nombre = "buscar_ambiguedades"
    if nombre in sys.modules:
        return sys.modules[nombre]
    spec = importlib.util.spec_from_file_location(nombre, RAIZ / "scripts" / f"{nombre}.py")
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def _seg(b: ModuleType, n: int, t_s: int, texto: str) -> object:
    return b.Segmento(n, t_s * 1000, t_s * 1000 + 4000, texto)


def test_la_union_de_mas_de_180_s_se_corta_y_cada_trozo_lista_lo_suyo(m: ModuleType) -> None:
    b = m.base()
    # cuatro coincidencias a 60 s: sus ventanas de +-45 s se solapan y se unen en una de ~274 s
    segs = [_seg(b, i, 100 + 60 * i, "zona limpia") for i in range(4)]
    pats = m.patrones("A-21")
    sin_corte = b.pasajes("tr-x", segs, pats)
    assert len(sin_corte) == 1 and sin_corte[0].t1_ms - sin_corte[0].t0_ms > m.MAXIMO_MS
    cortados = b.pasajes("tr-x", segs, pats, m.MAXIMO_MS)
    assert len(cortados) == 2
    assert all(p.t1_ms - p.t0_ms <= m.MAXIMO_MS for p in cortados)
    assert cortados[0].t1_ms == cortados[1].t0_ms  # consecutivos
    assert sum(p.terminos["zona limpia"] for p in cortados) == 4  # ninguna se pierde ni se repite


def test_un_trozo_sin_coincidencias_propias_no_se_emite(m: ModuleType) -> None:
    b = m.base()
    segs = [_seg(b, 0, 100, "zona limpia"), _seg(b, 1, 300, "hace ruido")]
    # dos coincidencias a 200 s: no se solapan, salen dos pasajes normales
    assert len(b.pasajes("tr-x", segs, m.patrones("A-21"), m.MAXIMO_MS)) == 2


def test_sin_corte_a18_no_cambia(m: ModuleType) -> None:
    b = m.base()
    segs = [_seg(b, 0, 100, "el stop"), _seg(b, 1, 180, "el riesgo")]
    assert b.pasajes("tr-x", segs) == b.pasajes("tr-x", segs, None, None)


def test_la_lista_cerrada_no_tiene_palabras_sueltas_de_uso_constante(m: ModuleType) -> None:
    b = m.base()
    for amb, terminos in m.TERMINOS.items():
        assert len(terminos) == len(set(terminos)), amb
        for t in terminos:
            assert b.normalizar(t) not in m.PROHIBIDOS, (amb, t)
    assert set(m.TERMINOS) == {"A-24", "A-21", "A-26", "A-34"}


@pytest.mark.parametrize(
    ("amb", "frase"),
    [
        ("A-21", "sea una zona limpia"),
        ("A-24", "la zona de liquidez tiene que ser la más reciente"),
        ("A-26", "vela bajista envuelve a la vela anterior"),
        ("A-34", "lo fija la vela de 4 previa cerrada"),
    ],
)
def test_los_controles_positivos_casan_con_su_lista(m: ModuleType, amb: str, frase: str) -> None:
    b = m.base()
    assert b.coincidencias([_seg(b, 0, 0, frase)], m.patrones(amb))
