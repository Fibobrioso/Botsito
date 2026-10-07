"""Que el test de «corrida con diagnostico» falla si se quita la condicion D2 (ADR-0070, con su
enmienda del 2026-10-07: la lista CERRADA de opciones). Sin tocar el codigo ni los tests: en
memoria, se sustituye el veredicto que usa el arnes por uno que ignora las opciones fuera de la
lista, y se ejecutan los tests que dependen de D2. Tienen que fallar. Despues se restaura y tienen
que pasar.

No ejecuta `botsito motor arnes`: los tests construyen corridas sinteticas a mano y solo PARSEAN
argumentos con el parser real.

Uso: uv run python docs/validation/anexos/UMBRAL-MAYO/sin_d2.py
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from botsito.cases import criterio_fidelidad
from botsito.engine import arnes

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ))
TEST = RAIZ / "tests" / "unit" / "test_umbral_mayo.py"
NOMBRES = (
    "test_una_corrida_con_diagnostico_que_llega_a_las_dos_sale_no",
    "test_depuracion_da_no",
    "test_una_opcion_nueva_del_parser_da_no_sin_tocar_la_lista",
)


def cargar_test():  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location("test_umbral_mayo", TEST)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def corre(test, nombre: str) -> str:  # type: ignore[no-untyped-def]
    try:
        getattr(test, nombre)()
    except AssertionError:
        return "FALLA (AssertionError)"
    return "pasa"


def main() -> int:
    test = cargar_test()
    original = arnes.habilita_medir

    def sin_d2(medida, criterio, meses, *, opciones_fuera):  # type: ignore[no-untyped-def]
        return criterio_fidelidad.habilita_medir(medida, criterio, meses, opciones_fuera=())

    ok = True
    for nombre in NOMBRES:
        antes = corre(test, nombre)
        arnes.habilita_medir = sin_d2  # type: ignore[assignment]
        try:
            quitada = corre(test, nombre)
        finally:
            arnes.habilita_medir = original
        despues = corre(test, nombre)
        print(f"{nombre}: con D2 {antes}; sin D2 {quitada}; restaurado {despues}")
        ok = ok and antes == "pasa" and quitada.startswith("FALLA") and despues == "pasa"
    print("VEREDICTO: " + ("los tres tests fallan si se quita D2" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
