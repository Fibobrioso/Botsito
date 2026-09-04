"""Fixtures compartidas."""

from __future__ import annotations

from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def repo() -> Path:
    return REPO


@pytest.fixture
def holdout_guard() -> None:
    """Guarda de la particion reservada. Se implementa y se hace autouse en F14.

    Cuando exista, fallara si cualquier modulo bajo botsito.spec o botsito.domain abre un
    fichero de knowledge/cases/holdout/.
    """
    return None
