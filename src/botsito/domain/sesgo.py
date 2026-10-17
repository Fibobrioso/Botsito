"""El sesgo H4 (RN-003, ADR-0044): la primera regla del motor. Puro, sobre velas ya agregadas.

RN-003: el sesgo es el de la vela H4 previa cerrada; cambia solo si esa vela rompio el extremo de
la anterior -basta con la mecha- Y cerro del color de esa ruptura (WhatsApp del trader del
2026-10-14, ADR-0080: rompe el bajo y cierra roja, bajista; rompe el maximo y cierra verde,
alcista); un equal no lo cambia. ADR-0044 fija lo que RN-003 no decia:

- se fija AL ABRIR la sesion y solo cuentan las H4 cuyo FIN no es posterior a la apertura. La vela
  se da por cerrada por su hora de fin, NO por su marca `completa`, que depende de cuantas M1 le
  llegaron a la agregacion: asi el resultado no puede mirar el futuro por mucho que se le pase;
- romper es superar el extremo por poco que sea: en puntos enteros, estrictamente mayor. Igual es
  un equal, y no rompe;
- si la vela rompe LOS DOS extremos, decide el COLOR con que cierra: verde, alcista; roja, bajista
  (sesion 3, A-34 RESUELTA; ADR-0060). Si cierra sin cuerpo -neutra, sin color- NO DECIDE: la
  busqueda sigue hacia atras como si no hubiera roto nada (sesion 4, S-13; ADR-0075, que enmienda
  ADR-0060 §2: hasta entonces daba AMBIGUO);
- si la vela rompe UN extremo y cierra del color contrario -rompe el maximo y cierra roja, o rompe
  el minimo y cierra verde- NO DECIDE y la busqueda sigue: «sigue el sesgo que habia» (ADR-0080,
  D1; hasta entonces el color no contaba con un solo extremo roto). Si cierra sin cuerpo, tampoco
  decide (ADR-0080, D3: decision del consultor, pendiente de confirmar con el trader);
- el estado inicial se busca hacia atras, como mucho `tope` velas; si ninguna rompio con el color
  de su ruptura, INSUFICIENTE.

Con INSUFICIENTE no se opera (RN-033). AMBIGUO sigue declarado porque la forma de RN-033, los
scripts de diagnostico y el visor lo nombran, pero ninguna vela lo produce desde ADR-0075. Las
cifras no viven aqui (ADR-0002): el tope y el criterio de ruptura los pasa quien llama, leidos del
registro. La rejilla H4 -`anclaje_h4`, con su huso- la construye `data.agregacion`; el dominio no
sabe de husos.
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
    # Declarado y SIN PRODUCTOR desde ADR-0075: la vela neutra con doble ruptura ya no lo da. Se
    # queda por la forma de RN-033 (`vale: ambiguo`), los scripts y el visor; retirarlo es deuda.
    AMBIGUO = "ambiguo"
    INSUFICIENTE = "insuficiente"


@dataclass(frozen=True, slots=True)
class ResultadoSesgo:
    sesgo: Sesgo
    # Cuanto supero la vela que fija el sesgo el extremo de su anterior, en puntos: con doble
    # ruptura decidida por el color, la del lado del color. None si no hubo ruptura (INSUFICIENTE).
    # Sirve para ver cuantas rupturas caen en la zona de A-16, donde la serie del trader y la
    # nuestra pueden discrepar.
    ruptura_puntos: int | None
    # Cuantas velas se miraron hacia atras hasta decidir (las saltadas cuentan).
    velas_miradas: int
    # La vela que fija el sesgo rompio LOS DOS extremos de su anterior y el lado lo dio su color.
    # Una doble ruptura sin cuerpo no fija nada (ADR-0075), asi que nunca llega aqui.
    doble_ruptura: bool = False
    # Las H4 que la busqueda salto ANTES de la que fija el sesgo (o hasta el tope), por que no
    # decidieron; el arnes las cuenta por sesion (ADR-0080, 4.f del encargo):
    # rompio UN extremo y cerro del color contrario (ADR-0080, D1);
    saltadas_color_contrario: int = 0
    # rompio UN extremo y cerro sin cuerpo (ADR-0080, D3);
    saltadas_neutras_simples: int = 0
    # rompio LOS DOS extremos y cerro sin cuerpo (ADR-0075).
    saltadas_neutras_dobles: int = 0


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
    saltadas = [0, 0, 0]  # color contrario (D1), neutra simple (D3), neutra doble (ADR-0075)

    def fija(sesgo: Sesgo, puntos: int | None, doble: bool) -> ResultadoSesgo:
        return ResultadoSesgo(sesgo, puntos, miradas, doble, *saltadas)

    for i in range(len(cerradas) - 1, 0, -1):
        if miradas == tope:
            break
        miradas += 1
        vela = cerradas[i]
        alto, bajo = _extremos(vela, criterio)
        alto_ant, bajo_ant = _extremos(cerradas[i - 1], criterio)
        arriba, abajo = alto - alto_ant, bajo_ant - bajo
        # El color es el del cuerpo, cierre contra apertura, sea cual sea el criterio de ruptura.
        verde, roja = vela.cierre > vela.abierta, vela.cierre < vela.abierta
        if arriba > 0 and abajo > 0:
            # Doble ruptura: «importa el color de la vela» (sesion 3, A-34; ADR-0060 §1).
            if verde:
                return fija(Sesgo.ALCISTA, arriba, True)
            if roja:
                return fija(Sesgo.BAJISTA, abajo, True)
            # Neutra, sin color: no decide. «si esta es una vela neutra, no tiene ningún color,
            # nosotros seguiríamos operando alcistas» (sesion 4, S-13; ADR-0075). Se sigue hacia
            # atras; ADR-0060 §2 daba AMBIGUO aqui.
            saltadas[2] += 1
        elif arriba > 0 or abajo > 0:
            # Ruptura de UN extremo: decide solo si cierra del color de esa ruptura (ADR-0080):
            # «la vela roja debe de haber roto con cuerpo o con mecha el bajo de la vela alcista
            # [...] Y terminar al cierre bajista» (WhatsApp del 2026-10-14, 14:55).
            if arriba > 0 and verde:
                return fija(Sesgo.ALCISTA, arriba, False)
            if abajo > 0 and roja:
                return fija(Sesgo.BAJISTA, abajo, False)
            # Del color contrario (D1) o sin cuerpo (D3): «sigue el sesgo que habia».
            saltadas[0 if (verde or roja) else 1] += 1
    return fija(Sesgo.INSUFICIENTE, None, False)


__all__ = ["CUERPO", "MECHA", "ResultadoSesgo", "Sesgo", "SesgoError", "sesgo_h4"]
