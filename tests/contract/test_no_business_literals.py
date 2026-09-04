"""Ningun parametro de negocio vive fuera del registro (F02).

En F01 la lista de literales prohibidos esta vacia: el test existe para que F02 solo tenga que
rellenarla. Ver MASTER_PLAN F02.
"""

from pathlib import Path

import pytest

BUSINESS_LITERALS: dict[str, str] = {
    # "0.75": "nivel del stop en la caja (RN-021): debe leerse del registro",
}


@pytest.mark.contract
def test_no_business_literals_outside_registry(repo: Path) -> None:
    offenders: list[str] = []
    for py in (repo / "src" / "botsito").rglob("*.py"):
        if py.parts[-2] == "config":
            continue
        text = py.read_text(encoding="utf-8")
        offenders.extend(
            f"{py.name}: {lit} ({why})" for lit, why in BUSINESS_LITERALS.items() if lit in text
        )
    assert offenders == []
