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
from botsito.domain.pivotes_m15 import Pivote, pivote_mas_reciente
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


class SinLecturaDePivoteError(LookupError):
    """Se pidio la liquidez de M15 a unos datos sin lectura de «formado» (A-35 sin fijar)."""


class DatosMercado:
    """Las velas de un tramo, entregadas SOLO hasta el instante que se pide: las H4 (el sesgo,
    RN-003) y, desde `trabajo/preparar-a35-a44`, las M15 y las M1 con las que se construye la M15
    en curso, para la liquidez de M15 (RN-004) con la lectura de «formado» que se le de. Sin
    lectura -A-35 sin fijar-, pedir la liquidez falla con nombre y la primitiva queda
    NO_IMPLEMENTADA, como hasta hoy."""

    def __init__(
        self,
        velas_h4: Sequence[Vela],
        velas_m15: Sequence[Vela] = (),
        velas_m1: Sequence[Vela] = (),
        lectura_pivote: str | None = None,
    ) -> None:
        self._velas = sorted(velas_h4, key=lambda v: v.fin)
        self._fines = [v.fin for v in self._velas]
        # las M15 completas, por su fin; las incompletas (la ultima del tramo) no cierran nunca
        self._m15 = sorted((v for v in velas_m15 if v.completa), key=lambda v: v.fin)
        self._fines_m15 = [v.fin for v in self._m15]
        self._rejilla = sorted(velas_m15, key=lambda v: v.inicio)  # todas: da la M15 en curso
        self._inicios_m15 = [v.inicio for v in self._rejilla]
        self._m1 = sorted(velas_m1, key=lambda v: v.inicio)
        self._inicios_m1 = [v.inicio for v in self._m1]
        self.lectura_pivote = lectura_pivote

    def velas_h4_cerradas(self, instante: int) -> list[Vela]:
        return self._velas[: bisect.bisect_right(self._fines, instante)]

    def _n_m15_cerradas(self, instante: int) -> int:
        return bisect.bisect_right(self._fines_m15, instante)

    def ultima_m15_cerrada(self, instante: int) -> Vela | None:
        n = self._n_m15_cerradas(instante)
        return self._m15[n - 1] if n else None

    def m15_en_curso(self, instante: int) -> Vela | None:
        """La M15 que contiene `instante`, construida SOLO con sus M1 cerradas hasta el; None si
        `instante` cae justo en un limite de M15 o no hay ninguna M1 dentro."""
        i = bisect.bisect_right(self._inicios_m15, instante) - 1
        if i < 0:
            return None
        rejilla = self._rejilla[i]
        if not (rejilla.inicio < instante < rejilla.fin):
            return None
        a = bisect.bisect_left(self._inicios_m1, rejilla.inicio)
        b = bisect.bisect_left(self._inicios_m1, MinutoUtc(instante))
        dentro = self._m1[a:b]
        if not dentro:
            return None
        return Vela(
            rejilla.inicio,
            dentro[0].abierta,
            max(v.maxima for v in dentro),
            min(v.minima for v in dentro),
            dentro[-1].cierre,
            sum(v.volumen for v in dentro),
            rejilla.duracion_min,
            len(dentro),
            False,
        )

    def m1_entre(self, desde: int, hasta: int) -> list[Vela]:
        """Las M1 con inicio en [desde, hasta), en orden: para medir sobre lo cerrado."""
        a = bisect.bisect_left(self._inicios_m1, MinutoUtc(desde))
        b = bisect.bisect_left(self._inicios_m1, MinutoUtc(hasta))
        return self._m1[a:b]

    def liquidez_m15(self, instante: int, lado: str) -> Pivote | None:
        """El pivote de M15 mas reciente ya formado del lado pedido (ADR-0045), con la lectura de
        «formado» de estos datos. Sin lectura, falla con nombre: A-35 sin fijar."""
        if self.lectura_pivote is None:
            raise SinLecturaDePivoteError(
                "sin lectura de «formado» (A-35): estos datos no producen liquidez_m15"
            )
        return pivote_mas_reciente(
            self._m15,
            self.m15_en_curso(instante),
            self.lectura_pivote,
            instante,
            lado,
            self._n_m15_cerradas(instante),
        )


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
    disparadas: set[str] = field(default_factory=set)  # reglas que dispararon en la sesion (H1)
    empates: set[tuple[str, tuple[str, ...]]] = field(default_factory=set)  # avisos de H3

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
                traza.disparadas |= set(evento.disparadas)
                traza.empates |= set(evento.empates)
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
    "SinLecturaDePivoteError",
    "DiaDeMercado",
    "Motor",
    "MotorSpec",
    "ResultadoDia",
    "Sesion",
    "TrazaSesion",
]
