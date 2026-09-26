"""El cableado del simulador (ADR-0053): dia -> motor de reglas -> ordenes -> broker -> llenado
con ticks -> capa de cuenta -> veredicto FTMO y operaciones del bot para el criterio de fidelidad.

`MotorCableado` cumple el protocolo `Motor` del arnes (ADR-0048) -`correr_dia(DiaDeMercado)`
devuelve un `ResultadoDia` con las operaciones del bot y las trazas por sesion-, asi que el arnes,
su informe y el visor lo usan sin cambios. Por dentro, cada minuto de la ventana pasa por las tres
fases de ADR-0028 en el orden de ADR-0053 §5: el broker avanza tick a tick hasta el ultimo
milisegundo anterior al cierre de M1 y la cuenta viva recibe sus eventos y marcas (riesgo por
tick); los eventos del broker quedan a disposicion de las primitivas y `EstadoDia.broker` se
actualiza (ordenes por evento); y el interprete corre el evento del cierre de M1 (estrategia).

UN SOLO RELOJ (§4): el del perfil, comprobado al arrancar contra `huso_operativa`. LA CUENTA
PERSISTE en toda la corrida; el estado de estrategia y el broker empiezan cada dia de cero (§6).
TICKS OBLIGATORIOS (§7): un dia sin dataset de ticks se rechaza salvo en modo depuracion, y
entonces toda la salida lo dice. SOLO CONSTRUCCION, por la compuerta del arnes (§8).
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, time
from decimal import Decimal
from typing import Any

from botsito.cases.criterio_fidelidad import Operacion as OperacionCriterio
from botsito.comun.husos import huso_canonico
from botsito.config.registro import Registro
from botsito.data.velas import a_datetime
from botsito.domain.ticks import MS_POR_MINUTO
from botsito.domain.velas import MinutoUtc
from botsito.engine.broker import LLENADA, MANUAL, Broker, ReglasBroker
from botsito.engine.cuenta import CuentaViva, EstadoCuenta, ReglasFase
from botsito.engine.interprete import EstadoDia, Interprete, Momento, ReglaEjecutable
from botsito.engine.llenado import OBJETIVO, RESPALDO_M1, STOP, TICKS, Configuracion
from botsito.engine.motor import DiaDeMercado, ResultadoDia, Sesion, TrazaSesion
from botsito.engine.primitivas_broker import (
    ContextoDia,
    EventoBroker,
    Zona,
    clasificar_cierre,
    primitivas_cableadas,
)
from botsito.engine.simulacion import MercadoDia

DEPURACION = "DEPURACION: respaldo M1, no cuenta"


class CableadoError(ValueError):
    """El cableado no puede correr asi: nunca se adivina."""


@dataclass
class TrazaBroker:
    """Lo que el broker y la cuenta hicieron en un dia, para el informe y el visor."""

    eventos: list[tuple[int, str, str, str]] = field(default_factory=list)  # ms, tipo, id, fuente
    rechazos: int = 0
    por_fuente: dict[str, int] = field(default_factory=lambda: {TICKS: 0, RESPALDO_M1: 0})
    huecos: set[str] = field(default_factory=set)
    equity_fin: Decimal = Decimal(0)
    saldo_fin: Decimal = Decimal(0)
    depuracion: bool = False


@dataclass
class MotorCableado:
    """El motor real cableado al broker y a la cuenta. `zonas_de` es la puerta para una estrategia
    sintetica en los tests (una funcion que produce zonas por minuto); en produccion no hay ninguna
    y la geometria sigue NO_IMPLEMENTADA."""

    vocabulario: Mapping[str, Mapping[str, Any]]
    reglas: Sequence[ReglaEjecutable]
    registro: Registro
    mercados: Mapping[str, MercadoDia]  # por dia AAAA-MM-DD
    reglas_broker: ReglasBroker
    reglas_fase: ReglasFase
    config_llenado: Configuracion
    contrato: Decimal
    depuracion: bool = False
    primitivas_extra: Mapping[str, Any] = field(default_factory=dict)  # sinteticas (tests)
    acumuladores_extra: Mapping[str, Any] = field(default_factory=dict)  # sinteticas (tests)
    zonas_de: Callable[[MercadoDia], Mapping[str, Zona]] | None = None  # sinteticas (tests)
    cuenta: CuentaViva | None = None
    trazas_broker: dict[str, TrazaBroker] = field(default_factory=dict)
    brokers: dict[str, Broker] = field(default_factory=dict)

    def __post_init__(self) -> None:
        comprobar_reloj_unico(self.registro, self.reglas_fase, self.mercados)

    def correr_dia(self, dia: DiaDeMercado) -> ResultadoDia:
        clave = dia.dia.isoformat()
        md = self.mercados.get(clave)
        if md is None:
            raise CableadoError(f"{clave}: sin mercado (ticks y M1) para ese dia")
        if not md.origen_ticks and not self.depuracion:
            raise CableadoError(
                f"{clave}: sin dataset de ticks; los ticks son obligatorios (ADR-0051 §8). Con "
                "--depuracion corre sobre el respaldo M1 y la salida lo dice"
            )
        huso = huso_canonico(dia.huso)
        limites = [
            (s.nombre, _minuto_local(dia.dia, s.desde, huso), _minuto_local(dia.dia, s.hasta, huso))
            for s in dia.sesiones
        ]
        primero = min(d for _, d, _ in limites)
        ultimo = max(h for _, _, h in limites)
        if self.cuenta is None:
            self.cuenta = CuentaViva(self.reglas_fase, self.contrato, primero * MS_POR_MINUTO - 1)
        broker = Broker(
            self.reglas_broker, self.config_llenado, md.mercado(), self.contrato, md.escala
        )
        ctx = ContextoDia(broker, self.cuenta, self.contrato, md.escala)
        if self.zonas_de is not None:
            ctx.zonas.update(self.zonas_de(md))
        primitivas = primitivas_cableadas(self.registro, ctx)
        if self.primitivas_extra or self.acumuladores_extra:
            predicados = dict(primitivas.predicados)
            predicados.update(self.primitivas_extra)
            acumuladores = dict(primitivas.acumuladores)
            acumuladores.update(self.acumuladores_extra)
            primitivas = type(primitivas)(predicados, primitivas.acciones, acumuladores)
        interprete = Interprete(self.vocabulario, primitivas)
        estado = EstadoDia()
        trazas = {nombre: TrazaSesion() for nombre, _, _ in limites}
        tb = TrazaBroker(depuracion=self.depuracion or not md.origen_ticks)
        vistos = 0
        instante = primero
        while instante <= ultimo:
            hasta_ms = instante * MS_POR_MINUTO - 1
            # 1. riesgo por tick: el broker hasta el ultimo milisegundo anterior al cierre
            nuevos = broker.avanzar(hasta_ms)
            vistos = self._a_la_cuenta(broker, ctx, tb, nuevos, vistos, hasta_ms)
            # 2. ordenes por evento del broker: hechos y eventos a la vista del interprete
            estado.broker = broker.hechos()
            ctx.acumuladores = self.cuenta.acumuladores()
            ctx.instante_ms = hasta_ms
            # 3. estrategia al cierre de M1
            sesion, abre = _sesion(limites, instante)
            momento = Momento(MinutoUtc(instante), sesion, abre, dia.datos)
            evento = interprete.evento(self.reglas, momento, estado)
            if sesion is not None:
                traza = trazas[sesion]
                traza.fijados += [(instante, r, h, v) for r, h, v in evento.fijados]
                traza.no_implementadas |= evento.no_implementadas
                traza.bloqueadas |= evento.bloqueadas
                traza.disparadas |= set(evento.disparadas)
                traza.empates |= set(evento.empates)
            ctx.eventos = []
            instante += 1
        # fin del dia: lo que quede vivo o pendiente se cierra y se cuenta (§6)
        fin_ms = ultimo * MS_POR_MINUTO - 1
        for p in list(broker.posiciones.values()):
            if p.abierta:
                broker.cerrar_a_mercado(p.id, fin_ms)
        for o in list(broker.ordenes.values()):
            if o.estado in ("colocada", "modificada"):
                broker.cancelar(o.id, fin_ms)
        nuevos = broker.avanzar(fin_ms)
        self._a_la_cuenta(broker, ctx, tb, nuevos, vistos, fin_ms)
        tb.huecos |= ctx.huecos
        tb.rechazos = len(broker.traza().rechazos)
        tb.equity_fin = self.cuenta.equity
        tb.saldo_fin = self.cuenta.saldo
        for nombre, traza in trazas.items():
            traza.anotaciones.update(estado.anotaciones.get(nombre, {}))
        self.trazas_broker[clave] = tb
        self.brokers[clave] = broker
        return ResultadoDia(clave, self._operaciones_del_bot(broker, md, dia, limites), trazas)

    def _a_la_cuenta(
        self,
        broker: Broker,
        ctx: ContextoDia,
        tb: TrazaBroker,
        nuevos: Sequence[tuple[int, str, str, str]],
        vistos: int,
        hasta_ms: int,
    ) -> int:
        """Los eventos del broker desde `vistos` pasan a la cuenta viva, a la traza y al
        contexto."""
        assert self.cuenta is not None
        cuenta = self.cuenta
        eventos = broker.traza().eventos
        for ms, tipo, id, fuente in eventos[vistos:]:
            tb.eventos.append((ms, tipo, id, fuente))
            tb.por_fuente[fuente] = tb.por_fuente.get(fuente, 0) + 1
            if tipo == LLENADA:
                p = (
                    broker.posiciones[f"pos-{id}"]
                    if f"pos-{id}" in broker.posiciones
                    else broker.posiciones[id]
                )
                cuenta.abrir(p.id, p.lado, p.lotes, _precio(p.entrada, broker.escala), ms)
                comision = self.reglas_broker.comision_por_lote * p.lotes
                cuenta.cargar(comision, ms)
                ctx.eventos.append(EventoBroker(ms, LLENADA, id, ctx.por_de_orden.get(id)))
            elif tipo in (STOP, OBJETIVO, MANUAL):
                p = broker.posiciones[id]
                assert p.precio_cierre is not None
                if self.reglas_broker.comision_por_lado:
                    cuenta.cargar(self.reglas_broker.comision_por_lote * p.lotes, ms)
                for instante_swap, importe in p.swaps:
                    if instante_swap <= ms:
                        cuenta.cargar(importe, instante_swap)
                cuenta.cerrar(p.id, _precio(p.precio_cierre, broker.escala), ms)
                signo = 1 if p.lado == "compra" else -1
                bruto = Decimal(signo * (p.precio_cierre - p.entrada))
                resultado = clasificar_cierre(tipo, p.stop_original is not None, bruto)
                ctx.eventos.append(
                    EventoBroker(ms, tipo, id, ctx.por_de_orden.get(p.orden_id), resultado)
                )
            else:
                ctx.eventos.append(EventoBroker(ms, tipo, id))
        vistos = len(eventos)
        # la peor marca del minuto de cada posicion viva
        for p in broker.posiciones.values():
            if p.abierta and p.marcas and p.marcas[-1][0] <= hasta_ms:
                cuenta.marcar(p.id, _precio(p.marcas[-1][1], broker.escala), p.marcas[-1][0])
        cuenta.avanzar(hasta_ms)
        return vistos

    def _operaciones_del_bot(
        self,
        broker: Broker,
        md: MercadoDia,
        dia: DiaDeMercado,
        limites: Sequence[tuple[str, int, int]],
    ) -> tuple[OperacionCriterio, ...]:
        """Las posiciones abiertas del dia en el formato del criterio (ADR-0043, ADR-0048 §4)."""
        salida: list[OperacionCriterio] = []
        for p in sorted(broker.posiciones.values(), key=lambda x: x.abierta_ms):
            minuto = p.abierta_ms // MS_POR_MINUTO
            sesion = next((n for n, d, h in limites if d <= minuto < h), None)
            if sesion is None:
                continue
            salida.append(
                OperacionCriterio(
                    dia.dia.isoformat(),
                    sesion,
                    p.lado,
                    datetime.fromtimestamp(p.abierta_ms / 1000, UTC),
                    _precio(p.entrada, broker.escala),
                )
            )
        return tuple(salida)

    def veredicto(self) -> tuple[EstadoCuenta, str, datetime | None]:
        if self.cuenta is None:
            return EstadoCuenta.EN_CURSO, "sin dias corridos", None
        return self.cuenta.estado, self.cuenta.motivo, self.cuenta.instante


def comprobar_reloj_unico(
    registro: Registro, reglas_fase: ReglasFase, mercados: Mapping[str, MercadoDia]
) -> None:
    """ADR-0053 §4: el reloj del perfil y `huso_operativa` tienen que dar la misma medianoche en
    cada dia de la corrida; si no, el cableado se niega."""
    operativa = huso_canonico(registro.texto("huso_operativa"))
    for clave in sorted(mercados):
        d = date.fromisoformat(clave)
        a = datetime.combine(d, time(0), tzinfo=reglas_fase.huso_corte).astimezone(UTC)
        b = datetime.combine(d, time(0), tzinfo=operativa).astimezone(UTC)
        if a != b:
            raise CableadoError(
                f"{clave}: el reloj del perfil ({reglas_fase.huso_corte.key}) y huso_operativa "
                f"({operativa.key}) no dan la misma medianoche: no hay un solo reloj"
            )


def _precio(puntos: int, escala: int) -> Decimal:
    return Decimal(puntos) / escala


def _minuto_local(dia: date, hhmm: str, huso: Any) -> int:
    hh, mm = (int(x) for x in hhmm.split(":"))
    local = datetime(dia.year, dia.month, dia.day, hh, mm, tzinfo=huso)
    return int((local.astimezone(UTC) - datetime(1970, 1, 1, tzinfo=UTC)).total_seconds() // 60)


def _sesion(limites: Sequence[tuple[str, int, int]], instante: int) -> tuple[str | None, bool]:
    for nombre, desde, hasta in limites:
        if desde <= instante < hasta:
            return nombre, instante == desde
    for nombre, _, hasta in limites:
        if instante == hasta:
            return nombre, False
    return None, False


def zona_sintetica(id: str, lado: str, entrada: int, extremo: int, por: str) -> Zona:
    """Una zona para los tests: la geometria real sigue NO_IMPLEMENTADA (A-29, A-35)."""
    return Zona(id, lado, entrada, extremo, por)  # type: ignore[arg-type]


def curva_de_equity(motor: MotorCableado) -> list[tuple[str, Decimal, Decimal, Decimal | None]]:
    """(dia, saldo al corte, saldo final, equity minima) por dia de la cuenta."""
    if motor.cuenta is None:
        return []
    return [
        (d.dia.isoformat(), d.saldo_corte, d.saldo_final, d.equity_minima)
        for d in motor.cuenta.cerrar_dia_en_curso()
    ]


def instante_de(minuto: int) -> datetime:
    return a_datetime(minuto)


__all__ = [
    "DEPURACION",
    "CableadoError",
    "MotorCableado",
    "Sesion",
    "TrazaBroker",
    "comprobar_reloj_unico",
    "curva_de_equity",
    "instante_de",
    "zona_sintetica",
]
