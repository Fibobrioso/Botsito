"""El freno de peticiones al servidor (rama `feature/freno-peticiones`, ADR-0067).

FTMO trata como practica prohibida «more than 2,000 server requests per day» (R13 de
`docs/validation/FTMO-REGLAS.md`, `firma_mensajes_dia_max`). El broker ya las contaba; desde aqui,
ademas, las FRENA. El freno vive en el puerto -el broker le pregunta antes de apuntar cada
peticion- y no en las reglas de la estrategia, asi que ninguna regla puede saltarselo. No tiene IO
ni reloj propio: el broker le da el dia de la firma de cada peticion (`huso_corte`), y el
adaptador real de MetaTrader usara la misma clase.

Tres cosas, con sus umbrales en el registro (ADR-0002), PROVISIONAL bajo A-54:

- **el aviso** (`freno_peticiones_aviso`): el dia que el total llega ahi, una entrada en la traza y
  en el log. No frena;
- **el corte** (`freno_peticiones_corte`): desde ahi, ese dia solo sale lo que protege la cuenta;
- **el bucle** (`freno_bucle_repeticiones` dentro de `freno_bucle_minutos`): tantas peticiones
  IGUALES dentro de la ventana cortan el envio el resto del dia. Igual es la misma `firma` -el
  contenido de la peticion, sin el id-, aunque haya otras en medio.

LO QUE PROTEGE LA CUENTA PASA SIEMPRE, Y CUENTA: cancelar una pendiente, cerrar a mercado y mover
el stop de una posicion viva hacia el lado que reduce el riesgo (el break even). FTMO no dice que
no sean «server requests», asi que se cuentan; el corte deja hueco para ellas. Una peticion NEGADA
no llega al servidor y no se cuenta. Todo lo negado, cada corte y el aviso quedan en `cortes`.

El dia cambia a medianoche en el reloj de la firma, y entonces todo vuelve a cero, tambien un
corte por bucle.
"""

from __future__ import annotations

import logging
from collections import deque
from collections.abc import Hashable
from dataclasses import dataclass, field
from datetime import date

LOG = logging.getLogger(__name__)

MOTIVO_AVISO = "freno_aviso"
MOTIVO_CORTE = "freno_corte"
MOTIVO_BUCLE = "freno_bucle"
MOTIVOS_QUE_NIEGAN = (MOTIVO_CORTE, MOTIVO_BUCLE)


class FrenoError(ValueError):
    """Unos umbrales que no tienen sentido: el freno no se arma con ellos."""


@dataclass(frozen=True)
class LimitesFreno:
    """Los umbrales del freno, ya leidos del registro por quien construye el broker."""

    corte: int
    aviso: int | None = None
    bucle_repeticiones: int | None = None
    bucle_ms: int | None = None

    def __post_init__(self) -> None:
        if self.corte <= 0:
            raise FrenoError(f"el corte es un numero de peticiones positivo, no {self.corte}")
        if self.aviso is not None and not 0 < self.aviso < self.corte:
            raise FrenoError(f"el aviso ({self.aviso}) va por debajo del corte ({self.corte})")
        if (self.bucle_repeticiones is None) != (self.bucle_ms is None):
            raise FrenoError("el freno de bucles lleva repeticiones Y ventana, o ninguna")
        if self.bucle_repeticiones is not None and self.bucle_repeticiones < 2:
            raise FrenoError("un bucle son al menos 2 peticiones iguales")
        if self.bucle_ms is not None and self.bucle_ms <= 0:
            raise FrenoError("la ventana del bucle es positiva")


@dataclass(frozen=True)
class Corte:
    """Una entrada del registro del freno: el aviso del dia o una peticion negada, con su motivo."""

    instante_ms: int
    tipo: str  # el de la peticion (`colocar`, `modificar`...), o el motivo en un aviso
    id: str
    motivo: str  # MOTIVO_AVISO, MOTIVO_CORTE o MOTIVO_BUCLE


@dataclass
class FrenoPeticiones:
    """El freno de UNA cuenta. `admitir` decide cada peticion antes de enviarla."""

    limites: LimitesFreno
    cortes: list[Corte] = field(default_factory=list)
    _dia: date | None = None
    _total: int = 0
    _avisado: bool = False
    _cortado: str | None = None  # el motivo del corte del dia, si lo hay
    _recientes: deque[tuple[int, Hashable]] = field(default_factory=deque)

    def total(self) -> int:
        """Las peticiones enviadas el dia en curso (las negadas no cuentan)."""
        return self._total

    def cortado(self) -> str | None:
        """El motivo por el que el dia en curso ya no envia lo que no protege, o None."""
        return self._cortado

    def admitir(
        self,
        dia: date,
        instante_ms: int,
        tipo: str,
        id: str,
        firma: Hashable | None,
        protege: bool,
    ) -> str | None:
        """None si la peticion sale (y se cuenta); si no, el motivo por el que se niega.

        `dia` es el dia de la firma del instante; `firma` es el contenido de la peticion sin su
        id, para reconocer las iguales (None si no se compara); `protege` es si protege la
        cuenta: entonces sale siempre."""
        self._cambiar_de_dia(dia)
        if protege:
            self._contar(instante_ms)
            return None
        if self._cortado is None and self._total >= self.limites.corte:
            self._cortar(MOTIVO_CORTE, instante_ms, f"{self._total} peticiones")
        if self._cortado is None and self._es_bucle(instante_ms, firma):
            self._cortar(MOTIVO_BUCLE, instante_ms, f"{self.limites.bucle_repeticiones} iguales")
        if self._cortado is not None:
            self.cortes.append(Corte(instante_ms, tipo, id, self._cortado))
            return self._cortado
        if firma is not None and self.limites.bucle_ms is not None:
            self._recientes.append((instante_ms, firma))
        self._contar(instante_ms)
        return None

    def _cambiar_de_dia(self, dia: date) -> None:
        if dia == self._dia:
            return
        self._dia = dia
        self._total = 0
        self._avisado = False
        self._cortado = None
        self._recientes.clear()

    def _contar(self, instante_ms: int) -> None:
        self._total += 1
        aviso = self.limites.aviso
        if aviso is not None and not self._avisado and self._total >= aviso:
            self._avisado = True
            self.cortes.append(Corte(instante_ms, MOTIVO_AVISO, "", MOTIVO_AVISO))
            LOG.warning(
                "freno de peticiones: AVISO, %d peticiones el %s (aviso en %d, corte en %d)",
                self._total, self._dia, aviso, self.limites.corte,
            )  # fmt: skip

    def _es_bucle(self, instante_ms: int, firma: Hashable | None) -> bool:
        n, ventana = self.limites.bucle_repeticiones, self.limites.bucle_ms
        if firma is None or n is None or ventana is None:
            return False
        while self._recientes and self._recientes[0][0] <= instante_ms - ventana:
            self._recientes.popleft()
        iguales = sum(1 for _, f in self._recientes if f == firma)
        return iguales + 1 >= n

    def _cortar(self, motivo: str, instante_ms: int, detalle: str) -> None:
        self._cortado = motivo
        LOG.warning(
            "freno de peticiones: CORTE (%s, %s) el %s en el instante %d; desde aqui solo sale lo "
            "que protege la cuenta",
            motivo, detalle, self._dia, instante_ms,
        )  # fmt: skip


__all__ = [
    "MOTIVOS_QUE_NIEGAN",
    "MOTIVO_AVISO",
    "MOTIVO_BUCLE",
    "MOTIVO_CORTE",
    "Corte",
    "FrenoError",
    "FrenoPeticiones",
    "LimitesFreno",
]
