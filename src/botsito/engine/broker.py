"""El broker simulado (ADR-0052, PROPUESTO): ordenes, posiciones y lo que la cuenta recibe.

Estado puro sobre un `Mercado` (ticks donde los hay, M1 de respaldo donde no) y el modelo de
llenado de ADR-0051. Sin IO, sin reloj de pared, sin cifras de negocio: los limites de la firma
vienen de `ReglasBroker` (leidas del perfil de cuenta por quien llama) y lo elegible del llenado
de `Configuracion`. Nada aqui asume un instrumento ni una firma.

CICLO DE VIDA de una orden limite: colocada -> (modificada)* -> llenada | cancelada | expirada;
o rechazada al colocarla por un limite del perfil (volumen maximo, ordenes simultaneas, posiciones
por dia), y el rechazo queda registrado. Una orden llenada abre una POSICION con stop y objetivo,
que se cierra por stop, por objetivo o a mercado (cierre manual). Cada cierre produce una
`cuenta.Operacion` con sus cargos -comision por lado si el perfil lo dice, swap por cada corte
diario del perfil que la posicion cruce- y sus MARCAS: el peor precio de cada minuto vivo, que es
lo que la capa de cuenta vigila (ADR-0050). La equity de la cuenta en cualquier marca es el saldo
mas el flotante de las posiciones del broker: un test lo comprueba.

NO se cablea al motor de reglas (ADR-0052 §5): el motor sigue sin tocarse. Este broker expone el
contrato que el motor tendra que cumplir -colocar, modificar, cancelar, cerrar a mercado, y leer
los hechos de origen broker `operacion_abierta` y `orden_limite_pendiente`- y `avanzar(hasta)`,
que procesa los eventos en orden de instante SIN MIRAR AL FUTURO: cada evento sale del primer
instante en que su condicion se cumple y nada posterior lo cambia.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal
from zoneinfo import ZoneInfo

from botsito.domain.ticks import MS_POR_MINUTO
from botsito.domain.velas import MinutoUtc
from botsito.engine.cuenta import Cargo, Marca, Operacion
from botsito.engine.llenado import (
    RESPALDO_M1,
    TICKS,
    Configuracion,
    Evento,
    Lado,
    Mercado,
    primer_llenado_limite,
    primera_salida,
)

COLOCADA = "colocada"
MODIFICADA = "modificada"
LLENADA = "llenada"
CANCELADA = "cancelada"
EXPIRADA = "expirada"
RECHAZADA = "rechazada"
MANUAL = "manual"
HECHO_OPERACION_ABIERTA = "operacion_abierta"
HECHO_ORDEN_PENDIENTE = "orden_limite_pendiente"
_EPOCA = datetime(1970, 1, 1, tzinfo=UTC)


class BrokerError(ValueError):
    """Una peticion que el broker no admite: nunca se adivina."""


@dataclass(frozen=True)
class ReglasBroker:
    """Los limites del perfil de cuenta y los costes, ya leidos por quien llama."""

    volumen_max_lotes: Decimal
    ordenes_simultaneas_max: int
    posiciones_dia_max: int
    huso_corte: ZoneInfo  # el dia de la firma (posiciones por dia) y el corte del swap
    comision_por_lote: Decimal  # moneda de la cuenta por lote
    comision_por_lado: bool
    swap_largo_puntos: Decimal  # por lote y noche, con signo (negativo = cuesta)
    swap_corto_puntos: Decimal


@dataclass
class Orden:
    id: str
    lado: Lado
    precio: int
    lotes: Decimal
    stop: int
    objetivo: int
    colocada_ms: int
    expira_ms: int | None
    estado: str = COLOCADA
    ultimo_cambio_ms: int = 0
    historial: list[tuple[int, str]] = field(default_factory=list)  # (instante, estado)


@dataclass
class Posicion:
    id: str
    orden_id: str
    lado: Lado
    lotes: Decimal
    entrada: int
    stop: int
    objetivo: int
    abierta_ms: int
    fuente_apertura: str
    cerrada_ms: int | None = None
    precio_cierre: int | None = None
    motivo_cierre: str | None = None
    fuente_cierre: str | None = None
    ultimo_precio: int = 0
    marcas: list[tuple[int, int]] = field(default_factory=list)  # (instante_ms, peor precio)
    swaps: list[tuple[int, Decimal]] = field(default_factory=list)

    @property
    def abierta(self) -> bool:
        return self.cerrada_ms is None


@dataclass(frozen=True)
class Rechazo:
    instante_ms: int
    orden_id: str
    motivo: str


@dataclass(frozen=True)
class Traza:
    """Lo que el broker hizo, para el informe: eventos con su fuente y rechazos."""

    eventos: tuple[tuple[int, str, str, str], ...]  # (instante_ms, tipo, id, fuente)
    rechazos: tuple[Rechazo, ...]

    def por_fuente(self) -> dict[str, int]:
        salida = {TICKS: 0, RESPALDO_M1: 0}
        for _, _, _, fuente in self.eventos:
            salida[fuente] = salida.get(fuente, 0) + 1
        return salida


def _instante(ms: int) -> datetime:
    return _EPOCA + timedelta(milliseconds=ms)


def _dia_local(ms: int, huso: ZoneInfo) -> date:
    return _instante(ms).astimezone(huso).date()


def _medianoche_ms(dia: date, huso: ZoneInfo) -> int:
    return int(
        (datetime.combine(dia, time(0), tzinfo=huso).astimezone(UTC) - _EPOCA).total_seconds()
        * 1000
    )


class Broker:
    """El broker de UNA cuenta sobre UN mercado. Determinista: todo se ordena por instante e id."""

    def __init__(
        self,
        reglas: ReglasBroker,
        config: Configuracion,
        mercado: Mercado,
        contrato: Decimal,
        escala: int,
    ) -> None:
        if contrato <= 0 or escala <= 0:
            raise BrokerError("contrato y escala son positivos")
        self.reglas = reglas
        self.config = config
        self.mercado = mercado
        self.contrato = contrato
        self.escala = escala
        self.ordenes: dict[str, Orden] = {}
        self.posiciones: dict[str, Posicion] = {}
        self._rechazos: list[Rechazo] = []
        self._eventos: list[tuple[int, str, str, str]] = []
        self._cerradas: list[Operacion] = []
        self.ahora_ms: int = 0

    # ------------------------------------------------------------------- el contrato del motor

    def colocar_limite(
        self,
        id: str,
        lado: Lado,
        precio: int,
        lotes: Decimal,
        stop: int,
        objetivo: int,
        instante_ms: int,
        expira_ms: int | None = None,
    ) -> Orden | Rechazo:
        """Coloca una limite. Un limite del perfil la RECHAZA y lo registra, no la encola."""
        self._avanza_reloj(instante_ms)
        if id in self.ordenes:
            raise BrokerError(f"orden {id!r} repetida")
        if lotes <= 0:
            raise BrokerError(f"{id}: lotes no positivos")
        if lado == "compra" and not stop < precio < objetivo:
            raise BrokerError(f"{id}: una compra lleva stop < precio < objetivo")
        if lado == "venta" and not objetivo < precio < stop:
            raise BrokerError(f"{id}: una venta lleva objetivo < precio < stop")
        motivo = self._limite_infringido(lotes, instante_ms)
        if motivo is not None:
            r = Rechazo(instante_ms, id, motivo)
            self._rechazos.append(r)
            self.ordenes[id] = Orden(
                id, lado, precio, lotes, stop, objetivo, instante_ms, expira_ms, RECHAZADA,
                instante_ms, [(instante_ms, RECHAZADA)],
            )  # fmt: skip
            return r
        orden = Orden(
            id, lado, precio, lotes, stop, objetivo, instante_ms, expira_ms, COLOCADA, instante_ms,
            [(instante_ms, COLOCADA)],
        )  # fmt: skip
        self.ordenes[id] = orden
        return orden

    def modificar(
        self,
        id: str,
        instante_ms: int,
        precio: int | None = None,
        stop: int | None = None,
        objetivo: int | None = None,
    ) -> Orden:
        self._avanza_reloj(instante_ms)
        orden = self._pendiente(id)
        orden.precio = precio if precio is not None else orden.precio
        orden.stop = stop if stop is not None else orden.stop
        orden.objetivo = objetivo if objetivo is not None else orden.objetivo
        orden.estado = MODIFICADA
        orden.ultimo_cambio_ms = instante_ms
        orden.historial.append((instante_ms, MODIFICADA))
        return orden

    def cancelar(self, id: str, instante_ms: int) -> Orden:
        self._avanza_reloj(instante_ms)
        orden = self._pendiente(id)
        orden.estado = CANCELADA
        orden.ultimo_cambio_ms = instante_ms
        orden.historial.append((instante_ms, CANCELADA))
        return orden

    def cerrar_a_mercado(self, posicion_id: str, instante_ms: int) -> Posicion:
        """Cierra al precio de mercado del instante: el ultimo tick anterior o igual, o el cierre
        de la M1 del minuto (respaldo). Sin precio disponible, no se puede cerrar y se dice."""
        self.avanzar(instante_ms)
        p = self.posiciones.get(posicion_id)
        if p is None or not p.abierta:
            raise BrokerError(f"posicion {posicion_id!r} no esta abierta")
        precio, fuente = self._precio_de_mercado(p.lado, instante_ms)
        self._cerrar(p, instante_ms, precio, MANUAL, fuente)
        return p

    def abrir_conocida(
        self,
        id: str,
        lado: Lado,
        precio: int,
        lotes: Decimal,
        stop: int,
        objetivo: int,
        instante_ms: int,
        fuente: str = "conocida",
    ) -> Posicion:
        """Abre una posicion en un llenado CONOCIDO (una operacion real del trader, cuyo instante y
        precio de entrada trae el caso), sin pasar por el modelo de llenado: a partir de ahi, el
        stop, el objetivo y el cierre a mercado si se deciden con el modelo. Los limites del perfil
        se aplican igual y un rechazo levanta error, porque no hay orden que rechazar."""
        self._avanza_reloj(instante_ms)
        if id in self.posiciones:
            raise BrokerError(f"posicion {id!r} repetida")
        if lotes <= 0:
            raise BrokerError(f"{id}: lotes no positivos")
        motivo = self._limite_infringido(lotes, instante_ms)
        if motivo is not None:
            raise BrokerError(f"{id}: el perfil no admite esta posicion ({motivo})")
        p = Posicion(
            id, id, lado, lotes, precio, stop, objetivo, instante_ms, fuente, ultimo_precio=precio
        )
        self.posiciones[id] = p
        self._eventos.append((instante_ms, LLENADA, id, fuente))
        return p

    def hechos(self) -> dict[str, bool]:
        """Los hechos de origen `broker` de la spec, derivados del estado (ADR-0028 §5)."""
        return {
            HECHO_OPERACION_ABIERTA: any(p.abierta for p in self.posiciones.values()),
            HECHO_ORDEN_PENDIENTE: any(
                o.estado in (COLOCADA, MODIFICADA) for o in self.ordenes.values()
            ),
        }

    # ------------------------------------------------------------------------------ avanzar

    def avanzar(self, hasta_ms: int) -> list[tuple[int, str, str, str]]:
        """Procesa, en orden de instante, todo lo que ocurre en (ahora, hasta]: llenados,
        expiraciones, stops y objetivos. Devuelve los eventos de este tramo."""
        if hasta_ms < self.ahora_ms:
            raise BrokerError("no se avanza hacia atras")
        inicio = len(self._eventos)
        while True:
            candidato = self._proximo_evento(hasta_ms)
            if candidato is None:
                break
            instante, _, tipo, objeto, evento = candidato
            self._aplicar(tipo, objeto, evento, instante)
        self._marcar_hasta(hasta_ms)
        self.ahora_ms = hasta_ms
        return self._eventos[inicio:]

    def _proximo_evento(self, hasta_ms: int) -> tuple[int, str, str, str, Evento | None] | None:
        candidatos: list[tuple[int, str, str, str, Evento | None]] = []
        for o in sorted(self.ordenes.values(), key=lambda x: x.id):
            if o.estado not in (COLOCADA, MODIFICADA):
                continue
            tope = hasta_ms if o.expira_ms is None else min(hasta_ms, o.expira_ms)
            # el tick en el que se coloco o modifico no cuenta (exclusivo); el tick del ultimo
            # evento procesado SI puede llenar otra orden pendiente (por eso ahora - 1)
            ev = primer_llenado_limite(
                o.lado,
                o.precio,
                max(self.ahora_ms - 1, o.ultimo_cambio_ms),
                tope,
                self.mercado,
                self.config,
            )
            if ev is not None:
                candidatos.append((ev.instante_ms, o.id, LLENADA, o.id, ev))
            elif o.expira_ms is not None and self.ahora_ms < o.expira_ms <= hasta_ms:
                candidatos.append((o.expira_ms, o.id, EXPIRADA, o.id, None))
        for p in sorted(self.posiciones.values(), key=lambda x: x.id):
            if not p.abierta:
                continue
            ev = primera_salida(
                p.lado,
                p.stop,
                p.objetivo,
                max(self.ahora_ms - 1, p.abierta_ms),
                hasta_ms,
                self.mercado,
                self.config,
            )
            if ev is not None:
                candidatos.append((ev.instante_ms, p.id, ev.tipo, p.id, ev))
        if not candidatos:
            return None
        return min(candidatos, key=lambda c: (c[0], c[2], c[1]))

    def _aplicar(self, tipo: str, objeto: str, evento: Evento | None, instante: int) -> None:
        self._marcar_hasta(instante)
        self.ahora_ms = instante
        if tipo == EXPIRADA:
            o = self.ordenes[objeto]
            o.estado = EXPIRADA
            o.ultimo_cambio_ms = instante
            o.historial.append((instante, EXPIRADA))
            self._eventos.append((instante, EXPIRADA, o.id, TICKS))
            return
        assert evento is not None
        if tipo == LLENADA:
            o = self.ordenes[objeto]
            o.estado = LLENADA
            o.ultimo_cambio_ms = instante
            o.historial.append((instante, LLENADA))
            p = Posicion(
                f"pos-{o.id}", o.id, o.lado, o.lotes, evento.precio, o.stop, o.objetivo, instante,
                evento.fuente, ultimo_precio=evento.precio,
            )  # fmt: skip
            self.posiciones[p.id] = p
            self._eventos.append((instante, LLENADA, o.id, evento.fuente))
            return
        p = self.posiciones[objeto]
        self._cerrar(p, instante, evento.precio, evento.tipo, evento.fuente)

    def _cerrar(self, p: Posicion, instante: int, precio: int, motivo: str, fuente: str) -> None:
        p.cerrada_ms = instante
        p.precio_cierre = precio
        p.motivo_cierre = motivo
        p.fuente_cierre = fuente
        p.ultimo_precio = precio
        self._eventos.append((instante, motivo, p.id, fuente))
        self._cerradas.append(self._operacion(p))

    # ------------------------------------------------------------------------------ marcas

    def _marcar_hasta(self, hasta_ms: int) -> None:
        """El peor precio de cada minuto vivo, por posicion, desde el ultimo minuto marcado."""
        for p in self.posiciones.values():
            if not p.abierta:
                continue
            desde = (
                p.marcas[-1][0] // MS_POR_MINUTO + 1 if p.marcas else p.abierta_ms // MS_POR_MINUTO
            )
            for m in range(desde, hasta_ms // MS_POR_MINUTO + 1):
                peor = self._peor_del_minuto(p.lado, m, p.abierta_ms, hasta_ms)
                if peor is None:
                    continue
                p.marcas.append((min(m * MS_POR_MINUTO + MS_POR_MINUTO - 1, hasta_ms), peor))
                p.ultimo_precio = peor
            self._swaps(p, hasta_ms)

    def _peor_del_minuto(self, lado: Lado, minuto: int, desde_ms: int, hasta_ms: int) -> int | None:
        ticks = self.mercado.ticks_del_minuto(minuto)
        if ticks is not None:
            valores = [
                int(t.bid) if lado == "compra" else int(t.ask)
                for t in ticks
                if desde_ms <= t.instante <= hasta_ms
            ]
            if not valores:
                return None
            return min(valores) if lado == "compra" else max(valores)
        vela = self.mercado.m1(minuto)
        if vela is None or int(vela.fin) * MS_POR_MINUTO > hasta_ms + MS_POR_MINUTO:
            return None
        spread = self.config.spread_supuesto(MinutoUtc(minuto))
        return int(vela.minima) if lado == "compra" else int(vela.maxima) + spread

    def _swaps(self, p: Posicion, hasta_ms: int) -> None:
        """Un swap por cada corte diario del perfil que la posicion cruce viva."""
        ultimo = p.swaps[-1][0] if p.swaps else p.abierta_ms
        dia = _dia_local(ultimo, self.reglas.huso_corte) + timedelta(days=1)
        corte = _medianoche_ms(dia, self.reglas.huso_corte)
        while corte <= hasta_ms:
            puntos = (
                self.reglas.swap_largo_puntos
                if p.lado == "compra"
                else self.reglas.swap_corto_puntos
            )
            importe = -puntos * p.lotes * self.contrato / self.escala  # negativo = cuesta
            p.swaps.append((corte, importe))
            dia += timedelta(days=1)
            corte = _medianoche_ms(dia, self.reglas.huso_corte)

    # ---------------------------------------------------------------------------- consultas

    def _precio_de_mercado(self, lado: Lado, instante_ms: int) -> tuple[int, str]:
        minuto = instante_ms // MS_POR_MINUTO
        ticks = self.mercado.ticks_del_minuto(minuto)
        if ticks is not None:
            previos = [t for t in ticks if t.instante <= instante_ms]
            if previos:
                t = previos[-1]
                return (int(t.bid) if lado == "compra" else int(t.ask)), TICKS
        vela = self.mercado.m1(minuto)
        if vela is None:
            raise BrokerError(f"sin precio de mercado en el minuto {minuto}")
        spread = self.config.spread_supuesto(MinutoUtc(minuto))
        return (int(vela.cierre) if lado == "compra" else int(vela.cierre) + spread), RESPALDO_M1

    def flotante(self) -> Decimal:
        """El P/L flotante de las posiciones vivas a su ultimo precio marcado, en moneda."""
        total = Decimal(0)
        for p in self.posiciones.values():
            if p.abierta:
                signo = 1 if p.lado == "compra" else -1
                total += (
                    signo
                    * Decimal(p.ultimo_precio - p.entrada)
                    * p.lotes
                    * self.contrato
                    / self.escala
                )
        return total

    def _pendiente(self, id: str) -> Orden:
        o = self.ordenes.get(id)
        if o is None or o.estado not in (COLOCADA, MODIFICADA):
            raise BrokerError(f"orden {id!r} no esta pendiente")
        return o

    def _avanza_reloj(self, instante_ms: int) -> None:
        if instante_ms < self.ahora_ms:
            raise BrokerError("una peticion no puede ir hacia atras en el tiempo")
        self.avanzar(instante_ms)

    def _limite_infringido(self, lotes: Decimal, instante_ms: int) -> str | None:
        r = self.reglas
        if lotes > r.volumen_max_lotes:
            return "volumen_max_lotes"
        vivas = sum(1 for o in self.ordenes.values() if o.estado in (COLOCADA, MODIFICADA))
        vivas += sum(1 for p in self.posiciones.values() if p.abierta)
        if vivas >= r.ordenes_simultaneas_max:
            return "ordenes_simultaneas_max"
        dia = _dia_local(instante_ms, r.huso_corte)
        hoy = sum(
            1 for p in self.posiciones.values() if _dia_local(p.abierta_ms, r.huso_corte) == dia
        )
        if hoy >= r.posiciones_dia_max:
            return "posiciones_dia_max"
        return None

    # --------------------------------------------------------------------------- la cuenta

    def _precio(self, puntos: int) -> Decimal:
        return Decimal(puntos) / self.escala

    def _operacion(self, p: Posicion) -> Operacion:
        assert p.cerrada_ms is not None and p.precio_cierre is not None
        cargos: list[Cargo] = []
        comision = self.reglas.comision_por_lote * p.lotes
        if self.reglas.comision_por_lado:
            cargos.append(Cargo(_instante(p.abierta_ms), comision, "comision"))
            cargos.append(Cargo(_instante(p.cerrada_ms), comision, "comision"))
        else:
            cargos.append(Cargo(_instante(p.abierta_ms), comision, "comision"))
        for instante, importe in p.swaps:
            if instante <= p.cerrada_ms:
                cargos.append(Cargo(_instante(instante), importe, "swap"))
        marcas = tuple(
            Marca(_instante(ms), self._precio(precio))
            for ms, precio in p.marcas
            if p.abierta_ms <= ms <= p.cerrada_ms
        )
        return Operacion(
            id=p.id,
            direccion=p.lado,
            lotes=p.lotes,
            apertura=Marca(_instante(p.abierta_ms), self._precio(p.entrada)),
            cierre=Marca(_instante(p.cerrada_ms), self._precio(p.precio_cierre)),
            cargos=tuple(cargos),
            marcas=marcas,
        )

    def operaciones_cerradas(self) -> tuple[Operacion, ...]:
        """Lo que la capa de cuenta (ADR-0050) recibe: una por posicion cerrada, en orden."""
        return tuple(sorted(self._cerradas, key=lambda o: (o.apertura.instante, o.id)))

    def traza(self) -> Traza:
        return Traza(tuple(self._eventos), tuple(self._rechazos))


def contrato_desde(escala: int, contrato: Decimal) -> tuple[Decimal, int]:
    """El par (contrato, escala) que el broker y la cuenta comparten: P/L = delta puntos / escala
    * lotes * contrato. La cuenta recibe precios en moneda (`Marca.precio`) y el mismo contrato."""
    return contrato, escala


__all__ = [
    "CANCELADA",
    "COLOCADA",
    "EXPIRADA",
    "HECHO_OPERACION_ABIERTA",
    "HECHO_ORDEN_PENDIENTE",
    "LLENADA",
    "MANUAL",
    "MODIFICADA",
    "RECHAZADA",
    "Broker",
    "BrokerError",
    "Orden",
    "Posicion",
    "Rechazo",
    "ReglasBroker",
    "Traza",
    "contrato_desde",
]
