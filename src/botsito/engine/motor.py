"""El motor de un dia: el interprete de ADR-0030 recorrido evento a evento (ADR-0048).

**LA UNIDAD DE EJECUCION ES EL DIA** (ADR-0048 §3). Un `EstadoDia` nace al empezar el dia y cruza
sus sesiones: un hecho que fija la primera sigue vivo en la segunda. Lo que A-39 deja abierto -que
pasa con lo pendiente o lo abierto al cambiar de sesion- es PROVISIONAL: aqui no se cierra ni se
retira nada al cambiar de sesion. Y cada dia empieza de cero, tambien PROVISIONAL (H6).

**LOS EVENTOS.** Uno por cada cierre de M1 entre la apertura de la primera sesion y el cierre de la
ultima, ambos incluidos: es la fase de estrategia de ADR-0028 §2. No hay ticks ni bróker simulado
(H4): la fase de riesgo se evalua en esos mismos cierres, y los hechos de origen `broker` son
falsos mientras nada se haya colocado.

**SIN MIRAR AL FUTURO.** Las primitivas solo ven lo cerrado hasta el instante del evento:
`DatosMercado.velas_h4_cerradas` corta por la hora de FIN de cada vela, como `domain/sesgo.py`.

Las operaciones del bot salen en el formato de `cases/criterio_fidelidad.Operacion`. Hoy el motor
real no puede producir ninguna, porque colocar una orden es una accion sin escribir y no hay bróker.
"""

from __future__ import annotations

import bisect
from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Protocol

from botsito.cases.criterio_fidelidad import Operacion
from botsito.comun.husos import huso_canonico
from botsito.data.velas import a_minuto
from botsito.domain.velas import MinutoUtc, Vela
from botsito.engine.interprete import (
    VALOR_APAGADO,
    EstadoDia,
    Interprete,
    Momento,
    ReglaEjecutable,
)


@dataclass(frozen=True)
class Sesion:
    nombre: str
    desde: str  # HH:MM en el huso del dia
    hasta: str


class DatosMercado:
    """Las H4 de un tramo, entregadas SOLO hasta el instante que se pide."""

    def __init__(self, velas_h4: Sequence[Vela]) -> None:
        self._velas = sorted(velas_h4, key=lambda v: v.fin)
        self._fines = [v.fin for v in self._velas]

    def velas_h4_cerradas(self, instante: int) -> list[Vela]:
        return self._velas[: bisect.bisect_right(self._fines, instante)]


@dataclass(frozen=True)
class DiaDeMercado:
    dia: date
    huso: str  # el de las sesiones (`huso_operativa`)
    sesiones: tuple[Sesion, ...]
    datos: DatosMercado


@dataclass
class TrazaSesion:
    """Lo que paso en una sesion: el material del embudo (ADR-0048 §5)."""

    fijados: list[tuple[int, str, str, str]] = field(default_factory=list)  # instante, regla...
    no_implementadas: set[tuple[str, str]] = field(default_factory=set)  # (regla, primitiva)
    bloqueadas: set[tuple[str, str, str]] = field(default_factory=set)
    anotaciones: dict[str, str] = field(default_factory=dict)

    @property
    def hechos_producidos(self) -> frozenset[str]:
        return frozenset(h for _, _, h, v in self.fijados if v != VALOR_APAGADO)


@dataclass(frozen=True)
class ResultadoDia:
    dia: str
    operaciones: tuple[Operacion, ...]
    sesiones: dict[str, TrazaSesion]


class Motor(Protocol):
    def correr_dia(self, dia: DiaDeMercado) -> ResultadoDia: ...


def _minuto_utc(dia: date, hhmm: str, huso: str) -> MinutoUtc:
    hh, mm = (int(x) for x in hhmm.split(":"))
    local = datetime(dia.year, dia.month, dia.day, hh, mm, tzinfo=huso_canonico(huso))
    return a_minuto(local)


@dataclass
class MotorSpec:
    """El motor real: la spec vigente, recorrida por el interprete con las primitivas de hoy."""

    interprete: Interprete
    reglas: Sequence[ReglaEjecutable]

    def correr_dia(self, dia: DiaDeMercado) -> ResultadoDia:
        limites = [
            (
                s.nombre,
                _minuto_utc(dia.dia, s.desde, dia.huso),
                _minuto_utc(dia.dia, s.hasta, dia.huso),
            )
            for s in dia.sesiones
        ]
        estado = EstadoDia()
        trazas = {nombre: TrazaSesion() for nombre, _, _ in limites}
        primero, ultimo = min(d for _, d, _ in limites), max(h for _, _, h in limites)
        instante: int = primero
        while instante <= ultimo:
            sesion, abre = self._sesion(limites, instante)
            momento = Momento(MinutoUtc(instante), sesion, abre, dia.datos)
            evento = self.interprete.evento(self.reglas, momento, estado)
            if sesion is not None:
                traza = trazas[sesion]
                traza.fijados += [(instante, r, h, v) for r, h, v in evento.fijados]
                traza.no_implementadas |= evento.no_implementadas
                traza.bloqueadas |= evento.bloqueadas
            instante += 1
        for nombre, traza in trazas.items():
            traza.anotaciones.update(estado.anotaciones.get(nombre, {}))
        return ResultadoDia(dia.dia.isoformat(), (), trazas)

    @staticmethod
    def _sesion(limites: Sequence[tuple[str, int, int]], instante: int) -> tuple[str | None, bool]:
        for nombre, desde, hasta in limites:
            if desde <= instante < hasta:
                return nombre, instante == desde
        for nombre, _, hasta in limites:
            if instante == hasta:
                return nombre, False  # el cierre de la ultima sesion: su fin de ventana
        return None, False


__all__ = [
    "DatosMercado",
    "DiaDeMercado",
    "Motor",
    "MotorSpec",
    "ResultadoDia",
    "Sesion",
    "TrazaSesion",
]
