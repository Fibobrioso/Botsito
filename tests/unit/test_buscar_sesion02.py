"""La busqueda de los candidatos de la sesion 02 (`scripts/buscar_ambiguedades.py --conjunto
sesion02`): su lista cerrada, sus controles positivos y que los conjuntos de A-24 y A-35 no
cambian, sin leer ninguna transcripcion real."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

RAIZ = Path(__file__).resolve().parents[2]
CANDIDATOS = {"C-01", "C-02", "C-04", "C-05", "C-06", "C-07"}


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


def test_la_lista_es_cerrada_y_sin_palabras_sueltas(m: ModuleType) -> None:
    b = m.base()
    assert set(m.TERMINOS_SESION02) == CANDIDATOS
    for candidato, terminos in m.TERMINOS_SESION02.items():
        assert len(terminos) == len(set(terminos)), candidato
        for t in terminos:
            assert len(t.split()) >= 2, (candidato, t)  # solo frases o combinaciones
            assert b.normalizar(t) not in m.PROHIBIDOS, (candidato, t)


def test_los_conjuntos_anteriores_no_cambian(m: ModuleType) -> None:
    # Sin `--conjunto`, A-24/A-21/A-26/A-34; con `a35`, A-35. Sus salidas commiteadas se
    # reproducen byte a byte: el conjunto nuevo va aparte y no comparte claves con ellos.
    assert m.CONJUNTOS["a24"] is m.TERMINOS
    assert m.CONJUNTOS["a35"] is m.TERMINOS_A35
    assert m.CONJUNTOS["sesion02"] is m.TERMINOS_SESION02
    assert set(m.TERMINOS) == {"A-24", "A-21", "A-26", "A-34"}
    assert set(m.TERMINOS_A35) == {"A-35"}
    assert not CANDIDATOS & (set(m.TERMINOS) | set(m.TERMINOS_A35))


@pytest.mark.parametrize(
    ("candidato", "frase"),
    [
        # ev-v3-004201-bfeb3734, la cita de `colocar_orden_limite` en la spec
        ("C-01", "apenas el breaker, o sea, marco mi orden limit y ya está"),
        # v1 #192, la frase de ev-v1-001454-69cebe62 en A35-PIVOTE-FORMADO-CLASIFICACION.md
        ("C-02", "Desde el punto más abajo te genera la vela contraria"),
        # ev-v4-003350-acb03ee7, la cita del cuestionario de la sesion 01
        ("C-07", "entonces en un día como máximo dos entradas ¿no? por separado"),
    ],
)
def test_los_controles_positivos_casan(m: ModuleType, candidato: str, frase: str) -> None:
    b = m.base()
    assert b.coincidencias([b.Segmento(0, 0, 4000, frase)], m.patrones(candidato))


def test_una_cifra_no_casa_dentro_de_otra(m: ModuleType) -> None:
    b = m.base()
    assert b.coincidencias([b.Segmento(0, 0, 4000, "el nivel 1 de la caja")], m.patrones("C-02"))
    assert not b.coincidencias([b.Segmento(0, 0, 4000, "el nivel 10")], m.patrones("C-02"))


def test_la_cli_rechaza_un_conjunto_que_no_existe(m: ModuleType, tmp_path: Path) -> None:
    assert m.main(["--conjunto", "sesion99", "--salida", str(tmp_path / "x.txt")]) == 2
    assert not (tmp_path / "x.txt").exists()
