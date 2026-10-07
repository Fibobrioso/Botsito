"""trabajo/guion-mismo-comando, fase 1: que los tests de la condicion fallan si se quita.

Sin tocar el codigo ni los tests: carga la guardia como el modulo que usan los tests
(`guardia_claude`), le cambia EN MEMORIA una pieza y corre los tests `ejecucion` de
`tests/unit/test_guardia_claude.py` dentro de este proceso. Tres mutaciones:

- «sin la condicion»: `exigir_ejecucion_verificable` no hace nada (como si ninguna via la llamara);
- «sin lo de antes»: `_exigir_comando_verificable` no hace nada (ni la lista cerrada, ni las
  sustituciones, ni lo que corre a la vez, ni la salida al propio guion);
- «sin la existencia»: un guion que no existe pasa, como en `main` (se lee como vacio).

Con la condicion entera, todos pasan; con cada mutacion, los que dependen de ella fallan; y
restaurada, vuelven a pasar. Los tests corren sobre el repositorio SINTETICO de su fixture: ningun
material se abre y no se ejecuta ninguno de los comandos que miden.

Uso: uv run python docs/validation/anexos/GUION-MISMO-COMANDO/sin_condicion.py
"""

from __future__ import annotations

import importlib.util
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

RAIZ = Path(__file__).resolve().parents[4]
GUARDIA = RAIZ / ".claude" / "hooks" / "guardia.py"
TESTS = RAIZ / "tests" / "unit" / "test_guardia_claude.py"


class Resultados:
    def __init__(self) -> None:
        self.por_test: dict[str, str] = {}

    def pytest_runtest_logreport(self, report: Any) -> None:
        if report.when == "call" or (report.when == "setup" and report.outcome != "passed"):
            self.por_test[report.nodeid.split("::", 1)[1]] = report.outcome


def correr() -> dict[str, str]:
    resultados = Resultados()
    pytest.main(
        [
            str(TESTS),
            "-q",
            "-p",
            "no:cacheprovider",
            "-k",
            "ejecucion",
            "--no-header",
            "-rN",
            "--tb=no",
        ],
        plugins=[resultados],
    )
    return resultados.por_test


def main() -> int:
    spec = importlib.util.spec_from_file_location("guardia_claude", GUARDIA)
    assert spec is not None and spec.loader is not None
    g = importlib.util.module_from_spec(spec)
    sys.modules["guardia_claude"] = g  # el fixture `g` de los tests reutiliza este modulo
    spec.loader.exec_module(g)

    original_guion = g._exigir_guion_legible

    def guion_como_en_main(ctx: Any, lex: Any, que: str, palabra: Any, lenguaje: str) -> bool:
        valores = g._valores(palabra, ctx, lex) or []
        if len(valores) == 1 and not Path(g._absoluta(valores[0], ctx.cwd)).exists():
            return False
        resultado: bool = original_guion(ctx, lex, que, palabra, lenguaje)
        return resultado

    def nada(*_args: Any, **_kwargs: Any) -> bool:
        return True

    mutaciones: list[tuple[str, str, Callable[..., Any]]] = [
        ("sin la condicion", "exigir_ejecucion_verificable", nada),
        ("sin lo de antes", "_exigir_comando_verificable", nada),
        ("sin la existencia", "_exigir_guion_legible", guion_como_en_main),
    ]
    base = correr()
    print(f"\n== con la condicion: {len(base)} tests, fallan {sum(r != 'passed' for r in base.values())}")
    ok = all(r == "passed" for r in base.values())
    for titulo, nombre, sustituta in mutaciones:
        original = getattr(g, nombre)
        setattr(g, nombre, sustituta)
        try:
            mutado = correr()
        finally:
            setattr(g, nombre, original)
        restaurado = correr()
        fallan = sorted(t for t, r in mutado.items() if r != "passed")
        print(f"\n== {titulo} ({nombre}): fallan {len(fallan)} de {len(mutado)}")
        for t in fallan:
            print(f"   FALLA  {t}")
        no_restaura = [t for t, r in restaurado.items() if r != "passed"]
        print(f"   restaurado: fallan {len(no_restaura)}")
        ok = ok and bool(fallan) and not no_restaura
    print("\nVEREDICTO: " + ("cada mutacion rompe sus tests y restaurada pasan" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
