"""Rompe a proposito, en los dos sentidos, los cuatro tests de la hoja 05 de
tests/unit/test_transcribir_sesion.py (`trabajo/hoja-sesion-05`, HOJA-SESION-05.md §2).

Carga `scripts/transcribir_sesion.py` y el modulo de tests de la raiz dada, y para cada test:
lo corre con el guion tal cual (tiene que pasar) y con dos mutaciones en memoria, una en cada
sentido (tiene que fallar). Cada mutacion se deshace antes de la siguiente. No escribe nada.

    uv run python docs/validation/anexos/HOJA-SESION-05/romper_tests.py <raiz del repo>
"""

import importlib.util
import sys
import traceback
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from pathlib import Path
from types import ModuleType
from typing import Any

raiz = Path(sys.argv[1]).resolve()


def _cargar(nombre: str, ruta: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


m = _cargar("transcribir_sesion", raiz / "scripts" / "transcribir_sesion.py")
t = _cargar("test_transcribir_sesion", raiz / "tests" / "unit" / "test_transcribir_sesion.py")


@contextmanager
def poner(obj: Any, clave: str, valor: Any) -> Iterator[None]:
    """Cambia un atributo (o una clave, si obj es un dict) y lo deja como estaba al salir."""
    if isinstance(obj, dict):
        antes = obj[clave]
        obj[clave] = valor
        try:
            yield
        finally:
            obj[clave] = antes
    else:
        antes = getattr(obj, clave)
        setattr(obj, clave, valor)
        try:
            yield
        finally:
            setattr(obj, clave, antes)


def correr(prueba: Callable[[ModuleType], None]) -> str:
    try:
        prueba(m)
    except AssertionError as e:
        # la linea del test en la que falla, para ver que cae en la asercion que toca
        marco = traceback.extract_tb(e.__traceback__)[-1]
        return f"FALLA en test_transcribir_sesion.py:{marco.lineno}: {marco.line}"
    return "pasa"


textos05 = m.CODIGOS_DE_SESION_TEXTO["05"]
titulo_del_cuerpo_s7 = "qué vela pones como 0 de la caja, y si la trazas con la vela abierta"
textos04 = m.CODIGOS_DE_SESION_TEXTO["04"]
sin_s25 = {k: v for k, v in textos05.items() if k != "S-25"}
con_s25 = {**textos04, "S-25": "x"}
orden04_cambiado = (m.ORDEN_SESION_04[1], m.ORDEN_SESION_04[0], *m.ORDEN_SESION_04[2:])

CASOS: list[tuple[str, Callable[[ModuleType], None], list[tuple[str, Any]]]] = [
    (
        "test_la_hoja_05_tiene_los_25_codigos_con_su_texto",
        t.test_la_hoja_05_tiene_los_25_codigos_con_su_texto,
        [
            ("S-7 con el titulo del cuerpo y no el del recuadro",
             poner(textos05, "S-7", titulo_del_cuerpo_s7)),
            ("sin S-25 (la hoja de 24 codigos)",
             poner(m.CODIGOS_DE_SESION_TEXTO, "05", sin_s25)),
        ],
    ),
    (
        "test_s25_vale_en_la_05_y_no_en_la_04",
        t.test_s25_vale_en_la_05_y_no_en_la_04,
        [
            ("S-25 tambien en la 04", poner(m.CODIGOS_DE_SESION_TEXTO, "04", con_s25)),
            ("S-25 fuera de la 05", poner(m.CODIGOS_DE_SESION_TEXTO, "05", sin_s25)),
        ],
    ),
    (
        "test_la_03_y_la_04_no_cambian",
        t.test_la_03_y_la_04_no_cambian,
        [
            ("la hoja 04 con S-1 y S-2 cambiados de sitio",
             poner(m.HOJAS, "04", orden04_cambiado)),
            ("el texto de S-1 de la 03 cambiado",
             poner(m.CODIGOS_DE_SESION_TEXTO["03"], "S-1", "otro texto")),
        ],
    ),
    (
        "test_la_sesion_en_curso_es_la_05",
        t.test_la_sesion_en_curso_es_la_05,
        [
            ("SESION_EN_CURSO = 04 (lo de main)", poner(m, "SESION_EN_CURSO", "04")),
            ("HOJAS['05'] con la hoja de la 04", poner(m.HOJAS, "05", m.ORDEN_SESION_04)),
        ],
    ),
]  # fmt: skip

malos = 0
for nombre, prueba, mutaciones in CASOS:
    tal_cual = correr(prueba)
    print(f"{nombre}: tal cual -> {tal_cual}")
    malos += tal_cual != "pasa"
    for descripcion, mutacion in mutaciones:
        with mutacion:
            salida = correr(prueba)
        print(f"  roto ({descripcion}) -> {salida}")
        malos += not salida.startswith("FALLA")
    print(f"  de nuevo tal cual -> {correr(prueba)}")
print("todo como se espera" if malos == 0 else f"{malos} resultados inesperados")
