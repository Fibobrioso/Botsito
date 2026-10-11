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


# `knowledge validate` sobre el repositorio real, UNA vez por sesion de pytest
# (trabajo/entorno-code, E3; respuesta del consultor del 2026-10-11, punto 1). Cuatro tests lo
# ejecutaban cada uno entero (unos 80 s cada vez): ahora el primero que lo pide lo calcula y
# los demas reciben el mismo resultado. Solo para el repositorio real; con cualquier otra raiz,
# `validar` corre de verdad. Un test que cambia una pieza de `validar` para ver que falla (G1,
# `test_citas_supersedidas.py`) no lo usa: un resultado compartido no puede mostrar eso.
@pytest.fixture(scope="session")
def validacion_del_repo() -> tuple[int, tuple[str, ...]]:
    """`validar(REPO)` una vez, con la guarda del holdout encendida y vigilada como en un test:
    los fixtures de sesion se crean ANTES que `holdout_guard`, asi que aqui se enciende a mano."""
    from botsito.validation import knowledge

    antes = (guarda_holdout.Estado.raiz, guarda_holdout.Estado.violaciones)
    guarda_holdout.Estado.raiz = RAIZ_HOLDOUT
    guarda_holdout.Estado.violaciones = []
    try:
        codigo, salida = knowledge.validar(REPO)
        vistas = list(guarda_holdout.Estado.violaciones)
    finally:
        guarda_holdout.Estado.raiz, guarda_holdout.Estado.violaciones = antes
    if vistas:
        pytest.fail(f"lectura de holdout en `knowledge validate`: {vistas}", pytrace=False)
    return codigo, tuple(salida)  # una tupla: ningun test puede cambiarla para los demas


@pytest.fixture
def knowledge_validate_compartido(
    validacion_del_repo: tuple[int, tuple[str, ...]], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Durante el test, `botsito.validation.knowledge.validar(REPO)` devuelve el resultado de
    sesion (una lista nueva cada vez); `cli.knowledge_validate` y `cli.main` la importan al
    llamarla, asi que lo reciben tal cual."""
    from botsito.validation import knowledge

    original = knowledge.validar

    def validar(repo: Path) -> tuple[int, list[str]]:
        if Path(repo).resolve() != REPO.resolve():
            return original(repo)
        codigo, salida = validacion_del_repo
        return codigo, list(salida)

    monkeypatch.setattr(knowledge, "validar", validar)
