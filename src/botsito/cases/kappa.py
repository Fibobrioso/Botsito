"""Kappa de Cohen entre dos rondas de etiquetado y gramatica de la etiqueta por sesion (F10).

La unidad de acuerdo es (caso, sesion): un caso (dia operativo) tiene una decision por cada
sesion H4 declarada en `config.yaml`. Las rondas se leen de los registros F09 `LABEL_CASE`
activos (respetando `supersede`); un fichero de ronda aparte solo existe como fixture de test.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from fractions import Fraction

from botsito.feedback.modelo import FeedbackRecord, activos

_DECISION = re.compile(
    r"^(?P<decision>[a-z_]+)(?:@(?P<hora>(?:[01]\d|2[0-3]):[0-5]\d))?$", re.ASCII
)
_PAR = re.compile(r"^(?P<clave>[a-z_][a-z0-9_]*)=(?P<valor>\S+)$", re.ASCII)


class EtiquetaError(ValueError):
    """La etiqueta no sigue la gramatica del kit o las rondas no son comparables."""


@dataclass(frozen=True, slots=True)
class Decision:
    sesion: str
    decision: str
    hora: str | None = None
    extras: tuple[tuple[str, str], ...] = ()


def parsear_etiqueta(
    valor: str, sesiones: Sequence[str], etiquetas: Sequence[str]
) -> dict[str, Decision]:
    """`07-11: venta@08:37 e=1.15364 sl=1.15420; 11-15: no_trade` -> una decision por sesion.
    Cada sesion declarada aparece exactamente una vez; la decision esta en `etiquetas`."""
    salida: dict[str, Decision] = {}
    for trozo in valor.split(";"):
        trozo = trozo.strip()
        if not trozo:
            continue
        if ":" not in trozo:
            raise EtiquetaError(f"falta ': ' entre sesion y decision en {trozo!r}")
        sesion, resto = trozo.split(":", 1)
        sesion = sesion.strip()
        if sesion not in sesiones:
            raise EtiquetaError(f"sesion desconocida {sesion!r} (declaradas: {list(sesiones)})")
        if sesion in salida:
            raise EtiquetaError(f"la sesion {sesion} aparece dos veces")
        partes = resto.split()
        if not partes:
            raise EtiquetaError(f"{sesion}: falta la decision")
        m = _DECISION.match(partes[0])
        if not m or m.group("decision") not in etiquetas:
            raise EtiquetaError(
                f"{sesion}: decision {partes[0]!r} no esta en {list(etiquetas)} "
                "(formato decision[@HH:MM])"
            )
        extras: list[tuple[str, str]] = []
        for p in partes[1:]:
            mp = _PAR.match(p)
            if not mp:
                raise EtiquetaError(f"{sesion}: {p!r} no es clave=valor")
            if any(mp.group("clave") == c for c, _ in extras):
                raise EtiquetaError(f"{sesion}: clave repetida {mp.group('clave')!r}")
            extras.append((mp.group("clave"), mp.group("valor")))
        salida[sesion] = Decision(sesion, m.group("decision"), m.group("hora"), tuple(extras))
    faltan = [s for s in sesiones if s not in salida]
    if faltan:
        raise EtiquetaError(f"faltan las sesiones {faltan}")
    return salida


@dataclass
class ResultadoKappa:
    unidades: int
    po: Fraction
    pe: Fraction
    kappa: Fraction | None  # None si pe == 1 (una sola categoria en ambas rondas)
    matriz: dict[str, dict[str, int]]  # a -> b -> recuento
    acuerdo_por_categoria: dict[str, Fraction]
    avisos: list[str] = field(default_factory=list)


def calcular(
    a: Mapping[str, str], b: Mapping[str, str], etiquetas: Sequence[str]
) -> ResultadoKappa:
    """Kappa de Cohen sin ponderar sobre las mismas unidades. Exacto (fracciones)."""
    if set(a) != set(b):
        solo_a = sorted(set(a) - set(b))
        solo_b = sorted(set(b) - set(a))
        raise EtiquetaError(
            f"las rondas no tienen las mismas unidades: solo en a {solo_a}, solo en b {solo_b}"
        )
    if not a:
        raise EtiquetaError("no hay unidades que comparar")
    for nombre, ronda in (("a", a), ("b", b)):
        malas = sorted({v for v in ronda.values() if v not in etiquetas})
        if malas:
            raise EtiquetaError(f"ronda {nombre}: etiquetas fuera del conjunto {malas}")
    n = len(a)
    matriz = {x: dict.fromkeys(etiquetas, 0) for x in etiquetas}
    for u in a:
        matriz[a[u]][b[u]] += 1
    acuerdos = sum(matriz[x][x] for x in etiquetas)
    po = Fraction(acuerdos, n)
    fila = {x: sum(matriz[x].values()) for x in etiquetas}
    columna = {y: sum(matriz[x][y] for x in etiquetas) for y in etiquetas}
    pe = sum((Fraction(fila[x] * columna[x], n * n) for x in etiquetas), Fraction(0))
    kappa = None if pe == 1 else (po - pe) / (1 - pe)
    acuerdo: dict[str, Fraction] = {}
    avisos: list[str] = []
    for x in etiquetas:
        presentes = fila[x] + columna[x] - matriz[x][x]
        if presentes:
            acuerdo[x] = Fraction(matriz[x][x], presentes)
    dominante = max(etiquetas, key=lambda x: fila[x] + columna[x])
    if fila[dominante] + columna[dominante] >= Fraction(3, 2) * n:
        avisos.append(
            f"prevalencia: {dominante!r} domina las dos rondas; kappa baja aunque el acuerdo "
            f"bruto sea alto (po = {float(po):.2f})"
        )
    if kappa is None:
        avisos.append("una sola categoria en ambas rondas: kappa no esta definida (pe = 1)")
    return ResultadoKappa(n, po, pe, kappa, matriz, acuerdo, avisos)


def etiquetas_de_registros(
    registros: Iterable[FeedbackRecord],
    sesion: str,
    sesiones_h4: Sequence[str],
    etiquetas: Sequence[str],
) -> dict[str, str]:
    """Unidades (`caso|sesion_h4` -> decision) de los `LABEL_CASE` ACTIVOS de una sesion de
    feedback. Dos registros activos sobre el mismo caso son error (uno debe superseder al otro).

    `activos` se aplica a TODOS los registros antes de filtrar: un `BORDERLINE` o un
    `MARK_FALSE_POSITIVE` tambien pueden superseder a un `LABEL_CASE` (los tres admiten objetivo
    `caso`), y filtrando primero por accion ese retiro se perderia y la etiqueta retirada
    reapareceria como viva. Una correccion hecha en otra sesion NO retira la etiqueta de esta:
    cada sesion es una ronda, y comparar rondas es justo lo que mide el kappa.
    """
    vivos = [r for r in activos(list(registros)) if r.sesion == sesion and r.accion == "LABEL_CASE"]
    salida: dict[str, str] = {}
    vistos: dict[str, str] = {}
    for r in sorted(vivos, key=lambda x: x.id):
        caso = r.objetivo.id
        if caso in vistos:
            raise EtiquetaError(
                f"{sesion}: {caso} tiene dos LABEL_CASE activos ({vistos[caso]}, {r.id})"
            )
        vistos[caso] = r.id
        try:
            decisiones = parsear_etiqueta(str(r.valor_resultante or ""), sesiones_h4, etiquetas)
        except EtiquetaError as exc:
            raise EtiquetaError(f"{r.id}: {exc}") from exc
        for s, d in decisiones.items():
            salida[f"{caso}|{s}"] = d.decision
    return salida
