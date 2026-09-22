"""Fixtures compartidas."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest

from tests import guarda_holdout

REPO = Path(__file__).resolve().parents[1]
RAIZ_HOLDOUT = REPO / "knowledge" / "cases" / "holdout"
# El material del trader vive en `corpus/`, fuera de git, y hasta el 2026-09-21 NADA impedia
# que un test abriera el xlsx de mayo: la guarda solo miraba la carpeta del holdout. ADR-0033
# lo dejo escrito -"el dia que F14 escriba la ingesta, pasa por la puerta"- y ese dia es hoy.
RAIZ_MATERIAL = REPO / "corpus" / "Estrategia del trader" / "Material adicional de su operativa"


@pytest.fixture(scope="session")
def repo() -> Path:
    return REPO


def pytest_configure(config: pytest.Config) -> None:
    guarda_holdout.instalar()


@pytest.fixture(autouse=True)
def holdout_guard(request: pytest.FixtureRequest) -> Iterator[type[guarda_holdout.Estado]]:
    """La guarda del holdout, encendida en TODOS los tests (F14 D4, ADR-0033).

    Hasta el 2026-09-17 era un stub que devolvia None con la promesa de implementarse en F14. Ahora
    vigila cualquier apertura de `knowledge/cases/holdout/{1,2,3}/` salvo su `README.md`, venga de
    quien venga. Si un test la provoca y se traga la excepcion, falla igual al terminar. Un test que
    la provoca A PROPOSITO -para verla saltar- se marca `provoca_holdout` y reapunta la raiz a un
    holdout sintetico: nunca al del repositorio.
    """
    guarda_holdout.Estado.raiz = RAIZ_HOLDOUT
    guarda_holdout.Estado.violaciones = []
    yield guarda_holdout.Estado
    vistas = list(guarda_holdout.Estado.violaciones)
    guarda_holdout.Estado.raiz = None
    guarda_holdout.Estado.violaciones = []
    if vistas and not request.node.get_closest_marker("provoca_holdout"):
        pytest.fail(
            f"lectura de holdout durante el test, aunque se tragara la excepcion: {vistas}",
            pytrace=False,
        )
