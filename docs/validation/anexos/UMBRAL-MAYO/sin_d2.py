"""Que el test de «corrida con diagnostico» falla si se quita la condicion D2 (ADR-0070). Sin tocar
el codigo ni los tests: en memoria, se sustituye el veredicto que usa el arnes por uno que ignora
el diagnostico, y se ejecuta el test. Tiene que fallar. Despues se restaura y tiene que pasar.

No ejecuta `botsito motor arnes`: el test construye una corrida sintetica a mano.

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


def cargar_test():  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location("test_umbral_mayo", TEST)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def corre(test, nombre: str) -> str:  # type: ignore[no-untyped-def]
    try:
        getattr(test, nombre)()
    except AssertionError as exc:
        return f"FALLA ({str(exc).splitlines()[0][:100] if str(exc) else 'AssertionError'})"
    return "pasa"


def main() -> int:
    test = cargar_test()
    nombre = "test_una_corrida_con_diagnostico_que_llega_a_las_dos_sale_no"
    original = arnes.habilita_medir
    antes = corre(test, nombre)
    print(f"con D2 (el codigo tal cual): {nombre}: {antes}")

    def sin_d2(medida, criterio, meses, *, con_diagnostico):  # type: ignore[no-untyped-def]
        return criterio_fidelidad.habilita_medir(medida, criterio, meses, con_diagnostico=False)

    arnes.habilita_medir = sin_d2  # type: ignore[assignment]
    try:
        quitada = corre(test, nombre)
    finally:
        arnes.habilita_medir = original
    print(f"sin D2 (el diagnostico ignorado): {nombre}: {quitada}")
    despues = corre(test, nombre)
    print(f"restaurado: {nombre}: {despues}")
    ok = antes == "pasa" and quitada.startswith("FALLA") and despues == "pasa"
    print("VEREDICTO: " + ("el test falla si se quita D2" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
