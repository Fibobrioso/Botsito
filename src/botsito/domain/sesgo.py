"""El sesgo H4 (RN-003, ADR-0044): la primera regla del motor. Puro, sobre velas ya agregadas.

RN-003: el sesgo es el de la vela H4 previa cerrada; cambia solo si esa vela rompio el extremo de
la anterior, y basta con la mecha; un equal no lo cambia. ADR-0044 fija lo que RN-003 no decia:

- se fija AL ABRIR la sesion y solo cuentan las H4 cuyo FIN no es posterior a la apertura. La vela
  se da por cerrada por su hora de fin, NO por su marca `completa`, que depende de cuantas M1 le
  llegaron a la agregacion: asi el resultado no puede mirar el futuro por mucho que se le pase;
- romper es superar el extremo por poco que sea: en puntos enteros, estrictamente mayor. Igual es
  un equal, y no rompe;
- si la vela rompe LOS DOS extremos, el sesgo es AMBIGUO (A-34 abierta);
- el estado inicial se busca hacia atras, como mucho `tope` velas; si ninguna rompio, INSUFICIENTE.

Con AMBIGUO o INSUFICIENTE no se opera. Las cifras no viven aqui (ADR-0002): el tope y el criterio
de ruptura los pasa quien llama, leidos del registro. La rejilla H4 -`anclaje_h4`, con su huso- la
construye `data.agregacion`; el dominio no sabe de husos.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum

from botsito.domain.velas import MinutoUtc, Vela

# Las opciones de `sesgo_h4_criterio_ruptura` (parametros.yaml): que extremos de la vela cuentan.
MECHA, CUERPO = "mecha", "cuerpo"


class SesgoError(ValueError):
    """Argumentos que el sesgo no admite."""


class Sesgo(Enum):
    ALCISTA = "alcista"
    BAJISTA = "bajista"
    AMBIGUO = "ambiguo"
    INSUFICIENTE = "insuficiente"


@dataclass(frozen=True, slots=True)
class ResultadoSesgo:
    sesgo: Sesgo
    # Cuanto supero la vela que fija el sesgo el extremo de su anterior, en puntos; en AMBIGUO, la
    # menor de las dos rupturas. None si no hubo ruptura (INSUFICIENTE). Sirve para ver cuantas
    # rupturas caen en la zona de A-16, donde la serie del trader y la nuestra pueden discrepar.
    ruptura_puntos: int | None
    # Cuantas velas se miraron hacia atras hasta decidir.
    velas_miradas: int


def _extremos(vela: Vela, criterio: str) -> tuple[int, int]:
    if criterio == MECHA:
        return vela.maxima, vela.minima
    if criterio == CUERPO:
        return max(vela.abierta, vela.cierre), min(vela.abierta, vela.cierre)
    raise SesgoError(f"criterio de ruptura {criterio!r} fuera de ({MECHA!r}, {CUERPO!r})")


def sesgo_h4(
    velas_h4: Sequence[Vela], apertura_sesion: MinutoUtc, tope: int, criterio: str
) -> ResultadoSesgo:
    """El sesgo al abrir la sesion que empieza en `apertura_sesion` (minuto UTC)."""
    if tope <= 0:
        raise SesgoError("el tope de velas hacia atras es un entero positivo")
    cerradas = sorted((v for v in velas_h4 if v.fin <= apertura_sesion), key=lambda v: v.inicio)
    miradas = 0
    for i in range(len(cerradas) - 1, 0, -1):
        if miradas == tope:
            break
        miradas += 1
        alto, bajo = _extremos(cerradas[i], criterio)
        alto_ant, bajo_ant = _extremos(cerradas[i - 1], criterio)
        arriba, abajo = alto - alto_ant, bajo_ant - bajo
        if arriba > 0 and abajo > 0:
            return ResultadoSesgo(Sesgo.AMBIGUO, min(arriba, abajo), miradas)
        if arriba > 0:
            return ResultadoSesgo(Sesgo.ALCISTA, arriba, miradas)
        if abajo > 0:
            return ResultadoSesgo(Sesgo.BAJISTA, abajo, miradas)
    return ResultadoSesgo(Sesgo.INSUFICIENTE, None, miradas)


__all__ = ["CUERPO", "MECHA", "ResultadoSesgo", "Sesgo", "SesgoError", "sesgo_h4"]
