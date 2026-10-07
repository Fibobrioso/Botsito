"""Con que reloj se cuentan la ventana operativa y sus sesiones (ADR-0063, ADR-0069).

Hasta la rama `trabajo/nocturno-01oct` el motor leia `huso_operativa` para DOS cosas: el reloj de
las SESIONES -a que hora abre y cierra la ventana, y donde caen sus sesiones- y el reloj del DIA DE
RIESGO -la medianoche que corta el tope diario, que tiene que ser la de la firma (ADR-0027,
ADR-0053 §4)-. ADR-0063 los separo: el selector `reloj_sesiones` dice CUAL reloj cuenta las
sesiones, y el dia de riesgo sigue en `huso_operativa`.

Desde ADR-0069 (A-42 RESUELTA) el reloj de las sesiones es LA REJILLA H4: las dos sesiones del
trader son las velas H4 de la rejilla de `anclaje_h4` que empiezan en ancla + 8 h y ancla + 12 h.
En su grafico (Europe/Madrid) son las 07-11 y 11-15 casi todo el ano, y las 06-10 y 10-14 las
semanas en que Europa y EE. UU. no coinciden en el horario de verano. El bot no sigue ningun
desfase: la apertura de cada vela sale de `limites_del_dia`, la misma funcion que parte las velas
H4 del bot con zoneinfo sobre el huso del ancla.

**La unica puerta es `RelojSesiones`**: de un dia operativo y una hora NOMINAL («HH:MM», la que
nombra el registro y el kit: `ventana_inicio`, `07-11`, `11-15`) a un instante UTC, y de un
instante a su dia y su hora nominal. Con `rejilla_h4`, el reloj marca `ventana_inicio` en el
instante en que abre la vela H4 numero `sesiones_primera_vela_h4` del dia de rejilla, y corre desde
ahi; con `civil_operativa` y `grafico` es la hora de pared en el huso de ese reloj (ADR-0063), que
sigue existiendo para que los tests calculen H2a y H1 por el mismo camino y demuestren que fallan.
Que parametros lee cada reloj vive aqui, en una tabla, y nunca una cifra (ADR-0002).
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from functools import cached_property
from zoneinfo import ZoneInfo

from botsito.comun.husos import huso_canonico
from botsito.config.registro import Registro
from botsito.data.agregacion import limites_del_dia
from botsito.data.velas import a_datetime, a_minuto
from botsito.domain.valores import HoraLocal
from botsito.domain.velas import MinutoUtc

PARAMETRO_RELOJ_SESIONES = "reloj_sesiones"
# Las opciones del selector que son un HUSO: cada una nombra el parametro que lo lleva (ADR-0063).
HUSO_DEL_RELOJ = {"civil_operativa": "huso_operativa", "grafico": "huso_grafico"}
# La opcion que es la rejilla (ADR-0069), y los parametros que lee: el ancla de la rejilla, la vela
# en que abre la ventana y la hora nominal con que se nombra esa apertura.
REJILLA_H4 = "rejilla_h4"
# Un reloj de pared dado por su huso, fuera del selector (`RelojSesiones.de_pared`).
DE_PARED = "pared"
PARAMETROS_DE_LA_REJILLA = {
    "anclaje": "anclaje_h4",
    "primera_vela": "sesiones_primera_vela_h4",
    "inicio": "ventana_inicio",
    "grafico": "huso_grafico",
}
MINUTOS_H4 = 240
MINUTOS_POR_DIA = 1440


class RelojError(ValueError):
    """El selector nombra un reloj que el motor no sabe leer, o la rejilla no da una vela entera:
    nunca se adivina."""


def huso_del_reloj(registro: Registro, selector: str) -> str:
    """El huso IANA del reloj que dice `selector`, un parametro enum del registro. Con la rejilla
    no hay huso: la hora nominal no es la de ningun reloj de pared (`RelojError`)."""
    opcion = registro.opcion(selector)
    parametro = HUSO_DEL_RELOJ.get(opcion)
    if parametro is None:
        relojes = ", ".join((*HUSO_DEL_RELOJ, REJILLA_H4))
        if opcion == REJILLA_H4:
            raise RelojError(
                f"{selector} = {opcion!r}: la rejilla no es un huso; los instantes salen de "
                f"`reloj_de_las_sesiones` ({relojes})"
            )
        raise RelojError(f"{selector} = {opcion!r}: no es un reloj del registro ({relojes})")
    return registro.texto(parametro)


def huso_de_las_sesiones(registro: Registro) -> str:
    """El huso de un reloj de pared de las sesiones (ADR-0063). Con `rejilla_h4`, `RelojError`."""
    return huso_del_reloj(registro, PARAMETRO_RELOJ_SESIONES)


def _minutos(hhmm: str) -> int:
    hh, mm = (int(x) for x in hhmm.split(":"))
    return hh * 60 + mm


@dataclass(frozen=True)
class RelojSesiones:
    """La puerta: de (dia, hora nominal) a instante UTC y de instante a (dia, hora nominal).

    `huso_visible` es el reloj de pared en que se PINTAN las horas (el visor): el del reloj de
    pared elegido, o, con la rejilla, el del grafico del trader, que es lo que el ve.
    """

    opcion: str
    huso_visible: str
    # solo con la rejilla:
    anclaje: HoraLocal | None = None
    primera_vela: int = 0  # 1 = la vela que abre en el ancla
    inicio_nominal: int = 0  # minutos del dia de `ventana_inicio`

    @classmethod
    def de_pared(cls, huso: str) -> RelojSesiones:
        """Un reloj de pared en `huso`, sin pasar por el selector: lo que piden los guiones de
        medicion de ramas cerradas, que siguen dando `huso_operativa` al arnes (ADR-0063 §5)."""
        return cls(DE_PARED, huso)

    @property
    def es_rejilla(self) -> bool:
        return self.opcion == REJILLA_H4

    @cached_property
    def _zona(self) -> ZoneInfo:
        return huso_canonico(self.anclaje.huso if self.anclaje is not None else self.huso_visible)

    # ------------------------------------------------------------------ de dia y hora a instante

    def instante(self, dia: date, hhmm: str) -> MinutoUtc:
        """El minuto UTC en que el reloj marca `hhmm` el dia operativo `dia`."""
        if not self.es_rejilla:
            hh, mm = divmod(_minutos(hhmm), 60)
            return a_minuto(datetime(dia.year, dia.month, dia.day, hh, mm, tzinfo=self._zona))
        return MinutoUtc(int(self.apertura(dia)) + _minutos(hhmm) - self.inicio_nominal)

    def apertura(self, dia: date) -> MinutoUtc:
        """La apertura de la vela numero `primera_vela` del dia de rejilla del dia operativo
        `dia`: el dia de rejilla cuya vela abre en esa fecha (en el huso del ancla). Se calcula,
        no se escribe «la vispera». Si esa vela no es una H4 entera (el dia de un cambio de hora
        del huso del ancla), el dia no es operable y se dice."""
        assert self.anclaje is not None
        for dia_rejilla in (dia - timedelta(days=1), dia, dia - timedelta(days=2)):
            limites = limites_del_dia(dia_rejilla, MINUTOS_H4, self.anclaje)
            if len(limites) < self.primera_vela + 1:
                continue
            abre = limites[self.primera_vela - 1]
            if a_datetime(abre).astimezone(self._zona).date() != dia:
                continue
            if int(limites[self.primera_vela]) - int(abre) != MINUTOS_H4:
                raise RelojError(
                    f"{dia.isoformat()}: la vela H4 numero {self.primera_vela} de la rejilla de "
                    f"{self.anclaje} no es entera (el dia de rejilla {dia_rejilla.isoformat()} "
                    "tiene un cambio de hora): el dia no es operable"
                )
            return abre
        raise RelojError(
            f"{dia.isoformat()}: ningun dia de rejilla de {self.anclaje} abre su vela numero "
            f"{self.primera_vela} en esa fecha"
        )

    def limites_de_sesiones(
        self, dia: date, sesiones: Sequence[tuple[str, str, str]]
    ) -> list[tuple[str, MinutoUtc, MinutoUtc]]:
        """(nombre, desde, hasta) en UTC de cada sesion nominal (nombre, «HH:MM», «HH:MM»). Con
        la rejilla, cada sesion tiene que ser UNA vela H4 entera de la rejilla, con nombre."""
        salida = [(n, self.instante(dia, a), self.instante(dia, b)) for n, a, b in sesiones]
        if self.es_rejilla and salida:
            assert self.anclaje is not None
            rejilla: set[int] = set()
            for k in range(-2, 2):
                rejilla |= {
                    int(x)
                    for x in limites_del_dia(dia + timedelta(days=k), MINUTOS_H4, self.anclaje)
                }
            for nombre, a, b in salida:
                if int(a) not in rejilla or int(b) not in rejilla or int(b) - int(a) != MINUTOS_H4:
                    raise RelojError(
                        f"{dia.isoformat()}: la sesion {nombre} no es una vela H4 entera de la "
                        f"rejilla de {self.anclaje} ({a_datetime(a):%H:%M}-"
                        f"{a_datetime(b):%H:%M} UTC)"
                    )
        return salida

    # ------------------------------------------------------------------ de instante a dia y hora

    def lectura(self, instante: int) -> tuple[date, int]:
        """El dia operativo y los minutos del dia que el reloj marca en `instante` (UTC)."""
        if not self.es_rejilla:
            local = a_datetime(instante).astimezone(self._zona)
            return local.date(), local.hour * 60 + local.minute
        # El dia nominal empieza `inicio_nominal` minutos antes de la apertura de su vela y dura
        # un dia: se prueba el dia del instante en el huso del ancla y sus vecinos.
        centro = a_datetime(instante).astimezone(self._zona).date()
        for dia in (centro, centro - timedelta(days=1), centro + timedelta(days=1)):
            try:
                abre = int(self.apertura(dia))
            except RelojError:
                continue
            minuto = instante - abre + self.inicio_nominal
            if 0 <= minuto < MINUTOS_POR_DIA:
                return dia, minuto
        raise RelojError(f"ningun dia operativo contiene el minuto UTC {instante} en la rejilla")


def reloj_de_las_sesiones(registro: Registro) -> RelojSesiones:
    """El reloj de las sesiones que dice `reloj_sesiones`, leido del registro una vez."""
    opcion = registro.opcion(PARAMETRO_RELOJ_SESIONES)
    if opcion in HUSO_DEL_RELOJ:
        return RelojSesiones(opcion, registro.texto(HUSO_DEL_RELOJ[opcion]))
    if opcion != REJILLA_H4:
        raise RelojError(
            f"{PARAMETRO_RELOJ_SESIONES} = {opcion!r}: no es un reloj del registro "
            f"({', '.join((*HUSO_DEL_RELOJ, REJILLA_H4))})"
        )
    p = PARAMETROS_DE_LA_REJILLA
    primera = registro.entero(p["primera_vela"])
    if primera < 1 or primera > MINUTOS_POR_DIA // MINUTOS_H4:
        raise RelojError(f"{p['primera_vela']} = {primera}: no es una vela del dia de rejilla")
    return RelojSesiones(
        opcion,
        registro.texto(p["grafico"]),
        anclaje=registro.hora(p["anclaje"]),
        primera_vela=primera,
        inicio_nominal=registro.hora(p["inicio"]).minutos_del_dia,
    )


__all__ = [
    "HUSO_DEL_RELOJ",
    "PARAMETROS_DE_LA_REJILLA",
    "PARAMETRO_RELOJ_SESIONES",
    "REJILLA_H4",
    "RelojError",
    "RelojSesiones",
    "huso_de_las_sesiones",
    "huso_del_reloj",
    "reloj_de_las_sesiones",
]
