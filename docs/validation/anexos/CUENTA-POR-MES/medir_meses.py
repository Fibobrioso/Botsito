"""Fase 0 de trabajo/cuenta-por-mes, c): que meses corre cada MotorCableado de los tests. Un espia
de `correr_dia` (solo anota) y pytest.main con el plugin como objeto. Se lanzo desde la carpeta de
trabajo de la sesion; aqui, la copia (con la salida en LF)."""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import pytest

SALIDA = Path(__file__).with_name("meses.txt")


class Espia:
    def __init__(self) -> None:
        self.actual = ""
        self.por_test: dict[str, dict[int, set[str]]] = defaultdict(lambda: defaultdict(set))
        from botsito.engine import cableado

        original = cableado.MotorCableado.correr_dia
        espia = self

        def correr_dia(motor, dia):  # type: ignore[no-untyped-def]
            espia.por_test[espia.actual][id(motor)].add(dia.dia.isoformat()[:7])
            return original(motor, dia)

        cableado.MotorCableado.correr_dia = correr_dia  # type: ignore[method-assign]

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_call(self, item):  # type: ignore[no-untyped-def]
        self.actual = item.nodeid
        yield

    def pytest_sessionfinish(self, session, exitstatus):  # type: ignore[no-untyped-def]
        lineas = [f"tests que corren el motor cableado: {len(self.por_test)}"]
        varios = 0
        todos: set[str] = set()
        for t in sorted(self.por_test):
            for meses in self.por_test[t].values():
                todos |= meses
                if len(meses) > 1:
                    varios += 1
                    lineas.append(f"VARIOS MESES: {t}: {sorted(meses)}")
        lineas.append(f"motores con mas de un mes: {varios}")
        lineas.append(f"meses vistos en total: {sorted(todos)}")
        lineas.append(f"exit de pytest: {exitstatus}")
        SALIDA.write_text("\n".join(lineas) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    sys.exit(pytest.main(["-q", "-p", "no:cacheprovider", "tests/unit"], plugins=[Espia()]))
