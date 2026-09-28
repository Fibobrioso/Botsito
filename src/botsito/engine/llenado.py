"""El modelo de llenado (ADR-0051, PROPUESTO): cuando y a que precio ocurre cada evento.

FUNCIONES PURAS sobre un `Mercado` que entrega, minuto a minuto, los ticks (si los hay) o la vela
M1 BID de respaldo con un spread supuesto. Sin IO, sin reloj, sin cifras de negocio: lo elegible
viene en `Configuracion`, que el broker lee de `knowledge/simulador/llenado.yaml`.

- Una cuenta compra al ASK y vende al BID (ADR-0051 §1). Las limites y los objetivos exigen que el
  lado relevante pase ESTRICTAMENTE mas alla de su nivel (o lo toque, si la configuracion lo dice);
  los stops saltan al TOCARLO.
- Con ticks, el orden real: gana el primer tick que cumpla; si el mismo tick cumple stop y objetivo,
  gana el stop (§3). Un evento nunca se evalua contra el tick en el que se decidio: solo contra los
  posteriores (`desde_ms` exclusivo).
- Sin ticks en un minuto, el RESPALDO M1: pesimista, el stop primero, y el evento en el CIERRE de
  la vela, marcado `respaldo_m1` (§3, §5). Un stop se llena a su nivel salvo que la vela abra mas
  alla: entonces a la apertura (§4, deslizamiento de hueco).
- Sin deslizamiento fijo salvo que la configuracion lo declare (§4).
- La ORDEN STOP DE ENTRADA (ADR-0056 §2, ADR-0057) salta al tocar su nivel y se llena al precio
  del tick que la dispara, como el stop de una posicion; y una pendiente del lado equivocado del
  precio se reconoce con `lado_equivocado` sobre la cotizacion del momento (`Mercado.cotizacion`).

SIN MIRAR AL FUTURO: cada funcion recorre desde `desde_ms` hacia delante y se detiene en el primer
evento; nada de lo posterior cambia lo decidido.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from typing import Literal

from botsito.domain.ticks import MS_POR_MINUTO, Tick
from botsito.domain.velas import MinutoUtc, Vela

Lado = Literal["compra", "venta"]
TICKS = "ticks"
RESPALDO_M1 = "respaldo_m1"
LLENADO = "llenado"
STOP = "stop"
OBJETIVO = "objetivo"
# el tipo de una orden pendiente de entrada (ADR-0056 §1-2): la limite de siempre y la stop
TIPO_LIMITE = "limite"
TIPO_STOP = "stop"
TIPOS_ORDEN = (TIPO_LIMITE, TIPO_STOP)


class LlenadoError(ValueError):
    """Argumentos que el modelo no admite: nunca se adivina."""


@dataclass(frozen=True)
class Configuracion:
    """Lo elegible del modelo (ADR-0051), leido de configuracion por quien llama."""

    limite_llena_al_toque: bool
    deslizamiento_fijo_puntos: int
    # spread supuesto (puntos) para un minuto UTC sin ticks: lo define la configuracion por hora
    spread_supuesto: Callable[[MinutoUtc], int]


@dataclass(frozen=True)
class Evento:
    tipo: str  # LLENADO, STOP u OBJETIVO
    instante_ms: int
    precio: int  # puntos, el precio al que se ejecuta
    fuente: str  # TICKS o RESPALDO_M1
    minuto: MinutoUtc


class Mercado:
    """Lo que el modelo puede ver: ticks por minuto y, donde no hay, la M1 BID del repositorio."""

    def __init__(self, ticks: Sequence[Tick], m1: Sequence[Vela]) -> None:
        por_minuto: dict[int, list[Tick]] = {}
        anterior = -1
        for t in ticks:
            if t.instante < anterior:
                raise LlenadoError("ticks desordenados")
            anterior = t.instante
            por_minuto.setdefault(int(t.minuto), []).append(t)
        self._ticks: Mapping[int, Sequence[Tick]] = {k: tuple(v) for k, v in por_minuto.items()}
        self._m1: Mapping[int, Vela] = {int(v.inicio): v for v in m1}
        minutos = set(self._ticks) | set(self._m1)
        self.primero = MinutoUtc(min(minutos)) if minutos else None
        self.ultimo = MinutoUtc(max(minutos)) if minutos else None

    def ticks_del_minuto(self, minuto: int) -> Sequence[Tick] | None:
        return self._ticks.get(minuto)

    def m1(self, minuto: int) -> Vela | None:
        return self._m1.get(minuto)

    def cotizacion(
        self, instante_ms: int, spread_supuesto: Callable[[MinutoUtc], int]
    ) -> tuple[int, int, str] | None:
        """(bid, ask, fuente) en `instante_ms`: el ultimo tick anterior o igual; donde no hay ticks,
        la ultima M1 CERRADA (bid = cierre, ask = cierre mas el spread supuesto, ADR-0051 §1). Mira
        hacia atras hasta el primer minuto del mercado; sin nada, None (ADR-0057, PROVISIONAL)."""
        if self.primero is None:
            return None
        minuto = instante_ms // MS_POR_MINUTO
        for k in range(minuto, int(self.primero) - 1, -1):
            ticks = self._ticks.get(k)
            if ticks:
                previos = [t for t in ticks if t.instante <= instante_ms]
                if previos:
                    return int(previos[-1].bid), int(previos[-1].ask), TICKS
                continue
            vela = self._m1.get(k)
            if vela is not None and _fin_ms(vela) <= instante_ms:
                bid = int(vela.cierre)
                return bid, bid + spread_supuesto(MinutoUtc(k)), RESPALDO_M1
        return None


def _fin_ms(vela: Vela) -> int:
    return int(vela.fin) * MS_POR_MINUTO


def _pasa(valor: int, nivel: int, sentido: int, al_toque: bool) -> bool:
    """`sentido` +1: el valor tiene que superar el nivel; -1: quedar por debajo."""
    if sentido > 0:
        return valor >= nivel if al_toque else valor > nivel
    return valor <= nivel if al_toque else valor < nivel


def _minutos(desde_ms: int, hasta_ms: int) -> range:
    return range(desde_ms // MS_POR_MINUTO, (hasta_ms - 1) // MS_POR_MINUTO + 1)


def primer_llenado_limite(
    lado: Lado,
    precio: int,
    desde_ms: int,
    hasta_ms: int,
    mercado: Mercado,
    config: Configuracion,
) -> Evento | None:
    """El primer instante en (desde_ms, hasta_ms) en que una LIMITE se llena, o None si no llega.

    Compra: el ASK pasa por debajo del precio. Venta: el BID pasa por encima (ADR-0051 §1-2). El
    precio de llenado es el de la orden.
    """
    if hasta_ms <= desde_ms:
        return None
    sentido = -1 if lado == "compra" else 1
    for m in _minutos(desde_ms, hasta_ms):
        ticks = mercado.ticks_del_minuto(m)
        if ticks is not None:
            for t in ticks:
                if t.instante <= desde_ms:
                    continue
                if t.instante >= hasta_ms:
                    return None
                valor = int(t.ask) if lado == "compra" else int(t.bid)
                if _pasa(valor, precio, sentido, config.limite_llena_al_toque):
                    return Evento(LLENADO, int(t.instante), precio, TICKS, MinutoUtc(m))
            continue
        vela = mercado.m1(m)
        if vela is None or _fin_ms(vela) <= desde_ms or _fin_ms(vela) > hasta_ms:
            continue
        spread = config.spread_supuesto(MinutoUtc(m))
        # compra: el ASK mas bajo de la vela es la minima BID mas el spread; venta: la maxima BID
        extremo = int(vela.minima) + spread if lado == "compra" else int(vela.maxima)
        if _pasa(extremo, precio, sentido, config.limite_llena_al_toque):
            return Evento(LLENADO, _fin_ms(vela), precio, RESPALDO_M1, MinutoUtc(m))
    return None


def primer_llenado_stop(
    lado: Lado,
    precio: int,
    desde_ms: int,
    hasta_ms: int,
    mercado: Mercado,
    config: Configuracion,
) -> Evento | None:
    """El primer instante en (desde_ms, hasta_ms) en que una orden STOP DE ENTRADA salta, o None.

    ADR-0056 §2 y ADR-0057: una venta stop salta cuando el BID toca o baja del nivel; una compra
    stop, cuando el ASK lo toca o lo sube. Es AL TOQUE, como el stop de una posicion (DN-1). Se
    llena al precio del tick que la dispara, mas el deslizamiento fijo de la configuracion (DN-3):
    si el tick llega ya pasado el nivel (hueco), a ese precio, peor que el nivel, nunca al nivel.
    Respaldo M1 (solo para depurar, ADR-0051 §8): la vela es BID y el ASK es BID mas el spread
    supuesto; al nivel, o a la APERTURA si la vela abre ya pasada; sellado al cierre de la vela,
    como la limite. La misma convencion que el stop de una posicion (§4)."""
    if hasta_ms <= desde_ms:
        return None
    compra = lado == "compra"
    for m in _minutos(desde_ms, hasta_ms):
        ticks = mercado.ticks_del_minuto(m)
        if ticks is not None:
            for t in ticks:
                if t.instante <= desde_ms:
                    continue
                if t.instante >= hasta_ms:
                    return None
                valor = int(t.ask) if compra else int(t.bid)
                if (valor >= precio) if compra else (valor <= precio):
                    return Evento(
                        LLENADO,
                        int(t.instante),
                        _deslizar_entrada(valor, compra, config),
                        TICKS,
                        MinutoUtc(m),
                    )
            continue
        vela = mercado.m1(m)
        if vela is None or _fin_ms(vela) <= desde_ms or _fin_ms(vela) > hasta_ms:
            continue
        desplazamiento = config.spread_supuesto(MinutoUtc(m)) if compra else 0
        abre = int(vela.abierta) + desplazamiento
        extremo = int(vela.maxima) + desplazamiento if compra else int(vela.minima)
        if (extremo >= precio) if compra else (extremo <= precio):
            hueco = abre > precio if compra else abre < precio
            return Evento(
                LLENADO,
                _fin_ms(vela),
                _deslizar_entrada(abre if hueco else precio, compra, config),
                RESPALDO_M1,
                MinutoUtc(m),
            )
    return None


def _deslizar_entrada(precio: int, compra: bool, config: Configuracion) -> int:
    """El deslizamiento de una ENTRADA va en contra: una compra paga mas, una venta cobra menos."""
    d = config.deslizamiento_fijo_puntos
    return precio + d if compra else precio - d


def lado_equivocado(tipo: str, lado: Lado, precio: int, bid: int, ask: int) -> bool:
    """Si una pendiente esta del lado equivocado del precio al colocarla (ADR-0056 §3, ADR-0057):
    una LIMITE de venta por debajo del BID o de compra por encima del ASK (el precio ya la paso);
    una STOP de venta por encima del BID o de compra por debajo del ASK. En el nivel exacto no es
    lado equivocado: la limite espera y la stop salta al siguiente tick (PROVISIONAL)."""
    if tipo == TIPO_LIMITE:
        return precio < bid if lado == "venta" else precio > ask
    if tipo == TIPO_STOP:
        return precio > bid if lado == "venta" else precio < ask
    raise LlenadoError(f"tipo de orden {tipo!r} desconocido")


def primera_salida(
    lado: Lado,
    stop: int,
    objetivo: int,
    desde_ms: int,
    hasta_ms: int,
    mercado: Mercado,
    config: Configuracion,
) -> Evento | None:
    """Que toca antes desde una posicion abierta: el STOP o el OBJETIVO (ADR-0051 §3-4).

    Larga: stop si el BID toca o baja del stop; objetivo si el BID pasa por encima. Corta: stop si
    el ASK toca o supera el stop; objetivo si el ASK pasa por debajo. Con ticks, el primero que
    ocurra (empate: stop, al precio del tick que lo dispara). Con respaldo M1: el stop primero.
    """
    if hasta_ms <= desde_ms:
        return None
    larga = lado == "compra"
    if larga and not stop < objetivo:
        raise LlenadoError("una larga lleva el stop por debajo del objetivo")
    if not larga and not stop > objetivo:
        raise LlenadoError("una corta lleva el stop por encima del objetivo")
    for m in _minutos(desde_ms, hasta_ms):
        ticks = mercado.ticks_del_minuto(m)
        if ticks is not None:
            for t in ticks:
                if t.instante <= desde_ms:
                    continue
                if t.instante >= hasta_ms:
                    return None
                valor = int(t.bid) if larga else int(t.ask)
                toca_stop = valor <= stop if larga else valor >= stop
                if toca_stop:
                    return Evento(
                        STOP,
                        int(t.instante),
                        _con_deslizamiento(valor, larga, config),
                        TICKS,
                        MinutoUtc(m),
                    )
                if _pasa(valor, objetivo, 1 if larga else -1, config.limite_llena_al_toque):
                    return Evento(OBJETIVO, int(t.instante), objetivo, TICKS, MinutoUtc(m))
            continue
        vela = mercado.m1(m)
        if vela is None or _fin_ms(vela) <= desde_ms or _fin_ms(vela) > hasta_ms:
            continue
        spread = config.spread_supuesto(MinutoUtc(m))
        # larga: mira el BID (la vela es BID); corta: mira el ASK = BID + spread
        desplazamiento = 0 if larga else spread
        abre = int(vela.abierta) + desplazamiento
        peor = int(vela.minima) + desplazamiento if larga else int(vela.maxima) + desplazamiento
        mejor = int(vela.maxima) + desplazamiento if larga else int(vela.minima) + desplazamiento
        toca_stop = peor <= stop if larga else peor >= stop
        if toca_stop:
            # hueco: si la vela ABRE mas alla del stop, se llena a la apertura (§4)
            salta = abre < stop if larga else abre > stop
            precio = abre if salta else stop
            return Evento(
                STOP,
                _fin_ms(vela),
                _con_deslizamiento(precio, larga, config),
                RESPALDO_M1,
                MinutoUtc(m),
            )
        if _pasa(mejor, objetivo, 1 if larga else -1, config.limite_llena_al_toque):
            return Evento(OBJETIVO, _fin_ms(vela), objetivo, RESPALDO_M1, MinutoUtc(m))
    return None


def _con_deslizamiento(precio: int, larga: bool, config: Configuracion) -> int:
    d = config.deslizamiento_fijo_puntos
    return precio - d if larga else precio + d


def spread_por_hora(
    tabla: Mapping[int, int], por_defecto: int, hora_local_de: Callable[[MinutoUtc], int]
) -> Callable[[MinutoUtc], int]:
    """Construye el `spread_supuesto` de `Configuracion` desde una tabla hora local -> puntos."""

    def spread(minuto: MinutoUtc) -> int:
        return tabla.get(hora_local_de(minuto), por_defecto)

    return spread


__all__ = [
    "LLENADO",
    "OBJETIVO",
    "RESPALDO_M1",
    "STOP",
    "TICKS",
    "TIPOS_ORDEN",
    "TIPO_LIMITE",
    "TIPO_STOP",
    "Configuracion",
    "Evento",
    "Lado",
    "LlenadoError",
    "Mercado",
    "lado_equivocado",
    "primer_llenado_limite",
    "primer_llenado_stop",
    "primera_salida",
    "spread_por_hora",
]
