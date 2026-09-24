"""El criterio de fidelidad en desarrollo (ADR-0043): emparejar y medir, SIN motor.

Compara operaciones del trader -las de los `caso-*.yaml` `dev`- con operaciones del bot, cuando
exista. Este modulo NO produce ninguna decision del bot: recibe las dos listas y las compara. Es
puro -sin IO salvo `cargar_criterio`-, y sus cifras no viven aqui sino en
`knowledge/cases/criterio_fidelidad.yaml` (ADR-0002: ninguna cifra de negocio en `src/`).

**LA UNIDAD es la operacion, dentro de su dia y su sesion.** Una operacion del bot empareja con una
del trader si coinciden el dia, la sesion y la direccion, `|Δentrada|` no pasa de la tolerancia en
puntos y `|Δinstante de llenado|` no pasa de la tolerancia en minutos. El instante del caso ES el
llenado (medido: `docs/validation/INSTANTE-LLENADO-SALIDA.txt`).

**UNO A UNO Y DETERMINISTA.** Entre todas las parejas compatibles se toman, en este orden, la de
menor `|Δinstante|`, luego la de menor `|Δentrada|`, luego la mas temprana; y ninguna
operacion se usa dos veces. Es un emparejamiento voraz global: el primer criterio de desempate
manda sobre todo el dia, no solo sobre una operacion.

**LO QUE NO PUNTUA.** Las operaciones del bot en dias sin ninguna del trader se cuentan aparte y no
entran en la precision: leer esa ausencia como decision del trader es una inferencia nuestra
(ADR-0016). Y fuera del criterio quedan stop, TP, resultado y gestion hasta que se resuelvan sus
ambiguedades (ADR-0043).
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

from botsito.comun.yaml_estricto import YamlError, leer_yaml

FICHERO_CRITERIO = "knowledge/cases/criterio_fidelidad.yaml"
_SEGUNDOS_POR_MINUTO = 60


class CriterioError(ValueError):
    """El fichero del criterio no tiene la forma declarada."""


@dataclass(frozen=True)
class Operacion:
    dia: str
    sesion: str
    direccion: str
    instante: datetime  # el LLENADO, con huso
    entrada: Decimal


@dataclass(frozen=True)
class Tolerancias:
    entrada_puntos: int
    instante_min: int
    escala: int  # puntos por unidad de precio del instrumento


@dataclass(frozen=True)
class Criterio:
    tolerancias: Tolerancias
    umbral_cobertura: Fraction
    umbral_precision: Fraction
    construccion: tuple[str, ...]
    medida: tuple[str, ...]


@dataclass(frozen=True)
class Pareja:
    trader: Operacion
    bot: Operacion
    delta_segundos: int
    delta_puntos: Decimal


@dataclass(frozen=True)
class Medida:
    parejas: tuple[Pareja, ...]
    n_trader: int
    n_bot_puntuables: int
    n_bot_fuera: int  # del bot en dias sin ninguna operacion del trader: no puntuan (ADR-0016)
    cobertura: Fraction | None  # None = sin definir (cero operaciones del trader)
    precision: Fraction | None  # None = sin definir (cero operaciones del bot puntuables)
    mismo_minuto: int
    delta_instante_min: dict[int, int]  # |Δinstante| en minutos enteros -> cuantas
    delta_entrada_puntos: dict[Decimal, int]  # |Δentrada| en puntos -> cuantas


def _deltas(trader: Operacion, bot: Operacion, tol: Tolerancias) -> tuple[int, Decimal]:
    segundos = abs(int((bot.instante - trader.instante).total_seconds()))
    puntos = abs(bot.entrada - trader.entrada) * tol.escala
    return segundos, puntos


def compatibles(trader: Operacion, bot: Operacion, tol: Tolerancias) -> bool:
    if (trader.dia, trader.sesion, trader.direccion) != (bot.dia, bot.sesion, bot.direccion):
        return False
    segundos, puntos = _deltas(trader, bot, tol)
    return puntos <= tol.entrada_puntos and segundos <= tol.instante_min * _SEGUNDOS_POR_MINUTO


def emparejar(
    trader: Sequence[Operacion], bot: Sequence[Operacion], tol: Tolerancias
) -> tuple[Pareja, ...]:
    """Uno a uno y determinista.

    Menor |Δinstante|, luego menor |Δentrada|, luego la mas temprana."""
    candidatas: list[tuple[int, Decimal, datetime, datetime, int, int]] = []
    for i, t in enumerate(trader):
        for j, b in enumerate(bot):
            if compatibles(t, b, tol):
                segundos, puntos = _deltas(t, b, tol)
                candidatas.append((segundos, puntos, min(t.instante, b.instante), b.instante, i, j))
    candidatas.sort()
    usados_t: set[int] = set()
    usados_b: set[int] = set()
    parejas: list[Pareja] = []
    for segundos, puntos, _, _, i, j in candidatas:
        if i in usados_t or j in usados_b:
            continue
        usados_t.add(i)
        usados_b.add(j)
        parejas.append(Pareja(trader[i], bot[j], segundos, puntos))
    return tuple(sorted(parejas, key=lambda p: (p.trader.instante, p.bot.instante)))


def _minuto(instante: datetime) -> datetime:
    return instante.replace(second=0, microsecond=0)


def medir(trader: Sequence[Operacion], bot: Sequence[Operacion], tol: Tolerancias) -> Medida:
    """Cobertura, precision y distribuciones. Nunca divide por cero: sin denominador, `None`."""
    dias_trader = {t.dia for t in trader}
    puntuables = [b for b in bot if b.dia in dias_trader]
    parejas = emparejar(trader, puntuables, tol)
    return Medida(
        parejas=parejas,
        n_trader=len(trader),
        n_bot_puntuables=len(puntuables),
        n_bot_fuera=len(bot) - len(puntuables),
        cobertura=Fraction(len(parejas), len(trader)) if trader else None,
        precision=Fraction(len(parejas), len(puntuables)) if puntuables else None,
        mismo_minuto=sum(
            1 for p in parejas if _minuto(p.trader.instante) == _minuto(p.bot.instante)
        ),
        delta_instante_min=dict(Counter(p.delta_segundos // _SEGUNDOS_POR_MINUTO for p in parejas)),
        delta_entrada_puntos=dict(Counter(p.delta_puntos for p in parejas)),
    )


def _fraccion(valor: object, campo: str) -> Fraction:
    try:
        f = Fraction(str(valor))
    except (ValueError, ZeroDivisionError) as exc:
        raise CriterioError(f"{FICHERO_CRITERIO}: {campo} no es un numero") from exc
    if not 0 <= f <= 1:
        raise CriterioError(f"{FICHERO_CRITERIO}: {campo} va entre 0 y 1")
    return f


def _entero(doc: dict[str, object], campo: str) -> int:
    valor = doc.get(campo)
    if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
        raise CriterioError(f"{FICHERO_CRITERIO}: {campo} es un entero positivo")
    return valor


def _meses(doc: dict[str, object], campo: str) -> tuple[str, ...]:
    valor = doc.get(campo)
    if not isinstance(valor, list) or not all(isinstance(m, str) for m in valor):
        raise CriterioError(f"{FICHERO_CRITERIO}: {campo} es una lista de meses AAAA-MM")
    return tuple(valor)


def cargar_criterio(repo: Path) -> Criterio:
    try:
        doc = leer_yaml(repo / FICHERO_CRITERIO)
    except (OSError, YamlError) as exc:
        raise CriterioError(f"{FICHERO_CRITERIO}: {exc}") from exc
    if not isinstance(doc, dict):
        raise CriterioError(f"{FICHERO_CRITERIO}: se espera un mapa")
    construccion, medida = _meses(doc, "construccion"), _meses(doc, "medida")
    if set(construccion) & set(medida):
        raise CriterioError(f"{FICHERO_CRITERIO}: un mes no puede construir y medir a la vez")
    return Criterio(
        tolerancias=Tolerancias(
            entrada_puntos=_entero(doc, "tolerancia_entrada_puntos"),
            instante_min=_entero(doc, "tolerancia_instante_min"),
            escala=_entero(doc, "escala_puntos"),
        ),
        umbral_cobertura=_fraccion(doc.get("umbral_cobertura"), "umbral_cobertura"),
        umbral_precision=_fraccion(doc.get("umbral_precision"), "umbral_precision"),
        construccion=construccion,
        medida=medida,
    )


__all__ = [
    "FICHERO_CRITERIO",
    "Criterio",
    "CriterioError",
    "Medida",
    "Operacion",
    "Pareja",
    "Tolerancias",
    "cargar_criterio",
    "compatibles",
    "emparejar",
    "medir",
]
