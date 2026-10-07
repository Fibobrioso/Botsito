"""trabajo/guion-mismo-comando, fase 1: que los tests de la condicion fallan si se quita, y que
fallan LOS QUE TIENEN QUE FALLAR.

Sin tocar el codigo ni los tests: carga la guardia como el modulo que usan los tests
(`guardia_claude`), le cambia EN MEMORIA una pieza y corre los tests `ejecucion` de
`tests/unit/test_guardia_claude.py` dentro de este proceso. Las mutaciones:

- «sin la condicion»: `exigir_ejecucion_verificable` no hace nada. Tienen que fallar EXACTAMENTE
  todos los casos de los tests que esperan una negacion, y ninguno de los que esperan que pase;
- una por cada pieza con nombre de la condicion (`_exigir_sin_expansiones`, `_exigir_lo_de_antes`,
  `_exigir_lo_de_a_la_vez`, `_exigir_salida_ajena`) y «sin la existencia» (un guion que no existe
  pasa, como en `main`): tienen que fallar, al menos, los casos que solo esa pieza niega.

Con la condicion entera, todos pasan; restaurada cada mutacion, vuelven a pasar. Los tests corren
sobre el repositorio SINTETICO de su fixture: ningun material se abre y no se ejecuta ninguno de los
comandos que miden (revisor de la rama, A7: la primera version solo pedia «que falle algo»).

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

# Los tests que esperan una NEGACION: sin la condicion, fallan todos sus casos.
NIEGAN = (
    "test_ejecucion_cambiada_en_el_mismo_comando_se_niega",
    "test_ejecucion_cada_via_pasa_por_la_condicion",
    "test_ejecucion_lo_de_fuera_de_la_lista_se_niega",
    "test_ejecucion_un_guion_que_no_existe_dice_como_reescribirlo",
    "test_ejecucion_make_solo_con_el_makefile_de_main",
    "test_ejecucion_powershell_sin_ejecuciones_y_lo_demas_igual",
)
CAMBIADA = "test_ejecucion_cambiada_en_el_mismo_comando_se_niega"
FUERA = "test_ejecucion_lo_de_fuera_de_la_lista_se_niega"
# Lo que SOLO niega cada pieza (el guion existe y lo demas del comando esta en la lista).
ESPERADOS: dict[str, list[str]] = {
    "_exigir_sin_expansiones": [
        f"{CAMBIADA}[python existente.py <(cp a.py existente.py)]",
        f"{FUERA}[X=$Y python inocuo.py]",
        f"{FUERA}[X=$(echo 1) python inocuo.py]",
    ],
    "_exigir_lo_de_antes": [
        f"{CAMBIADA}[cp a.py existente.py && uv run python existente.py]",
        f"{CAMBIADA}[cp a.py scripts/otro.py && uv run python scripts/otro.py]",
        f"{FUERA}[inventado && python inocuo.py]",
        f"{FUERA}[grep hola docs/a.md && python inocuo.py]",
        f"{FUERA}[python inocuo.py && python existente.py]",
        f"{FUERA}[set -x; python inocuo.py]",
        # `cd && python inocuo.py` no: tras `cd` a secas (HOME) el guion tampoco existe, y lo
        # niegan las dos piezas.
    ],
    "_exigir_lo_de_a_la_vez": [
        f"{CAMBIADA}[python existente.py & cp a.py existente.py]",
        f"{FUERA}[python inocuo.py | tee salida.txt]",
        f"{FUERA}[python inocuo.py | sort -o salida.txt]",
        f"{FUERA}[python inocuo.py | uniq - salida.txt]",
        f"{FUERA}[python inocuo.py | inventado]",
    ],
    "_exigir_salida_ajena": [f"{CAMBIADA}[python existente.py > existente.py]"],
    "_exigir_guion_legible": [
        f"{FUERA}[python nuevo.py]",
        "test_ejecucion_un_guion_que_no_existe_dice_como_reescribirlo",
    ],
}


class Resultados:
    def __init__(self) -> None:
        self.por_test: dict[str, str] = {}

    def pytest_runtest_logreport(self, report: Any) -> None:
        if report.when == "call" or (report.when == "setup" and report.outcome != "passed"):
            self.por_test[report.nodeid.split("::", 1)[1]] = report.outcome


def correr() -> dict[str, str]:
    resultados = Resultados()
    argumentos = [str(TESTS), "-q", "-p", "no:cacheprovider", "-k", "ejecucion", "--no-header"]
    pytest.main([*argumentos, "-rN", "--tb=no"], plugins=[resultados])
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
        ("sin las expansiones", "_exigir_sin_expansiones", nada),
        ("sin lo de antes", "_exigir_lo_de_antes", nada),
        ("sin lo de a la vez", "_exigir_lo_de_a_la_vez", nada),
        ("sin la salida ajena", "_exigir_salida_ajena", nada),
        ("sin la existencia", "_exigir_guion_legible", guion_como_en_main),
    ]
    base = correr()
    niegan = {t for t in base if t.split("[", 1)[0] in NIEGAN}
    print(f"\n== con la condicion: {len(base)} tests, fallan {sum(r != 'passed' for r in base.values())}")
    print(f"   esperan una negacion: {len(niegan)}")
    ok = all(r == "passed" for r in base.values())
    for titulo, nombre, sustituta in mutaciones:
        original = getattr(g, nombre)
        setattr(g, nombre, sustituta)
        try:
            mutado = correr()
        finally:
            setattr(g, nombre, original)
        restaurado = correr()
        fallan = {t for t, r in mutado.items() if r != "passed"}
        print(f"\n== {titulo} ({nombre}): fallan {len(fallan)} de {len(mutado)}")
        if nombre == "exigir_ejecucion_verificable":
            exacto = fallan == niegan
            print(f"   fallan EXACTAMENTE los que esperan una negacion: {'si' if exacto else 'NO'}")
            for t in sorted(fallan ^ niegan):
                print(f"   DIFERENCIA  {t}")
            ok = ok and exacto
        else:
            faltan = [t for t in ESPERADOS[nombre] if t not in fallan]
            print(f"   de los {len(ESPERADOS[nombre])} que solo niega esta pieza, fallan "
                  f"{len(ESPERADOS[nombre]) - len(faltan)}")
            for t in faltan:
                print(f"   NO FALLA  {t}")
            ok = ok and not faltan
        for t in sorted(fallan):
            print(f"   FALLA  {t}")
        no_restaura = [t for t, r in restaurado.items() if r != "passed"]
        print(f"   restaurado: fallan {len(no_restaura)}")
        ok = ok and not no_restaura
    print(
        "\nVEREDICTO: "
        + (
            "sin la condicion fallan exactamente los que esperan una negacion; cada pieza rompe "
            "los suyos; restaurada, todo pasa"
            if ok
            else "NO"
        )
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
