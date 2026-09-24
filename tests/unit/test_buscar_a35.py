"""La busqueda de A-35 (`scripts/buscar_ambiguedades.py --conjunto a35`): su lista cerrada, sus
controles positivos y que el conjunto de A-24 no cambia, sin leer ninguna transcripcion real."""

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


def test_la_lista_de_a35_es_cerrada_y_sin_palabras_sueltas_de_uso_constante(m: ModuleType) -> None:
    b = m.base()
    assert set(m.TERMINOS_A35) == {"A-35"}
    terminos = m.TERMINOS_A35["A-35"]
    assert len(terminos) == len(set(terminos))
    for t in terminos:
        assert len(t.split()) >= 2, t  # solo frases o combinaciones
        assert b.normalizar(t) not in m.PROHIBIDOS, t


def test_el_conjunto_de_a24_no_cambia(m: ModuleType) -> None:
    # A-35 va aparte: sin `--conjunto`, la busqueda es la de A-24, A-21, A-26 y A-34, cuya salida
    # commiteada se reproduce byte a byte
    assert m.CONJUNTOS["a24"] is m.TERMINOS
    assert set(m.TERMINOS) == {"A-24", "A-21", "A-26", "A-34"}
    assert not set(m.TERMINOS) & set(m.TERMINOS_A35)


@pytest.mark.parametrize(
    "frase",
    [
        # v4 #846 y #849, y la cita de ev-v4-005053-885e2773
        "Uno ya formado",
        "Por encima de este ya formado",
        "Claro, buscamos, o sea Por encima de este ya formado Buscamos por encima del tray",
        # v4 #836, la pregunta que el trader contesto
        "¿tomas el último pico que ya se formó del todo o simplemente el punto más alto de las "
        "últimas velas aunque sigan en curso?",
    ],
)
def test_los_controles_positivos_de_a35_casan(m: ModuleType, frase: str) -> None:
    b = m.base()
    assert b.coincidencias([b.Segmento(0, 0, 4000, frase)], m.patrones("A-35"))


def test_la_cli_rechaza_un_conjunto_que_no_existe(m: ModuleType, tmp_path: Path) -> None:
    assert m.main(["--conjunto", "a99", "--salida", str(tmp_path / "x.txt")]) == 2
    assert not (tmp_path / "x.txt").exists()
