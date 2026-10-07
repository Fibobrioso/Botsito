"""Que los tests de D2 (ADR-0070, con sus enmiendas del 2026-10-07: la lista CERRADA de opciones y
la corrida SIMULADA con el perfil de la cuenta real y su primera fase) fallan si se quita cada
condicion. Sin tocar el codigo ni los tests: en memoria, se sustituye el veredicto que usa el arnes
por uno que ignora la condicion, y se ejecutan los tests que dependen de ella. Tienen que fallar.
Despues se restaura y tienen que pasar.

Dos mutaciones:
- «sin la lista»: el veredicto ignora las opciones fuera de la lista;
- «sin la simulacion»: el veredicto recibe siempre una simulacion valida (el perfil del criterio y
  su primera fase), corriera o no la corrida con --simular y con el perfil y la fase que fueran.

No ejecuta `botsito motor arnes`: los tests construyen corridas sinteticas a mano y solo PARSEAN
argumentos con el parser real.

Uso: uv run python docs/validation/anexos/UMBRAL-MAYO/sin_d2.py
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from botsito.cases import criterio_fidelidad
from botsito.cases.criterio_fidelidad import Simulacion
from botsito.engine import arnes

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ))
TEST = RAIZ / "tests" / "unit" / "test_umbral_mayo.py"


def sin_la_lista(medida, criterio, meses, *, opciones_fuera, simulacion):  # type: ignore[no-untyped-def]
    return criterio_fidelidad.habilita_medir(
        medida, criterio, meses, opciones_fuera=(), simulacion=simulacion
    )


def sin_la_simulacion(medida, criterio, meses, *, opciones_fuera, simulacion):  # type: ignore[no-untyped-def]
    valida = Simulacion(criterio.perfil_para_medir, "primera", "primera")
    return criterio_fidelidad.habilita_medir(
        medida, criterio, meses, opciones_fuera=opciones_fuera, simulacion=valida
    )


MUTACIONES = (
    (
        "sin la lista",
        sin_la_lista,
        (
            "test_una_corrida_con_diagnostico_que_llega_a_las_dos_sale_no",
            "test_depuracion_da_no",
            "test_una_opcion_nueva_del_parser_da_no_sin_tocar_la_lista",
            "test_una_opcion_del_parser_raiz_tambien_cuenta",
        ),
    ),
    (
        "sin la simulacion",
        sin_la_simulacion,
        (
            "test_sin_simular_da_no",
            "test_sin_simulacion_nunca_sale_si",
            "test_simular_con_otro_perfil_da_no",
            "test_simular_con_otra_fase_da_no",
        ),
    ),
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
    ok = True
    for titulo, mutada, nombres in MUTACIONES:
        print(f"-- {titulo}")
        for nombre in nombres:
            antes = corre(test, nombre)
            arnes.habilita_medir = mutada  # type: ignore[assignment]
            try:
                quitada = corre(test, nombre)
            finally:
                arnes.habilita_medir = original
            despues = corre(test, nombre)
            print(f"{nombre}: con la condicion {antes}; {titulo} {quitada}; restaurado {despues}")
            ok = ok and antes == "pasa" and quitada.startswith("FALLA") and despues == "pasa"
    print("VEREDICTO: " + ("los ocho tests fallan si se quita su condicion" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
