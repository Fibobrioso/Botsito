"""El broker simulado (ADR-0052, PROPUESTO): ordenes, posiciones y lo que la cuenta recibe.

Estado puro sobre un `Mercado` (ticks donde los hay, M1 de respaldo donde no) y el modelo de
llenado de ADR-0051. Sin IO, sin reloj de pared, sin cifras de negocio: los limites de la firma
vienen de `ReglasBroker` (leidas del perfil de cuenta por quien llama) y lo elegible del llenado
de `Configuracion`. Nada aqui asume un instrumento ni una firma.

CICLO DE VIDA de una orden pendiente, LIMITE o STOP (ADR-0056 §2, ADR-0057): colocada ->
(modificada)* -> llenada | cancelada | expirada; o rechazada al colocarla, y el rechazo queda
registrado con su motivo: un limite del perfil (volumen maximo, ordenes simultaneas, posiciones por
dia), el PRECIO INVALIDO de una pendiente del lado equivocado del precio (una limite de venta por
debajo del bid, una stop de venta por encima; y al reves en compra), o el STOPS LEVEL, cuando se
conoce. Una pendiente del lado equivocado NUNCA se llena a su propio precio: se rechaza, como haria
MT5 (PROVISIONAL hasta la demo de FTMO). Una orden STOP no se coloca sin stops level: el del perfil
(`firma_stops_level_puntos`, UNKNOWN hasta medirlo, A-27) o uno hipotetico en diagnostico.

PETICIONES AL SERVIDOR (R13 de FTMO-REGLAS.md, `firma_mensajes_dia_max`; rama
`feature/contador-peticiones`): el broker apunta cada peticion que recibe -colocar, modificar
(una pendiente o el stop de una posicion), cancelar y cerrar a mercado-, ACEPTADA O RECHAZADA, que
es la lectura mas estricta de «server requests» hasta que FTMO diga otra cosa. Lo que el servidor
hace solo -llenar, expirar, saltar el stop o el objetivo- no es una peticion, y tampoco
`abrir_conocida`, que repite una operacion del trader y no la emite el bot. Una peticion que el
broker no admite (`BrokerError`) no se apunta: es un error de quien llama y la corrida se para.
Desde `feature/freno-peticiones` (ADR-0067) cada peticion pasa antes por el FRENO
(`engine/freno.py`): con el corte del dia o un bucle, lo que no protege la cuenta se niega -no
llega al servidor, no se cuenta y queda en `Traza.cortes`-; cancelar, cerrar a mercado y mover el
stop de una posicion hacia el break even salen siempre, y cuentan. Sin umbrales del registro el
broker frena igual en `mensajes_dia_max`, el limite de la firma.

CIERRES DE MERCADO (R15 de FTMO-REGLAS.md; rama `feature/cierres-de-mercado`, ADR-0068): antes
que el freno, colocar y modificar una pendiente preguntan al PREDICADO UNICO
`domain.cierres.ventana_prohibida_por_cierre`. Desde dos horas antes de un cierre largo hasta que
acaba, y fuera de lo que cubre el calendario, se niegan: un `Rechazo` con su motivo, que no llega
al servidor ni se cuenta. Una pendiente ya puesta se CANCELA al empezar la ventana si
`ReglasCierres.cancelar_pendientes` (PROVISIONAL bajo A-55), antes que un llenado de ese instante;
la cancelacion protege la cuenta y cuenta. Una posicion abierta no se toca (R7). Todo va a
`Traza.cierres` y al log.

Una orden llenada abre una POSICION con stop y objetivo, que se cierra por stop, por objetivo o a
mercado (cierre manual); si era una stop, la posicion guarda el deslizamiento de la entrada. Cada
cierre produce una `cuenta.Operacion` con sus cargos -comision por lado si el perfil lo dice,
swap por cada corte diario del perfil que la posicion cruce- y sus MARCAS: el peor precio de cada
minuto vivo, que es lo que la capa de cuenta vigila (ADR-0050). La equity de la cuenta en
cualquier marca es el saldo mas el flotante de las posiciones del broker: un test lo comprueba.

NO se cablea al motor de reglas (ADR-0052 §5): el motor sigue sin tocarse. Este broker expone el
contrato que el motor tendra que cumplir -colocar, modificar, cancelar, cerrar a mercado, y leer
los hechos de origen broker `operacion_abierta` y `orden_limite_pendiente`- y `avanzar(hasta)`,
que procesa los eventos en orden de instante SIN MIRAR AL FUTURO: cada evento sale del primer
instante en que su condicion se cumple y nada posterior lo cambia.
"""

from __future__ import annotations

import logging
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal
from zoneinfo import ZoneInfo

from botsito.domain.cierres import (
    ReglasCierres,
    proxima_prohibicion,
    ventana_prohibida_por_cierre,
)
from botsito.domain.ticks import MS_POR_MINUTO
from botsito.domain.velas import MinutoUtc
from botsito.engine.cuenta import Cargo, Marca, Operacion
from botsito.engine.freno import Corte, FrenoPeticiones, LimitesFreno
from botsito.engine.llenado import (
    RESPALDO_M1,
    TICKS,
    TIPO_LIMITE,
    TIPO_STOP,
    TIPOS_ORDEN,
    Configuracion,
    Evento,
    Lado,
    Mercado,
    lado_equivocado,
    primer_llenado_limite,
    primer_llenado_stop,
    primer_toque_al_tick,
    primera_salida,
)

COLOCADA = "colocada"
MODIFICADA = "modificada"
LLENADA = "llenada"
CANCELADA = "cancelada"
EXPIRADA = "expirada"
RECHAZADA = "rechazada"
MANUAL = "manual"
# el stop de una posicion cambia (RN-014): AL TICK que pasa el nivel vigilado (fuente `ticks`), o
# en el cierre de la M1 cuando lo pide el motor (fuente `cierre_m1`, o `respaldo_m1` si ese minuto
# no tiene ticks), ADR-0065. No es un cierre: la posicion sigue viva
STOP_MOVIDO = "stop_movido"
CIERRE_M1 = "cierre_m1"
HECHO_OPERACION_ABIERTA = "operacion_abierta"
HECHO_ORDEN_PENDIENTE = "orden_limite_pendiente"
MOTIVO_PRECIO_INVALIDO = "precio_invalido"
MOTIVO_STOPS_LEVEL = "stops_level"
PARAMETRO_STOPS_LEVEL = "firma_stops_level_puntos"
PETICION_COLOCAR = "colocar"
PETICION_MODIFICAR = "modificar"
PETICION_CANCELAR = "cancelar"
PETICION_CERRAR = "cerrar"
TIPOS_PETICION = (PETICION_COLOCAR, PETICION_MODIFICAR, PETICION_CANCELAR, PETICION_CERRAR)
_EPOCA = datetime(1970, 1, 1, tzinfo=UTC)
LOG = logging.getLogger(__name__)


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
    # la distancia minima al precio que admite el broker (A-27): None mientras sea UNKNOWN
    stops_level_puntos: int | None = None
    # peticiones al servidor por dia de la firma (R13): el limite de la firma, y el freno de
    # ultimo recurso si no llegan umbrales del registro (ADR-0067)
    mensajes_dia_max: int | None = None
    # los umbrales del freno, leidos del registro (ADR-0067); None: el freno corta en
    # `mensajes_dia_max`
    freno: LimitesFreno | None = None
    # la ventana prohibida antes de un cierre de mercado largo (ADR-0068): None, sin calendario
    cierres: ReglasCierres | None = None


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
    tipo: str = TIPO_LIMITE  # TIPO_LIMITE o TIPO_STOP


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
    stop_original: int | None = None  # el stop con el que nacio, si se movio despues
    stop_movido_ms: int | None = None  # el ultimo cambio de stop: el nuevo cuenta DESPUES
    # el break even vigilado al tick (ADR-0065): el nivel que el BID tiene que pasar y desde cuando
    break_even_nivel: int | None = None
    break_even_desde_ms: int = 0
    marcas: list[tuple[int, int]] = field(default_factory=list)  # (instante_ms, peor precio)
    swaps: list[tuple[int, Decimal]] = field(default_factory=list)
    # puntos EN CONTRA entre el precio de la orden y el llenado: 0 en una limite; en una stop, el
    # hueco y el deslizamiento de la configuracion (ADR-0057)
    deslizamiento_entrada: int = 0

    @property
    def abierta(self) -> bool:
        return self.cerrada_ms is None


@dataclass(frozen=True)
class Rechazo:
    instante_ms: int
    orden_id: str
    motivo: str


@dataclass(frozen=True)
class Peticion:
    """Una peticion al servidor (R13): su tipo, la orden o posicion y si se acepto."""

    instante_ms: int
    tipo: str  # uno de TIPOS_PETICION
    id: str
    aceptada: bool


@dataclass(frozen=True)
class Traza:
    """Lo que el broker hizo, para el informe: eventos con su fuente, rechazos y peticiones."""

    eventos: tuple[tuple[int, str, str, str], ...]  # (instante_ms, tipo, id, fuente)
    rechazos: tuple[Rechazo, ...]
    peticiones: tuple[Peticion, ...] = ()
    cortes: tuple[Corte, ...] = ()  # el aviso del dia y lo que el freno nego (ADR-0067)
    cierres: tuple[Corte, ...] = ()  # lo negado o cancelado por un cierre de mercado (ADR-0068)

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


def peticiones_por_dia(
    peticiones: Iterable[Peticion], huso_corte: ZoneInfo
) -> dict[date, dict[str, int]]:
    """Las peticiones agrupadas por el dia de la firma -el que corta a medianoche en `huso_corte`,
    como el dia de riesgo (ADR-0027)-: por dia, cuantas de cada tipo, `total` y `rechazadas`."""
    salida: dict[date, dict[str, int]] = {}
    for p in peticiones:
        dia = salida.setdefault(
            _dia_local(p.instante_ms, huso_corte),
            {**dict.fromkeys(TIPOS_PETICION, 0), "total": 0, "rechazadas": 0},
        )
        dia[p.tipo] += 1
        dia["total"] += 1
        dia["rechazadas"] += not p.aceptada
    return dict(sorted(salida.items()))


class Broker:
    """El broker de UNA cuenta sobre UN mercado. Determinista: todo se ordena por instante e id."""

    def __init__(
        self,
        reglas: ReglasBroker,
        config: Configuracion,
        mercado: Mercado,
        contrato: Decimal,
        escala: int,
        stops_level_diagnostico: int | None = None,
    ) -> None:
        if contrato <= 0 or escala <= 0:
            raise BrokerError("contrato y escala son positivos")
        if stops_level_diagnostico is not None:
            if reglas.stops_level_puntos is not None:
                raise BrokerError(
                    f"{PARAMETRO_STOPS_LEVEL} ya esta fijado en {reglas.stops_level_puntos} (A-27 "
                    "medida): la corrida cuenta y no admite un stops level en diagnostico"
                )
            if stops_level_diagnostico < 0:
                raise BrokerError("un stops level en diagnostico no es negativo")
        # el stops level con el que opera: el del perfil o, sin el, el del diagnostico (ADR-0057)
        self.stops_level: int | None = (
            reglas.stops_level_puntos
            if reglas.stops_level_puntos is not None
            else stops_level_diagnostico
        )
        self.reglas = reglas
        self.config = config
        self.mercado = mercado
        self.contrato = contrato
        self.escala = escala
        self.ordenes: dict[str, Orden] = {}
        self.posiciones: dict[str, Posicion] = {}
        self._rechazos: list[Rechazo] = []
        self._peticiones: list[Peticion] = []
        self._eventos: list[tuple[int, str, str, str]] = []
        self._cerradas: list[Operacion] = []
        self._cierres: list[Corte] = []
        self.ahora_ms: int = 0
        # el freno (ADR-0067): los umbrales del registro, o el limite de la firma sin ellos
        limites = reglas.freno
        if limites is None and reglas.mensajes_dia_max is not None:
            limites = LimitesFreno(corte=reglas.mensajes_dia_max)
        if (
            limites is not None
            and reglas.mensajes_dia_max is not None
            and limites.corte > reglas.mensajes_dia_max
        ):
            raise BrokerError(
                f"el corte del freno ({limites.corte}) pasa del limite de la firma "
                f"({reglas.mensajes_dia_max}): tiene que ir por debajo, con margen"
            )
        self.freno: FrenoPeticiones | None = (
            FrenoPeticiones(limites) if limites is not None else None
        )

    def _admitir(
        self, instante_ms: int, tipo: str, id: str, firma: object, protege: bool
    ) -> str | None:
        """Pregunta al freno ANTES de enviar: None si sale, o el motivo por el que se niega."""
        if self.freno is None:
            return None
        dia = _dia_local(instante_ms, self.reglas.huso_corte)
        return self.freno.admitir(dia, instante_ms, tipo, id, firma, protege)

    def _prohibido_por_cierre(self, instante_ms: int, tipo: str, id: str) -> str | None:
        """Pregunta al predicado de los cierres (ADR-0068): None si se puede, o el motivo; lo
        negado queda en `Traza.cierres` y en el log."""
        c = self.reglas.cierres
        if c is None:
            return None
        p = ventana_prohibida_por_cierre(instante_ms, c.calendario, c.margen_ms, c.minimo_ms)
        if p is None:
            return None
        self._cierres.append(Corte(instante_ms, tipo, id, p.motivo))
        LOG.info(
            "cierre de mercado: negada %s %s en el instante %d (%s%s)",
            tipo, id, instante_ms, p.motivo,
            f", cierre desde {p.cierre.inicio_ms} ({p.cierre.fuente})" if p.cierre else "",
        )  # fmt: skip
        return p.motivo

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
        """Coloca una LIMITE. Un limite del perfil o un precio invalido la RECHAZA y lo registra,
        no la encola."""
        return self._colocar(
            TIPO_LIMITE, id, lado, precio, lotes, stop, objetivo, instante_ms, expira_ms
        )

    def colocar_stop(
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
        """Coloca una STOP de entrada (ADR-0056 §2): una venta stop por debajo del bid, una compra
        stop por encima del ask, que saltan al tocar su nivel. Sin stops level, se niega."""
        return self._colocar(
            TIPO_STOP, id, lado, precio, lotes, stop, objetivo, instante_ms, expira_ms
        )

    def _colocar(
        self,
        tipo: str,
        id: str,
        lado: Lado,
        precio: int,
        lotes: Decimal,
        stop: int,
        objetivo: int,
        instante_ms: int,
        expira_ms: int | None,
    ) -> Orden | Rechazo:
        self._avanza_reloj(instante_ms)
        if tipo not in TIPOS_ORDEN:
            raise BrokerError(f"{id}: tipo de orden {tipo!r} desconocido")
        if id in self.ordenes:
            raise BrokerError(f"orden {id!r} repetida")
        if lotes <= 0:
            raise BrokerError(f"{id}: lotes no positivos")
        if lado == "compra" and not stop < precio < objetivo:
            raise BrokerError(f"{id}: una compra lleva stop < precio < objetivo")
        if lado == "venta" and not objetivo < precio < stop:
            raise BrokerError(f"{id}: una venta lleva objetivo < precio < stop")
        if tipo == TIPO_STOP and self.stops_level is None:
            raise BrokerError(
                f"{id}: una orden stop no se coloca sin stops level: {PARAMETRO_STOPS_LEVEL} es "
                "UNKNOWN en el perfil de cuenta hasta medirlo en la demo de la firma (A-27). Para "
                "correr en hipotesis, --diagnostico-a27 <puntos>: ETIQUETADO y sin valor para "
                "ninguna medida (ADR-0057)"
            )
        # el cierre de mercado y despues el freno, antes que el servidor: una orden negada no se
        # envia, no se cuenta y no existe (ADR-0068, ADR-0067)
        cerrado = self._prohibido_por_cierre(instante_ms, PETICION_COLOCAR, id)
        if cerrado is not None:
            return Rechazo(instante_ms, id, cerrado)
        firma = (PETICION_COLOCAR, tipo, lado, precio, stop, objetivo, lotes)
        negada = self._admitir(instante_ms, PETICION_COLOCAR, id, firma, protege=False)
        if negada is not None:
            return Rechazo(instante_ms, id, negada)
        motivo = self._limite_infringido(lotes, instante_ms)
        if motivo is None:
            motivo = self._precio_infringido(tipo, lado, precio, stop, objetivo, instante_ms)
        if motivo is not None:
            r = Rechazo(instante_ms, id, motivo)
            self._rechazos.append(r)
            self._peticiones.append(Peticion(instante_ms, PETICION_COLOCAR, id, False))
            self.ordenes[id] = Orden(
                id, lado, precio, lotes, stop, objetivo, instante_ms, expira_ms, RECHAZADA,
                instante_ms, [(instante_ms, RECHAZADA)], tipo,
            )  # fmt: skip
            return r
        orden = Orden(
            id, lado, precio, lotes, stop, objetivo, instante_ms, expira_ms, COLOCADA, instante_ms,
            [(instante_ms, COLOCADA)], tipo,
        )  # fmt: skip
        self.ordenes[id] = orden
        self._peticiones.append(Peticion(instante_ms, PETICION_COLOCAR, id, True))
        return orden

    def _precio_infringido(
        self, tipo: str, lado: Lado, precio: int, stop: int, objetivo: int, instante_ms: int
    ) -> str | None:
        """El motivo de rechazo por precio (ADR-0057, PROVISIONAL hasta la demo de FTMO), o None.
        Con la cotizacion del momento: una pendiente del lado equivocado es PRECIO INVALIDO; y, si
        el stops level es conocido, una pendiente o su stop u objetivo mas cerca de el que ese
        minimo es STOPS LEVEL. Sin cotizacion (antes del primer precio del mercado) no se juzga."""
        q = self.mercado.cotizacion(instante_ms, self.config.spread_supuesto)
        if q is None:
            return None
        bid, ask, _ = q
        if lado_equivocado(tipo, lado, precio, bid, ask):
            return MOTIVO_PRECIO_INVALIDO
        minimo = self.stops_level
        if minimo:
            referencia = ask if lado == "compra" else bid
            if min(abs(precio - referencia), abs(precio - stop), abs(precio - objetivo)) < minimo:
                return MOTIVO_STOPS_LEVEL
        return None

    def modificar(
        self,
        id: str,
        instante_ms: int,
        precio: int | None = None,
        stop: int | None = None,
        objetivo: int | None = None,
    ) -> Orden | Rechazo:
        """Modifica una pendiente. Si la modificacion la deja con un precio invalido (ADR-0057),
        se RECHAZA, se registra y la orden sigue como estaba, como en MT5."""
        self._avanza_reloj(instante_ms)
        orden = self._pendiente(id)
        nuevo_precio = precio if precio is not None else orden.precio
        nuevo_stop = stop if stop is not None else orden.stop
        nuevo_objetivo = objetivo if objetivo is not None else orden.objetivo
        cerrado = self._prohibido_por_cierre(instante_ms, PETICION_MODIFICAR, id)
        if cerrado is not None:
            return Rechazo(instante_ms, id, cerrado)  # la orden sigue como estaba (ADR-0068)
        firma = (PETICION_MODIFICAR, id, nuevo_precio, nuevo_stop, nuevo_objetivo)
        negada = self._admitir(instante_ms, PETICION_MODIFICAR, id, firma, protege=False)
        if negada is not None:
            return Rechazo(instante_ms, id, negada)  # la orden sigue como estaba
        motivo = self._precio_infringido(
            orden.tipo, orden.lado, nuevo_precio, nuevo_stop, nuevo_objetivo, instante_ms
        )
        if motivo is not None:
            r = Rechazo(instante_ms, id, motivo)
            self._rechazos.append(r)
            self._peticiones.append(Peticion(instante_ms, PETICION_MODIFICAR, id, False))
            return r
        self._peticiones.append(Peticion(instante_ms, PETICION_MODIFICAR, id, True))
        orden.precio = nuevo_precio
        orden.stop = nuevo_stop
        orden.objetivo = nuevo_objetivo
        orden.estado = MODIFICADA
        orden.ultimo_cambio_ms = instante_ms
        orden.historial.append((instante_ms, MODIFICADA))
        return orden

    def cancelar(self, id: str, instante_ms: int) -> Orden:
        self._avanza_reloj(instante_ms)
        orden = self._pendiente(id)
        # protege la cuenta: sale siempre, y cuenta (ADR-0067)
        self._admitir(instante_ms, PETICION_CANCELAR, id, None, protege=True)
        self._peticiones.append(Peticion(instante_ms, PETICION_CANCELAR, id, True))
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
        # protege la cuenta: sale siempre, y cuenta (ADR-0067)
        self._admitir(instante_ms, PETICION_CERRAR, posicion_id, None, protege=True)
        self._peticiones.append(Peticion(instante_ms, PETICION_CERRAR, posicion_id, True))
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

    def mover_stop(self, posicion_id: str, stop: int, instante_ms: int) -> Posicion:
        """Cambia el stop de una posicion viva (RN-014, ADR-0053 §1); el objetivo no se toca. La
        posicion guarda el stop original para clasificar el cierre (break even o salto el stop).

        Si el stop YA esta ahi -el break even se movio al tick antes del cierre de la M1 que el
        motor mira (ADR-0065)- no hace nada: ni peticion ni evento. Si no, es una peticion
        `modificar` y queda en la traza como `stop_movido`, con la fuente del minuto: `cierre_m1`
        con ticks, `respaldo_m1` sin ellos."""
        self._avanza_reloj(instante_ms)
        p = self.posiciones.get(posicion_id)
        if p is None or not p.abierta:
            raise BrokerError(f"posicion {posicion_id!r} no esta abierta")
        if p.stop == stop:
            return p
        if p.lado == "compra" and not stop < p.objetivo:
            raise BrokerError(f"{posicion_id}: el stop de una larga va por debajo del objetivo")
        if p.lado == "venta" and not stop > p.objetivo:
            raise BrokerError(f"{posicion_id}: el stop de una corta va por encima del objetivo")
        fuente = (
            CIERRE_M1
            if self.mercado.ticks_del_minuto(instante_ms // MS_POR_MINUTO) is not None
            else RESPALDO_M1
        )
        self._mover(p, stop, instante_ms, fuente)  # si el freno lo niega, la posicion sigue igual
        return p

    def vigilar_break_even(self, posicion_id: str, nivel: int, instante_ms: int) -> None:
        """El break even de RN-014 AL TICK (ADR-0065): desde `instante_ms`, el primer tick cuyo BID
        pase `nivel` a favor de la posicion pone su stop en la entrada exacta. Vigilar no es una
        peticion -lo hace el bot en local, mirando el precio-; mover el stop si lo es. Solo una
        posicion viva con su stop sin mover; un nivel nuevo sustituye al anterior."""
        self._avanza_reloj(instante_ms)
        p = self.posiciones.get(posicion_id)
        if p is None or not p.abierta or p.stop_original is not None:
            return
        p.break_even_nivel = nivel
        p.break_even_desde_ms = instante_ms

    def _mover(self, p: Posicion, stop: int, instante_ms: int, fuente: str) -> bool:
        """Mueve el stop de una posicion viva, si el freno lo deja (ADR-0067). PROTEGE -sale
        siempre- solo el PRIMER movimiento hacia el lado que reduce el riesgo, que es el break even
        de RN-014: asi lo que protege queda acotado (una vez por posicion) y un bucle que suba el
        stop punto a punto no se cuela por ahi. Los demas se frenan como lo que no protege. Nunca
        deja la posicion sin stop: si se niega, conserva el que tenia."""
        hacia_dentro = stop > p.stop if p.lado == "compra" else stop < p.stop
        protege = hacia_dentro and p.stop_original is None
        negada = self._admitir(
            instante_ms, PETICION_MODIFICAR, p.id, (PETICION_MODIFICAR, p.id, stop), protege
        )
        if negada is not None:
            return False
        self._peticiones.append(Peticion(instante_ms, PETICION_MODIFICAR, p.id, True))
        if p.stop_original is None:
            p.stop_original = p.stop
        p.stop = stop
        p.stop_movido_ms = instante_ms
        p.break_even_nivel = None
        self._eventos.append((instante_ms, STOP_MOVIDO, p.id, fuente))
        return True

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
        ventana = self._proxima_ventana(hasta_ms)
        for o in sorted(self.ordenes.values(), key=lambda x: x.id):
            if o.estado not in (COLOCADA, MODIFICADA):
                continue
            if ventana is not None:
                candidatos.append((ventana, o.id, CANCELADA, o.id, None))
            tope = hasta_ms if o.expira_ms is None else min(hasta_ms, o.expira_ms)
            # el tick en el que se coloco o modifico no cuenta (exclusivo); el tick del ultimo
            # evento procesado SI puede llenar otra orden pendiente (por eso ahora - 1)
            llenado = primer_llenado_stop if o.tipo == TIPO_STOP else primer_llenado_limite
            ev = llenado(
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
            # el stop movido cuenta desde el tick SIGUIENTE al que lo movio (ADR-0065 §3), como
            # cualquier evento del modelo: nunca contra el tick en el que se decidio
            desde = max(self.ahora_ms - 1, p.abierta_ms, p.stop_movido_ms or 0)
            ev = primera_salida(
                p.lado, p.stop, p.objetivo, desde, hasta_ms, self.mercado, self.config
            )
            if ev is not None:
                candidatos.append((ev.instante_ms, p.id, ev.tipo, p.id, ev))
            if p.break_even_nivel is not None:
                toque = primer_toque_al_tick(
                    p.lado,
                    p.break_even_nivel,
                    max(self.ahora_ms - 1, p.break_even_desde_ms),
                    hasta_ms,
                    self.mercado,
                )
                if toque is not None:
                    candidatos.append((toque.instante_ms, p.id, STOP_MOVIDO, p.id, toque))
        if not candidatos:
            return None
        # en el mismo instante, primero la cancelacion por un cierre (ADR-0068: que no se llene
        # dentro de la ventana), despues lo que el servidor hace con lo que YA hay (llenar, saltar
        # el stop vigente o el objetivo) y al final mover el stop (ADR-0065 §3)
        return min(
            candidatos, key=lambda c: (c[0], c[2] != CANCELADA, c[2] == STOP_MOVIDO, c[2], c[1])
        )

    def _proxima_ventana(self, hasta_ms: int) -> int | None:
        """El inicio de la proxima ventana prohibida en (ahora, hasta], si hay pendientes que
        cancelar en ella (ADR-0068, `cancelar_pendientes`)."""
        c = self.reglas.cierres
        if c is None or not c.cancelar_pendientes:
            return None
        return proxima_prohibicion(self.ahora_ms, hasta_ms, c.calendario, c.margen_ms, c.minimo_ms)

    def _aplicar(self, tipo: str, objeto: str, evento: Evento | None, instante: int) -> None:
        self._marcar_hasta(instante)
        self.ahora_ms = instante
        if tipo == CANCELADA:
            self._cancelar_por_cierre(self.ordenes[objeto], instante)
            return
        if tipo == EXPIRADA:
            o = self.ordenes[objeto]
            o.estado = EXPIRADA
            o.ultimo_cambio_ms = instante
            o.historial.append((instante, EXPIRADA))
            self._eventos.append((instante, EXPIRADA, o.id, TICKS))
            return
        assert evento is not None
        if tipo == STOP_MOVIDO:
            p = self.posiciones[objeto]
            self._mover(p, p.entrada, instante, TICKS)
            return
        if tipo == LLENADA:
            o = self.ordenes[objeto]
            o.estado = LLENADA
            o.ultimo_cambio_ms = instante
            o.historial.append((instante, LLENADA))
            contra = evento.precio - o.precio if o.lado == "compra" else o.precio - evento.precio
            p = Posicion(
                f"pos-{o.id}", o.id, o.lado, o.lotes, evento.precio, o.stop, o.objetivo, instante,
                evento.fuente, ultimo_precio=evento.precio, deslizamiento_entrada=contra,
            )  # fmt: skip
            self.posiciones[p.id] = p
            self._eventos.append((instante, LLENADA, o.id, evento.fuente))
            return
        p = self.posiciones[objeto]
        self._cerrar(p, instante, evento.precio, evento.tipo, evento.fuente)

    def _cancelar_por_cierre(self, o: Orden, instante: int) -> None:
        """Al empezar una ventana prohibida, la pendiente se cancela (ADR-0068): lo que protege la
        cuenta, que sale siempre y cuenta (ADR-0067 §3). El motivo lo dice el mismo predicado."""
        c = self.reglas.cierres
        assert c is not None
        p = ventana_prohibida_por_cierre(instante, c.calendario, c.margen_ms, c.minimo_ms)
        if p is None:  # el predicado manda: si no prohibe, la orden sigue
            return
        self._admitir(instante, PETICION_CANCELAR, o.id, None, protege=True)
        self._peticiones.append(Peticion(instante, PETICION_CANCELAR, o.id, True))
        o.estado = CANCELADA
        o.ultimo_cambio_ms = instante
        o.historial.append((instante, CANCELADA))
        self._eventos.append((instante, CANCELADA, o.id, TICKS))
        self._cierres.append(Corte(instante, PETICION_CANCELAR, o.id, p.motivo))
        LOG.info(
            "cierre de mercado: cancelada la pendiente %s en el instante %d (%s)",
            o.id, instante, p.motivo,
        )  # fmt: skip

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
        cortes = tuple(self.freno.cortes) if self.freno is not None else ()
        return Traza(
            tuple(self._eventos),
            tuple(self._rechazos),
            tuple(self._peticiones),
            cortes,
            tuple(self._cierres),
        )


def contrato_desde(escala: int, contrato: Decimal) -> tuple[Decimal, int]:
    """El par (contrato, escala) que el broker y la cuenta comparten: P/L = delta puntos / escala
    * lotes * contrato. La cuenta recibe precios en moneda (`Marca.precio`) y el mismo contrato."""
    return contrato, escala


__all__ = [
    "CANCELADA",
    "CIERRE_M1",
    "COLOCADA",
    "EXPIRADA",
    "HECHO_OPERACION_ABIERTA",
    "HECHO_ORDEN_PENDIENTE",
    "LLENADA",
    "MANUAL",
    "MODIFICADA",
    "MOTIVO_PRECIO_INVALIDO",
    "MOTIVO_STOPS_LEVEL",
    "PARAMETRO_STOPS_LEVEL",
    "PETICION_CANCELAR",
    "PETICION_CERRAR",
    "PETICION_COLOCAR",
    "PETICION_MODIFICAR",
    "RECHAZADA",
    "STOP_MOVIDO",
    "TIPOS_PETICION",
    "Broker",
    "BrokerError",
    "Orden",
    "Peticion",
    "Posicion",
    "Rechazo",
    "ReglasBroker",
    "Traza",
    "contrato_desde",
    "peticiones_por_dia",
]
