"""El motor de un dia: el interprete de ADR-0030 recorrido evento a evento (ADR-0048).

**LA UNIDAD DE EJECUCION ES EL DIA** (ADR-0048 §3). Un `EstadoDia` nace al empezar el dia y cruza
sus sesiones: un hecho que fija la primera sigue vivo en la segunda. Lo pendiente y lo abierto al
cambiar de sesion no lo decide este modulo sino las reglas: RN-035 retira la orden sin llenar al
abrir la sesion siguiente (A-30 y A-39, RESUELTAS en la sesion 4; `primitivas_broker.py`) y RN-002
cierra la posicion antes del fin de su vela H4 (ADR-0060). Y cada dia empieza de cero, PROVISIONAL
(H6).

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
from botsito.domain.pivotes_m15 import (
    CUALQUIER_MECHA,
    MECHAS_QUE_VUELVEN,
    NO_MUEVE,
    Pivote,
    nivel_con_mecha_que_vuelve,
    pivote_mas_reciente,
)
from botsito.domain.velas import MinutoUtc, Vela
from botsito.engine.interprete import (
    VALOR_APAGADO,
    EstadoDia,
    Interprete,
    Momento,
    ReglaEjecutable,
)
from botsito.engine.relojes import RelojSesiones


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
        mecha_que_vuelve: str = NO_MUEVE,
        criterio_toma: str = "cuerpo",
    ) -> None:
        # `mecha_que_vuelve` y `criterio_toma` son `liquidez_m15_mecha_que_vuelve` y
        # `liquidez_m15_criterio_toma` del registro (ADR-0084): los lee quien construye los datos
        # (el arnes y el visor). Sin darlos, el nivel es el de antes de ADR-0084
        if mecha_que_vuelve not in MECHAS_QUE_VUELVEN:
            raise ValueError(
                f"mecha que vuelve {mecha_que_vuelve!r} no esta en {MECHAS_QUE_VUELVEN}"
            )
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
        self.mecha_que_vuelve = mecha_que_vuelve
        self.criterio_toma = criterio_toma

    def velas_h4_cerradas(self, instante: int) -> list[Vela]:
        return self._velas[: bisect.bisect_right(self._fines, instante)]

    def _n_m15_cerradas(self, instante: int) -> int:
        return bisect.bisect_right(self._fines_m15, instante)

    def ultima_m15_cerrada(self, instante: int) -> Vela | None:
        n = self._n_m15_cerradas(instante)
        return self._m15[n - 1] if n else None

    def ultima_m1_cerrada(self, instante: int) -> Vela | None:
        """La M1 que cierra justo en `instante` -la que dispara el evento de ese minuto-; None
        si esa vela falta en los datos."""
        i = bisect.bisect_left(self._inicios_m1, MinutoUtc(instante - 1))
        if i < len(self._m1) and int(self._m1[i].inicio) == instante - 1:
            return self._m1[i]
        return None

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
        p = pivote_mas_reciente(
            self._m15,
            self.m15_en_curso(instante),
            self.lectura_pivote,
            instante,
            lado,
            self._n_m15_cerradas(instante),
            self.mecha_que_vuelve,
        )
        if p is None or self.mecha_que_vuelve != CUALQUIER_MECHA:
            return p
        # caso (ii) de ADR-0084: las M1 cerradas desde que el pivote esta formado hasta este
        # instante (la que cierra en `instante` incluida) mueven el nivel con sus mechas, y la
        # primera que lo cruza con el criterio de la toma lo congela
        return nivel_con_mecha_que_vuelve(
            p, self.m1_entre(int(p.formado_en), instante), self.criterio_toma
        )


@dataclass(frozen=True)
class DiaDeMercado:
    dia: date
    huso: str  # el reloj de pared en que se PINTAN las horas (`RelojSesiones.huso_visible`)
    sesiones: tuple[Sesion, ...]
    datos: DatosMercado
    # La puerta que convierte «HH:MM» en instantes (ADR-0069). Sin ella -un dia hecho a mano en
    # los tests- las horas son de pared en `huso`, que es lo que el motor hacia hasta entonces.
    reloj: RelojSesiones | None = None

    def limites(self) -> list[tuple[str, MinutoUtc, MinutoUtc]]:
        """(nombre, desde, hasta) en UTC de cada sesion, por la puerta."""
        if self.reloj is not None:
            return self.reloj.limites_de_sesiones(
                self.dia, [(s.nombre, s.desde, s.hasta) for s in self.sesiones]
            )
        return [
            (
                s.nombre,
                _minuto_utc(self.dia, s.desde, self.huso),
                _minuto_utc(self.dia, s.hasta, self.huso),
            )
            for s in self.sesiones
        ]


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
        limites = dia.limites()
        estado = EstadoDia()
        trazas = {nombre: TrazaSesion() for nombre, _, _ in limites}
        primero, ultimo = min(d for _, d, _ in limites), max(h for _, _, h in limites)
        instante: int = primero
        while instante <= ultimo:
            sesion, abre = self._sesion(limites, instante)
            desde = next((d for n, d, _ in limites if n == sesion), None)
            momento = Momento(MinutoUtc(instante), sesion, abre, dia.datos, desde, primero)
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
