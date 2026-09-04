"""Agregacion de velas con anclaje por reloj de pared (F15, ADR-0005).

Regla: los limites de vela de periodo P se calculan por dia local del huso del anclaje como
`anclaje + k*P` (k tal que no pase de 24 h) y se convierten a UTC. Un instante local inexistente
(salto de primavera) se omite; uno ambiguo (repeticion de otono) produce los dos limites (ambos
pliegues). Una M1 pertenece al ultimo limite menor o igual que su inicio. No se inventan velas:
un limite sin M1 no produce vela. Es lo que dibujan TradingView (huso del grafico) y MT5 (hora
de servidor): la vela que cruza un cambio de hora dura 3 h o 5 h.

`huecos()` describe los minutos sin vela dentro de una sesion y sirve para el manifiesto; no
decide nada de negocio.
"""

from __future__ import annotations

import bisect
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from botsito.data.velas import a_datetime, a_minuto
from botsito.domain.valores import HoraLocal
from botsito.domain.velas import MINUTOS_POR_DIA, MinutoUtc, Vela, combinar


class AnclajeError(ValueError):
    """El anclaje o el periodo no son validos."""


@dataclass(frozen=True, slots=True)
class Hueco:
    desde: MinutoUtc  # primer minuto ausente
    hasta: MinutoUtc  # primer minuto presente tras el hueco
    minutos: int


def _huso(nombre: str) -> ZoneInfo:
    try:
        return ZoneInfo(nombre)
    except (ZoneInfoNotFoundError, ValueError) as exc:
        raise AnclajeError(f"huso desconocido {nombre!r}") from exc


def _a_utc_ambos_pliegues(local: datetime, huso: ZoneInfo) -> list[MinutoUtc]:
    """Instantes UTC de una hora de pared: 0 (inexistente), 1 (normal) o 2 (ambigua)."""
    salida: list[MinutoUtc] = []
    for pliegue in (0, 1):
        con_huso = local.replace(tzinfo=huso, fold=pliegue)
        # Un instante inexistente "salta": ida a UTC y vuelta no devuelve la hora de pared pedida.
        # (`astimezone` al mismo huso devuelve el objeto sin normalizar: hay que pasar por UTC.)
        if con_huso.astimezone(UTC).astimezone(huso).replace(tzinfo=None) != local:
            continue
        m = a_minuto(con_huso)
        if m not in salida:
            salida.append(m)
    return sorted(salida)


def limites_del_dia(dia_local: date, periodo_min: int, anclaje: HoraLocal) -> list[MinutoUtc]:
    """Limites UTC de las velas cuyo inicio de pared cae en `dia_local` (hora >= anclaje)."""
    if periodo_min <= 0 or MINUTOS_POR_DIA % periodo_min:
        raise AnclajeError(f"periodo {periodo_min} min invalido: debe dividir 1440")
    huso = _huso(anclaje.huso)
    base = datetime(dia_local.year, dia_local.month, dia_local.day) + timedelta(
        minutes=anclaje.minutos_del_dia
    )
    limites: list[MinutoUtc] = []
    for k in range(MINUTOS_POR_DIA // periodo_min):
        limites.extend(_a_utc_ambos_pliegues(base + timedelta(minutes=k * periodo_min), huso))
    return sorted(set(limites))


def limites_entre(
    desde: MinutoUtc, hasta: MinutoUtc, periodo_min: int, anclaje: HoraLocal
) -> list[MinutoUtc]:
    """Limites UTC ordenados que cubren [desde, hasta), con el ultimo anterior a `desde`."""
    huso = _huso(anclaje.huso)
    dia = (a_datetime(desde).astimezone(huso) - timedelta(days=2)).date()
    fin = (a_datetime(hasta).astimezone(huso) + timedelta(days=2)).date()
    limites: list[MinutoUtc] = []
    while dia <= fin:
        limites.extend(limites_del_dia(dia, periodo_min, anclaje))
        dia += timedelta(days=1)
    limites = sorted(set(limites))
    i = bisect.bisect_right(limites, desde) - 1
    j = bisect.bisect_left(limites, hasta)
    return limites[max(i, 0) : j + 1]


def agregar(velas_m1: list[Vela], periodo_min: int, anclaje: HoraLocal) -> list[Vela]:
    """Velas de `periodo_min` minutos a partir de M1 ordenadas y sin solapar. Puro y determinista.

    La duracion de cada vela agregada es la distancia hasta el limite siguiente (`periodo - 60`,
    `periodo`, `periodo + 60` o `60` el dia de un cambio de hora), no `periodo_min`. `completa`
    dice si el limite de cierre ya paso (hay una M1 posterior o la ultima M1 llega justo a el).
    """
    if not velas_m1:
        return []
    for a, b in zip(velas_m1, velas_m1[1:], strict=False):
        if b.inicio < a.fin:
            raise AnclajeError(f"M1 desordenadas o solapadas en {b.inicio}")
    limites = limites_entre(velas_m1[0].inicio, velas_m1[-1].fin, periodo_min, anclaje)
    if len(limites) < 2 or limites[0] > velas_m1[0].inicio:
        raise AnclajeError("no hay limite anterior a la primera vela (huso o anclaje invalidos)")
    salida: list[Vela] = []
    grupo: list[Vela] = []
    indice = 0
    for v in velas_m1:
        while indice + 1 < len(limites) and limites[indice + 1] <= v.inicio:
            if grupo:
                # Hay una M1 posterior al limite de cierre: la vela esta cerrada.
                salida.append(_cerrar(grupo, limites[indice], limites[indice + 1], True))
                grupo = []
            indice += 1
        grupo.append(v)
    if grupo:
        # La ultima vela solo esta cerrada si su ultima M1 llega justo al limite de cierre.
        cerrada = grupo[-1].fin == limites[indice + 1]
        salida.append(_cerrar(grupo, limites[indice], limites[indice + 1], cerrada))
    return salida


def _cerrar(grupo: list[Vela], inicio: MinutoUtc, fin: MinutoUtc, completa: bool) -> Vela:
    return combinar(grupo, inicio, int(fin) - int(inicio), completa)


def huecos(velas: list[Vela]) -> list[Hueco]:
    """Minutos ausentes entre velas consecutivas (dentro de lo que hay; no juzga sesiones)."""
    salida: list[Hueco] = []
    for a, b in zip(velas, velas[1:], strict=False):
        if b.inicio > a.fin:
            salida.append(Hueco(a.fin, b.inicio, int(b.inicio) - int(a.fin)))
    return salida
