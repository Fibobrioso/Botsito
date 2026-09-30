"""El embudo de las 77 (`scripts/embudo_77.py`): clasificacion y tabla sobre casos SINTETICOS.

Ninguna vela ni ningun caso real se lee aqui: cada `Hechos` se escribe a mano para que la
operacion muera en un paso distinto, en el orden del pipeline, y la tabla que sale se fija entera.
"""

from __future__ import annotations

import importlib.util
import sys
from dataclasses import replace
from pathlib import Path
from types import ModuleType
from typing import Any

RAIZ = Path(__file__).resolve().parents[2]
TOL_PUNTOS, TOL_S = 3, 15 * 60
T = 1_900_000_000  # un instante sintetico, en segundos UTC


def _cargar() -> ModuleType:
    nombre = "embudo_77"
    if nombre in sys.modules:
        return sys.modules[nombre]
    spec = importlib.util.spec_from_file_location(nombre, RAIZ / "scripts" / f"{nombre}.py")
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def _base(e: ModuleType) -> Any:
    """Una compra que el bot acompana hasta el final: coincide."""
    return e.Hechos(
        sesion="07-11", direccion="compra", instante_s=T, entrada=1000, en_sesion=True,
        sesgo="alcista", tomas_rn004_s=(T - 1800,), toma_s=T - 1800, toma_sesion="07-11",
        zona_lado="compra", zona_entrada=1002, zona_formada_s=T - 600, sin_esquema=None,
        sin_orden=None,
        rechazo=None, llenada=True, pos_sesion="07-11", pos_abierta_s=T + 60, pos_entrada=1002,
        emparejada=True, bot_casa_con_otra=False,
    )  # fmt: skip


def test_cada_paso_en_el_orden_del_pipeline() -> None:
    e = _cargar()
    b = _base(e)
    s = replace(b, emparejada=False)
    casos = [
        (b, ("coincide", "coincide", "")),
        (replace(s, en_sesion=False), ("sesion", "fuera de la ventana de su sesion", "")),
        (replace(s, sesgo="ambiguo"), ("sesgo", "sin sesgo", "ambiguo")),
        (replace(s, sesgo="bajista"), ("sesgo", "sesgo contrario", "bajista")),
        (
            replace(s, toma_s=None, tomas_rn004_s=()),
            ("liquidez", "ninguna toma de M15 antes del trader", ""),
        ),
        (
            replace(s, toma_s=T + TOL_S + 60),
            ("liquidez", "RN-004 la fija y el productor no la registra", ""),
        ),
        (
            replace(s, toma_sesion="anterior", zona_entrada=1050),
            (
                "liquidez",
                "la del productor es de una sesion anterior y no usa las nuevas",
                "1 toma(s) nueva(s) en la sesion antes del trader",
            ),
        ),
        (
            replace(s, toma_sesion="anterior", zona_entrada=1050, tomas_rn004_s=()),
            (
                "liquidez",
                "la del productor es de una sesion anterior y en la sesion no hay otra",
                "",
            ),
        ),
        (
            replace(
                s,
                zona_lado=None,
                zona_entrada=None,
                zona_formada_s=None,
                sin_esquema="la primera ruptura deja mas zonas de control que el tope (RN-009): 8",
            ),
            (
                "breaker",
                "sin esquema: la primera ruptura deja mas zonas de control que el tope (RN-009)",
                "8",
            ),
        ),
        (replace(s, zona_entrada=1004), ("caja", "0 fuera de tolerancia", "4 puntos")),
        (
            replace(s, zona_formada_s=T + TOL_S + 60),
            ("momento", "el breaker cierra tarde", "16 min"),
        ),
        (replace(s, sin_orden="RN-011 no dispara"), ("reglas", "RN-011 no dispara", "")),
        (replace(s, rechazo="precio_invalido"), ("broker", "rechazo: precio_invalido", "")),
        (
            replace(s, llenada=False, pos_abierta_s=None, pos_entrada=None),
            ("llenado", "la orden no se llena", ""),
        ),
        (
            replace(s, pos_abierta_s=T + 20 * 60),
            ("llenado", "se llena fuera de la tolerancia de minutos", "20 min"),
        ),
        (
            replace(s, bot_casa_con_otra=True),
            ("llenado", "su operacion casa con otra del trader", ""),
        ),
    ]
    for hechos, esperado in casos:
        assert e.clasificar(hechos, TOL_PUNTOS, TOL_S) == esperado, esperado


def test_una_toma_de_la_sesion_anterior_con_zona_que_casa_no_mata() -> None:
    """La toma es de otra sesion, pero su zona casa con la del trader: sigue el embudo."""
    e = _cargar()
    h = replace(_base(e), emparejada=False, toma_sesion="anterior", rechazo="volumen")
    assert e.clasificar(h, TOL_PUNTOS, TOL_S) == ("broker", "rechazo: volumen", "")


def test_la_tabla_del_embudo() -> None:
    e = _cargar()
    clases = {
        "lectura_a": ["sesgo", "sesgo", "caja", "coincide"],
        "lectura_b": ["liquidez", "caja", "caja", "broker"],
    }
    assert e.tabla(clases) == [
        "| paso | lectura_a | lectura_b |",
        "|---|---|---|",
        "| 1. sesion | 0 | 0 |",
        "| 2. sesgo | 2 | 0 |",
        "| 3. liquidez | 0 | 1 |",
        "| 4. breaker | 0 | 0 |",
        "| 5. caja | 1 | 2 |",
        "| 6. momento | 0 | 0 |",
        "| 7. reglas | 0 | 0 |",
        "| 8. broker | 0 | 1 |",
        "| 9. llenado | 0 | 0 |",
        "| coincide | 1 | 0 |",
        "| total | 4 | 4 |",
    ]


def _vida(e: ModuleType, **cambios: Any) -> Any:
    """Una venta con la vida de la orden stop (ADR-0064) que el bot acompana hasta el final."""
    base = e.HechosVida(
        en_sesion=True, direccion="venta", sesgo="bajista", toma_s=T - 1800, instante_s=T,
        entrada=1000, ordenes=((1001, "llenada", T - 300, "venta", T + 30, 1001),),
        sin_orden=None, emparejada=False, bot_casa_con_otra=False,
    )  # fmt: skip
    return replace(base, **cambios)


def test_la_vida_de_la_orden_stop_en_el_orden_del_pipeline() -> None:
    """Con la orden en el punto, los pasos describen como nace, se reubica y se llena: cada caso
    muere en un paso distinto y en su orden."""
    e = _cargar()
    casos = [
        (_vida(e, emparejada=True), ("coincide", "coincide", "")),
        (_vida(e, en_sesion=False), ("sesion", "fuera de la ventana de su sesion", "")),
        (_vida(e, sesgo="alcista"), ("sesgo", "sesgo contrario", "alcista")),
        (
            _vida(e, toma_s=None),
            ("liquidez", "ninguna toma de M15 en la sesion antes del trader", ""),
        ),
        (
            _vida(e, ordenes=(), sin_orden="sin punto con caja"),
            ("nace", "sin punto con caja", ""),
        ),
        (
            _vida(e, ordenes=((1020, "llenada", T, "venta", T, 1020),)),
            ("punto", "el punto del bot no es el del trader", "el mas cercano a 20 puntos"),
        ),
        (
            _vida(e, ordenes=((1001, "rechazada", T, "venta", None, None),)),
            ("broker", "la orden en su precio se rechaza", ""),
        ),
        (
            _vida(e, ordenes=((1001, "cancelada", T, "venta", None, None),)),
            ("reubica", "la orden en su precio se cancela antes de llenarse", ""),
        ),
        (
            _vida(e, ordenes=((1001, "llenada", T, "venta", T + 3600, 1001),)),
            ("llenado", "se llena fuera de la tolerancia de minutos", "60 min"),
        ),
    ]
    for hechos, esperado in casos:
        assert e.clasificar_vida(hechos, TOL_PUNTOS, TOL_S) == esperado, esperado
    assert e.tabla({"x": ["nace", "coincide"]}, e.PASOS_VIDA)[5] == "| 4. nace | 1 |"
