"""A-21 RESUELTA (sesion 4, S-10; ADR-0076): «limpia» es «sin alternancia de colores», y eso es lo
que RN-009 ya filtra con zonas_control_max_por_esquema = 1, porque cada paso de vela contraria a
vela del color de la entrada forma una zona de control. La tabla de series sinteticas de la
respuesta del consultor (2026-10-12, punto 0), en compra y en venta: por cada serie, lo que da
`detectar_esquema` con `solo_una_zona_de_control` y el tope de RN-009, y lo que daria la
comprobacion literal «ningun cambio de color en el retroceso» (solo como medida). Las unicas
diferencias salian de la vela de cuerpo cero en medio y del breaker contrario que rompe con mecha:
las dos preguntas de la sesion 5. Desde ADR-0085 (2026-10-26) la vela de cuerpo cero ya no es una
diferencia: el trader dijo que no cuenta como alternancia (S-19), y queda solo el breaker por
mecha (S-20, a la sesion 6)."""

from __future__ import annotations

from pathlib import Path

import pytest

from botsito.config.registro import cargar_registro
from botsito.domain.estructura_m1 import (
    COMPRA,
    LECTURAS_LIMPIA,
    MECHA,
    PRIMER_ESQUEMA,
    SEGUNDO_ESQUEMA,
    SOLO_UNA_ZONA_DE_CONTROL,
    VENTA,
    _pasa,
    bloque_de_origen,
    detectar_esquema,
    referencia_del_breaker,
    zonas_de_control,
)
from botsito.domain.pivotes_m15 import color
from botsito.domain.velas import Vela
from tests.unit.test_estructura_m1 import PREVIO, TOMA, _serie

RAIZ = Path(__file__).resolve().parents[2]
Paso = tuple[int, int] | tuple[int, int, int | None, int | None]
# Una venta: un tramo previo que deja un BAJO de M1 en 980 y la subida que toma la liquidez (la
# toma es la vela 4), espejo de PREVIO (p -> 2100 - p)
PREVIO_VENTA: list[Paso] = [
    (1100, 1050),
    (1050, 1000),
    (1000, 981, 980, None),
    (981, 1040),
    (1040, 1110),
]
NONE = "None"


def _espejo(pasos: list[Paso]) -> list[Paso]:
    """La misma serie para una venta: cada precio p -> 2100 - p; el minimo pasa a maximo."""
    salida: list[Paso] = []
    for p in pasos:
        a, c = 2100 - p[0], 2100 - p[1]
        lo = None if len(p) < 3 or p[2] is None else 2100 - p[2]
        hi = None if len(p) < 4 or p[3] is None else 2100 - p[3]
        salida.append((a, c, hi, lo))
    return salida


# (nombre, pasos tras la toma en compra, esquema esperado o None, zonas, literal limpia,
#  colores del tramo literal en compra -en venta, los mismos en espejo-, igual)
SERIES: list[tuple[str, list[Paso], str, int, bool, str, bool]] = [
    (
        "S-10: V, R, V, R y breaker V",
        [(990, 1040), (1040, 1020), (1020, 1050), (1050, 1030), (1030, 1119, None, 1125)],
        NONE, 2, False, "RVR", True,
    ),
    (
        "retroceso limpio de un solo bloque (R, R) y breaker V",
        [(990, 1040), (1040, 1020), (1020, 1010, 1005, None), (1010, 1060),
         (1060, 1119, None, 1125)],
        SEGUNDO_ESQUEMA, 1, True, "RR", True,
    ),
    (
        "una zona de control y el ultimo tramo limpio (V, R, V, breaker V)",
        [(990, 1040), (1040, 1020), (1020, 1060), (1060, 1119, None, 1125)],
        SEGUNDO_ESQUEMA, 1, True, "R", True,
    ),
    (
        "doble alternancia (V, R, V, R, V, R) y breaker V",
        [(990, 1040), (1040, 1020), (1020, 1050), (1050, 1030), (1030, 1060), (1060, 1040),
         (1040, 1119, None, 1125)],
        NONE, 3, False, "RVRVR", True,
    ),
    (
        "breaker contrario (R) que rompe con mecha, retroceso limpio (R, R)",
        [(990, 1040), (1040, 1020), (1020, 1010), (1010, 1005, None, 1125)],
        PRIMER_ESQUEMA, 0, True, "RRR", True,
    ),
    (
        "alternancia con cuerpo cero en medio (R, doji, V, R) y breaker V",
        [(990, 1040), (1040, 1020), (1020, 1020), (1020, 1050), (1050, 1030),
         (1030, 1119, None, 1125)],
        # ADR-0085 (sesion 5, S-19): el doji no corta la racha ni cuenta como alternancia, asi que
        # da lo mismo que R, V, R (S-10). Hasta el 2026-10-26: segundo esquema con 1 zona, DISTINTO
        NONE, 2, False, "RVR", True,
    ),
    (
        "breaker contrario (R) que rompe con mecha tras alternancia (R, V)",
        [(990, 1040), (1040, 1020), (1020, 1050), (1050, 1030, None, 1125)],
        SEGUNDO_ESQUEMA, 1, False, "RVR", False,  # el bloque de origen es el propio breaker
    ),
]  # fmt: skip
ESPEJO_DE_COLORES = str.maketrans("VR", "RV")


def sin_alternancia_literal(
    m1: list[Vela], idx_toma: int, lado: str, criterio: str
) -> tuple[bool | None, str]:
    """La lectura literal de la PARADA, solo como medida: desde la primera vela contraria posterior
    al primer impulso hasta el bloque de origen (incluido), saltando las de cuerpo cero, ningun
    cambio de color. (limpia, colores del tramo), o (None, '') si no hay breaker."""
    signo = 1 if lado == COMPRA else -1
    referencia = referencia_del_breaker(m1, idx_toma + 1, lado)
    if referencia is None:
        return None, ""
    i = next(
        (k for k in range(idx_toma + 1, len(m1)) if _pasa(m1[k], referencia, lado, criterio)), None
    )
    if i is None:
        return None, ""
    bloque = bloque_de_origen(m1, i, lado)
    if bloque is None:
        return None, ""
    primer_impulso = next((k for k in range(idx_toma + 1, i + 1) if color(m1[k]) == signo), None)
    if primer_impulso is None:
        return None, ""
    primera_contraria = next(
        (k for k in range(primer_impulso + 1, bloque[1]) if color(m1[k]) == -signo), None
    )
    if primera_contraria is None:
        return True, ""
    colores = [color(v) for v in m1[primera_contraria : bloque[1]] if color(v) != 0]
    letras = "".join({1: "V", -1: "R"}[c] for c in colores)
    return all(c == colores[0] for c in colores), letras


@pytest.mark.parametrize(
    ("nombre", "pasos", "esquema", "zonas", "limpia", "letras", "igual"), SERIES
)
@pytest.mark.parametrize("lado", [COMPRA, VENTA])
def test_la_tabla_de_series_de_a21(
    nombre: str,
    pasos: list[Paso],
    esquema: str,
    zonas: int,
    limpia: bool,
    letras: str,
    igual: bool,
    lado: str,
) -> None:
    previo = PREVIO if lado == COMPRA else PREVIO_VENTA
    m1 = _serie([*previo, *(pasos if lado == COMPRA else _espejo(pasos))])
    e = detectar_esquema(m1, TOMA, lado, MECHA, 1, SOLO_UNA_ZONA_DE_CONTROL)
    assert zonas_de_control(m1, TOMA, len(m1) - 1, lado) == zonas, nombre
    assert (NONE if e is None else e.cual) == esquema, nombre
    literal, tramo = sin_alternancia_literal(m1, TOMA, lado, MECHA)
    assert tramo == (letras if lado == COMPRA else letras.translate(ESPEJO_DE_COLORES)), nombre
    assert literal is limpia, (nombre, tramo)
    assert ((e is not None) == literal) is igual, (nombre, tramo)


def test_las_diferencias_son_solo_el_doji_y_el_breaker_por_mecha() -> None:
    """El caso (b) de la respuesta del consultor: A-21 se cierra con la opcion que ya existe.
    CAMBIA DE SENTIDO A PROPOSITO el 2026-10-26 (ADR-0085, sesion 5, S-19): la vela sin cuerpo ya
    no es una diferencia -el motor hace lo que la lectura literal-, y queda solo el breaker
    contrario que rompe con la mecha tras una alternancia (S-20, a la sesion 6). El nombre se
    conserva para que la historia se lea."""
    distintas = [nombre for nombre, *_, igual in SERIES if not igual]
    assert distintas == ["breaker contrario (R) que rompe con mecha tras alternancia (R, V)"]


def test_a21_queda_cerrada_con_la_opcion_que_ya_existia() -> None:
    """El enum no gana ninguna opcion, el registro trae el valor y la ambiguedad esta RESUELTA."""
    from botsito.cases.ambiguedades import cargar_ambiguedades

    assert LECTURAS_LIMPIA == ("solo_una_zona_de_control", "sin_mecha_mas_alla_del_extremo")
    registro = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
    p = registro.parametros["zona_control_limpia"]
    assert p.estado.value == "CONFIRMED" and p.valor == SOLO_UNA_ZONA_DE_CONTROL
    assert p.fuente is not None and p.fuente.id == "fb-2026-10-04-sesion-04-48fb5817"
    a21 = next(
        a
        for a in cargar_ambiguedades(RAIZ / "knowledge" / "spec" / "ambiguedades.yaml")
        if a.id == "A-21"
    )
    assert a21.estado == "RESUELTA" and "zona_control_limpia" in a21.parametros
