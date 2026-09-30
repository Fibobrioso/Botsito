"""El cableado del simulador (ADR-0053): dia -> motor de reglas -> ordenes -> broker -> llenado
con ticks -> capa de cuenta -> veredicto FTMO y operaciones del bot para el criterio de fidelidad.

`MotorCableado` cumple el protocolo `Motor` del arnes (ADR-0048) -`correr_dia(DiaDeMercado)`
devuelve un `ResultadoDia` con las operaciones del bot y las trazas por sesion-, asi que el arnes,
su informe y el visor lo usan sin cambios. Por dentro, cada minuto de la ventana pasa por las tres
fases de ADR-0028 en el orden de ADR-0053 §5: el broker avanza tick a tick hasta el ultimo
milisegundo anterior al cierre de M1 y la cuenta viva recibe sus eventos y marcas (riesgo por
tick); los eventos del broker quedan a disposicion de las primitivas y `EstadoDia.broker` se
actualiza (ordenes por evento); y el interprete corre el evento del cierre de M1 (estrategia).

UN SOLO RELOJ (§4) PARA EL DIA DE RIESGO: el del perfil, comprobado al arrancar contra
`huso_operativa`. El de las sesiones es otro y lo elige `reloj_sesiones` (ADR-0063). LA CUENTA
PERSISTE en toda la corrida; el estado de estrategia y el broker empiezan cada dia de cero (§6).
TICKS OBLIGATORIOS (§7): un dia sin dataset de ticks se rechaza salvo en modo depuracion, y
entonces toda la salida lo dice. SOLO CONSTRUCCION, por la compuerta del arnes (§8).
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, time
from decimal import Decimal
from pathlib import Path
from typing import Any

from botsito.cases.criterio_fidelidad import Criterio
from botsito.cases.criterio_fidelidad import Operacion as OperacionCriterio
from botsito.cases.paquete import Config
from botsito.comun.husos import huso_canonico
from botsito.config.registro import Registro
from botsito.data.velas import a_datetime
from botsito.domain.ticks import MS_POR_MINUTO
from botsito.domain.velas import MinutoUtc
from botsito.engine.arnes import DiaTrader
from botsito.engine.broker import (
    LLENADA,
    MANUAL,
    TIPOS_PETICION,
    Broker,
    Peticion,
    ReglasBroker,
    peticiones_por_dia,
)
from botsito.engine.cuenta import CuentaViva, EstadoCuenta, ReglasFase, reglas_de_fase
from botsito.engine.diagnostico import DiagnosticoRechazadoError
from botsito.engine.interprete import EstadoDia, Interprete, Momento, ReglaEjecutable
from botsito.engine.llenado import OBJETIVO, RESPALDO_M1, STOP, TICKS, Configuracion
from botsito.engine.motor import DiaDeMercado, ResultadoDia, Sesion, TrazaSesion
from botsito.engine.perfil_cuenta import PerfilCuenta, cargar_perfil
from botsito.engine.primitivas_broker import (
    ContextoDia,
    EventoBroker,
    Zona,
    clasificar_cierre,
    primitivas_cableadas,
)
from botsito.engine.simulacion import MercadoDia, mercado_de_construccion, reglas_broker_de
from botsito.engine.simulador_config import FICHERO_LLENADO, cargar_config_llenado
from botsito.engine.tope_trader import (
    ACUMULADOR_DIA,
    ACUMULADOR_SEMANA,
    ORIGEN_FIRMA,
    ORIGEN_TRADER,
    SeguidorTope,
    TopeTrader,
)
from botsito.engine.visor import DetalleBroker, EventoVisor, OrdenVisor, ZonaVisor
from botsito.engine.zonas import zonas_del_dia

DEPURACION = "DEPURACION: respaldo M1, no cuenta"
NOMBRE_MOTOR = "spec vigente + broker simulado (ADR-0053)"
CARPETA_PERFILES = Path("knowledge") / "cuentas"


class CableadoError(ValueError):
    """El cableado no puede correr asi: nunca se adivina."""


@dataclass
class TrazaBroker:
    """Lo que el broker y la cuenta hicieron en un dia, para el informe y el visor."""

    eventos: list[tuple[int, str, str, str]] = field(default_factory=list)  # ms, tipo, id, fuente
    rechazos: int = 0
    por_fuente: dict[str, int] = field(default_factory=lambda: {TICKS: 0, RESPALDO_M1: 0})
    huecos: set[str] = field(default_factory=set)
    peticiones: list[Peticion] = field(default_factory=list)  # al servidor, R13
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
    perfil: str = ""  # nombre del perfil y fase, solo para el informe
    fase: str = ""
    primitivas_extra: Mapping[str, Any] = field(default_factory=dict)  # sinteticas (tests)
    acumuladores_extra: Mapping[str, Any] = field(default_factory=dict)  # sinteticas (tests)
    zonas_de: Callable[[MercadoDia], Mapping[str, Zona]] | None = None  # sinteticas (tests)
    tope: TopeTrader | None = None  # el tope propio del trader (A-44), si esta fijado
    limpia: str | None = None  # la lectura de A-21, si esta fijada (o en diagnostico)
    stops_level_diagnostico: int | None = None  # A-27 en diagnostico (ADR-0057)
    tipo_orden: str | None = None  # A-47 fijado o en diagnostico; sin el, la limite de siempre
    # DIAGNOSTICO: la cuenta empieza de cero cada dia, sin arrastrar saldo ni frenos (revision de
    # F35); por defecto se arrastra, ADR-0053 §6
    cuenta_diaria: bool = False
    cuenta: CuentaViva | None = None
    seguidor: SeguidorTope | None = None
    # el primer limite que se toco en toda la corrida: (origen, cual, instante ms)
    primero_en_tocar: tuple[str, str, int] | None = None
    trazas_broker: dict[str, TrazaBroker] = field(default_factory=dict)
    brokers: dict[str, Broker] = field(default_factory=dict)
    estados: dict[str, EstadoDia] = field(default_factory=dict)  # el EstadoDia de cada dia corrido

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
        if self.cuenta_diaria:
            self.cuenta, self.seguidor = None, None
        if self.cuenta is None:
            self.cuenta = CuentaViva(self.reglas_fase, self.contrato, primero * MS_POR_MINUTO - 1)
        broker = Broker(
            self.reglas_broker,
            self.config_llenado,
            md.mercado(),
            self.contrato,
            md.escala,
            stops_level_diagnostico=self.stops_level_diagnostico,
        )
        if self.tope is not None and self.seguidor is None:
            self.seguidor = SeguidorTope(
                self.tope, _instante(primero * MS_POR_MINUTO - 1), self.cuenta.saldo
            )
        ctx = ContextoDia(broker, self.cuenta, self.contrato, md.escala, tope=self.tope)
        if self.zonas_de is not None:
            ctx.zonas.update(self.zonas_de(md))
        primitivas = primitivas_cableadas(self.registro, ctx, self.limpia, self.tipo_orden)
        if self.primitivas_extra or self.acumuladores_extra:
            predicados = dict(primitivas.predicados)
            predicados.update(self.primitivas_extra)
            acumuladores = dict(primitivas.acumuladores)
            acumuladores.update(self.acumuladores_extra)
            primitivas = type(primitivas)(predicados, primitivas.acciones, acumuladores)
        interprete = Interprete(self.vocabulario, primitivas)
        estado = EstadoDia()
        self.estados[clave] = estado
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
            # la PEOR equity del minuto y su instante, antes de que la lectura reinicie el tramo:
            # el tope del trader se lee como el de la firma, con la peor marca (ADR-0053 §5)
            peor_equity, peor_ms = self.cuenta.peor_equity_del_tramo()
            ctx.acumuladores = self.cuenta.acumuladores()
            if self.seguidor is not None:
                self.seguidor.avanzar(_instante(hasta_ms), self.cuenta.saldo)
                ctx.acumuladores.update(self.seguidor.acumuladores(self.cuenta.saldo, peor_equity))
            self._anotar_toque(ctx.acumuladores, peor_ms)
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
        tb.peticiones = list(broker.traza().peticiones)
        tb.equity_fin = self.cuenta.equity
        tb.saldo_fin = self.cuenta.saldo
        for nombre, traza in trazas.items():
            traza.anotaciones.update(estado.anotaciones.get(nombre, {}))
        self.trazas_broker[clave] = tb
        self.brokers[clave] = broker
        return ResultadoDia(clave, self._operaciones_del_bot(broker, md, dia, limites), trazas)

    def _anotar_toque(self, acumuladores: Mapping[str, Decimal], peor_ms: int) -> None:
        """El primer limite que se toca en la corrida, y de quien es: del trader (RN-020, A-44) o
        de la firma (la cuenta, ADR-0050). Los dos son independientes; se aplica el que se toque
        antes y la traza dice cual. El toque del trader lleva el instante de la peor marca del
        minuto; el de la firma, el instante exacto de su suspension; a igual instante, la traza
        nombra al trader y el mas restrictivo manda igual."""
        if self.primero_en_tocar is not None:
            return
        assert self.cuenta is not None
        trader: tuple[str, str, int] | None = None
        for cual in (ACUMULADOR_DIA, ACUMULADOR_SEMANA):
            valor, tope = acumuladores.get(cual), acumuladores.get(f"{cual}:tope")
            if valor is not None and tope is not None and valor >= tope:
                trader = (ORIGEN_TRADER, cual, peor_ms)
                break
        firma: tuple[str, str, int] | None = None
        if self.cuenta.estado is EstadoCuenta.SUSPENDIDA and self.cuenta.instante is not None:
            ms = int(self.cuenta.instante.timestamp() * 1000)
            firma = (ORIGEN_FIRMA, self.cuenta.motivo.split(":")[0], ms)
        if trader is not None and (firma is None or trader[2] <= firma[2]):
            self.primero_en_tocar = trader
        elif firma is not None:
            self.primero_en_tocar = firma

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
    """ADR-0053 §4: el reloj del perfil y `huso_operativa` -el del DIA DE RIESGO- tienen que dar
    la misma medianoche en cada dia de la corrida; si no, el cableado se niega. El reloj de las
    sesiones no entra aqui: puede ser otro (`reloj_sesiones`, ADR-0063)."""
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
    return Zona(id, lado, entrada, extremo, por)


def curva_de_equity(motor: MotorCableado) -> list[tuple[str, Decimal, Decimal, Decimal | None]]:
    """(dia, saldo al corte, saldo final, equity minima) por dia CORRIDO. La cuenta corta todos
    los dias de calendario que cruza entre dos dias corridos (el limite diario se recalcula cada
    dia), pero solo se listan los dias con mercado: la curva no nombra ningun dia que la corrida no
    haya leido."""
    if motor.cuenta is None:
        return []
    return [
        (d.dia.isoformat(), d.saldo_corte, d.saldo_final, d.equity_minima)
        for d in motor.cuenta.cerrar_dia_en_curso()
        if d.dia.isoformat() in motor.trazas_broker
    ]


def instante_de(minuto: int) -> datetime:
    return a_datetime(minuto)


def perfil_del_repo(repo: Path, nombre: str | None) -> PerfilCuenta:
    """El perfil de cuenta: el pedido por nombre o, si `knowledge/cuentas/` tiene uno solo, ese.
    Con varios y sin nombre, se pide. Ningun nombre de firma vive en el codigo (ADR-0050)."""
    carpeta = repo / CARPETA_PERFILES
    if nombre is not None:
        ruta = carpeta / f"{nombre}.yaml"
        if not ruta.exists():
            raise CableadoError(f"no existe el perfil {nombre!r} en {CARPETA_PERFILES}")
        return cargar_perfil(ruta)
    rutas = sorted(carpeta.glob("*.yaml"))
    if len(rutas) != 1:
        raise CableadoError(
            f"{CARPETA_PERFILES} tiene {len(rutas)} perfiles: hay que pedir uno con --perfil"
        )
    return cargar_perfil(rutas[0])


def construir_motor_cableado(
    repo: Path,
    carpeta_datos: Path,
    criterio: Criterio,
    config: Config,
    registro: Registro,
    vocabulario: Mapping[str, Mapping[str, Any]],
    reglas: Sequence[ReglaEjecutable],
    dias: Sequence[DiaTrader],
    perfil: PerfilCuenta,
    fase: str | None,
    depuracion: bool,
    tope: TopeTrader | None = None,
    limpia: str | None = None,
    stops_level_diagnostico: int | None = None,
    tipo_orden: str | None = None,
) -> MotorCableado:
    """El motor cableado sobre los dias de CONSTRUCCION pedidos: el mercado de cada dia (M1 y
    ticks) pasa por la compuerta del arnes caso a caso (ADR-0053 §8). La fase, si no se pide, es
    la primera que declara el perfil (DECISION pendiente de validar). `stops_level_diagnostico`
    es el stops level hipotetico de A-27 (ADR-0057): se rechaza si el perfil ya lo tiene."""
    reglas_broker = reglas_broker_de(perfil)
    if stops_level_diagnostico is not None and reglas_broker.stops_level_puntos is not None:
        raise DiagnosticoRechazadoError(
            f"el perfil {perfil.nombre} ya fija el stops level ({reglas_broker.stops_level_puntos}"
            " puntos, A-27 medida): la corrida cuenta y no admite --diagnostico-a27"
        )
    fase_real = fase if fase is not None else perfil.fases()[0]
    mercados = {
        d.dia: mercado_de_construccion(repo, carpeta_datos, criterio, config, registro, d.id)
        for d in dias
    }
    return MotorCableado(
        vocabulario=vocabulario,
        reglas=reglas,
        registro=registro,
        mercados=mercados,
        reglas_broker=reglas_broker,
        reglas_fase=reglas_de_fase(perfil, fase_real),
        config_llenado=cargar_config_llenado(repo / FICHERO_LLENADO).configuracion(),
        contrato=registro.decimal("instrumento_contrato"),
        depuracion=depuracion,
        perfil=perfil.nombre,
        fase=fase_real,
        tope=tope,
        limpia=limpia,
        stops_level_diagnostico=stops_level_diagnostico,
        tipo_orden=tipo_orden,
    )


def _instante(ms: int) -> datetime:
    return datetime.fromtimestamp(ms / 1000, UTC)


def detalle_para_visor(motor: MotorCableado, dia: str) -> DetalleBroker | None:
    """Las ordenes, las posiciones y los eventos del broker de un dia ya corrido, para el visor."""
    broker = motor.brokers.get(dia)
    tb = motor.trazas_broker.get(dia)
    if broker is None or tb is None:
        return None
    escala = broker.escala
    ordenes = tuple(
        OrdenVisor(
            id=o.id,
            lado=o.lado,
            precio=_precio(o.precio, escala),
            lotes=o.lotes,
            stop=_precio(o.stop, escala),
            objetivo=_precio(o.objetivo, escala),
            estado=o.estado,
            colocada=_instante(o.colocada_ms),
        )
        for o in sorted(broker.ordenes.values(), key=lambda o: (o.colocada_ms, o.id))
    )
    posiciones = tuple(
        OrdenVisor(
            id=p.id,
            lado=p.lado,
            precio=_precio(p.entrada, escala),
            lotes=p.lotes,
            stop=_precio(p.stop, escala),
            objetivo=_precio(p.objetivo, escala),
            estado=p.motivo_cierre or "abierta",
            colocada=_instante(p.abierta_ms),
            cerrada=_instante(p.cerrada_ms) if p.cerrada_ms is not None else None,
            precio_cierre=_precio(p.precio_cierre, escala) if p.precio_cierre is not None else None,
        )
        for p in sorted(broker.posiciones.values(), key=lambda p: (p.abierta_ms, p.id))
    )
    eventos = tuple(
        EventoVisor(_instante(ms), tipo, id, fuente) for ms, tipo, id, fuente in tb.eventos
    )
    estado = motor.estados.get(dia)
    zonas = tuple(
        ZonaVisor(
            id=z.id,
            lado=z.lado,
            entrada=_precio(z.entrada, escala),
            extremo=_precio(z.extremo, escala),
            por=z.por,
            desde=_instante(z.desde * MS_POR_MINUTO) if z.desde is not None else None,
            formada=_instante(z.formada * MS_POR_MINUTO) if z.formada is not None else None,
        )
        for z in (zonas_del_dia(estado).values() if estado is not None else ())
    )
    return DetalleBroker(
        ordenes=ordenes,
        posiciones=posiciones,
        eventos=eventos,
        zonas=zonas,
        rechazos=tb.rechazos,
        huecos=tuple(sorted(tb.huecos)),
        saldo_fin=tb.saldo_fin,
        equity_fin=tb.equity_fin,
        depuracion=DEPURACION if tb.depuracion else None,
    )


def _primero_en_tocar(motor: MotorCableado) -> str:
    if motor.primero_en_tocar is None:
        return "ninguno"
    origen, cual, ms = motor.primero_en_tocar
    return f"{origen} ({cual}) en {_instante(ms).isoformat()}"


def informe_simulacion(motor: MotorCableado) -> str:
    """La cola del informe del arnes en modo simulacion: veredicto de la cuenta sobre el tramo,
    curva de equity por dia, eventos del broker y huecos con nombre. Determinista."""
    estado, motivo, instante = motor.veredicto()
    dias = sorted(motor.trazas_broker)
    depurados = [d for d in dias if motor.trazas_broker[d].depuracion]
    lineas = [
        "",
        "## Simulacion (ADR-0053)",
        f"MOTOR: {NOMBRE_MOTOR}",
        f"PERFIL: {motor.perfil or '-'}; FASE: {motor.fase or '-'}",
        f"DIAS CORRIDOS: {len(dias)}",
        "TOPE DEL TRADER (RN-020, A-44): "
        + (motor.tope.descripcion() if motor.tope is not None else "sin fijar: hueco con nombre"),
        "PRIMERO EN TOCAR UN LIMITE: " + _primero_en_tocar(motor),
    ]
    if motor.cuenta_diaria:
        lineas.append(
            "CUENTA: REINICIADA CADA DIA (diagnostico): el veredicto, el saldo y la curva son solo "
            "del ultimo dia corrido"
        )
    if depurados:
        lineas.append(
            f"{DEPURACION}: {len(depurados)} dias sobre respaldo M1 ({', '.join(depurados)})"
        )
    lineas += [
        "",
        "### Veredicto de la cuenta sobre el tramo",
        f"estado: {estado.value}",
        f"motivo: {motivo}",
        f"instante: {instante.isoformat() if instante is not None else '-'}",
    ]
    if motor.cuenta is not None:
        lineas += [
            f"saldo final: {motor.cuenta.saldo}",
            f"equity final: {motor.cuenta.equity}",
            f"dias de trading: {motor.cuenta.dias_de_trading}",
        ]
    lineas += ["", "### Curva de equity (dia | saldo al corte | saldo final | equity minima)"]
    for dia, corte, final, minima in curva_de_equity(motor):
        lineas.append(f"{dia} | {corte} | {final} | {minima if minima is not None else '-'}")
    por_fuente: dict[str, int] = {TICKS: 0, RESPALDO_M1: 0}
    rechazos = 0
    huecos: set[str] = set()
    total = 0
    lineas += ["", "### Eventos del broker (dia | instante UTC | tipo | id | fuente)"]
    for dia in dias:
        tb = motor.trazas_broker[dia]
        rechazos += tb.rechazos
        huecos |= tb.huecos
        for fuente, n in tb.por_fuente.items():
            por_fuente[fuente] = por_fuente.get(fuente, 0) + n
        for ms, tipo, id, fuente in tb.eventos:
            total += 1
            lineas.append(f"{dia} | {_instante(ms).isoformat()} | {tipo} | {id} | {fuente}")
    if not total:
        lineas.append("ninguno")
    lineas += [
        "",
        f"eventos: {total}; por fuente: "
        + ", ".join(f"{f} {n}" for f, n in sorted(por_fuente.items())),
        f"rechazos del broker: {rechazos}",
        "huecos con nombre (primitivas sin contrato que se pidieron): "
        + (", ".join(sorted(huecos)) if huecos else "ninguno"),
    ]
    return "\n".join(lineas + _informe_peticiones(motor)) + "\n"


def _informe_peticiones(motor: MotorCableado) -> list[str]:
    """Las peticiones al servidor por dia de la firma (R13): el total de cada dia, el mayor y el
    limite del perfil al lado. SOLO SE MIDE: ninguna regla frena por peticiones todavia."""
    huso = motor.reglas_broker.huso_corte
    contadas = peticiones_por_dia(
        (p for d in sorted(motor.trazas_broker) for p in motor.trazas_broker[d].peticiones), huso
    )
    # todos los dias corridos salen, tambien los que no tuvieron ninguna peticion
    vacio = {**dict.fromkeys(TIPOS_PETICION, 0), "total": 0, "rechazadas": 0}
    por_dia = {date.fromisoformat(d): dict(vacio) for d in motor.trazas_broker} | contadas
    por_dia = dict(sorted(por_dia.items()))
    lineas = [
        "",
        f"### Peticiones al servidor (R13; dia de la firma en {huso.key})",
        "LECTURA: colocar, modificar, cancelar y cerrar, aceptadas o rechazadas, emitidas por el "
        "bot; solo se mide, nada frena",
        f"dia | total | {' | '.join(TIPOS_PETICION)} | rechazadas",
    ]
    for dia, n in por_dia.items():
        tipos = " | ".join(str(n[t]) for t in TIPOS_PETICION)
        lineas.append(f"{dia.isoformat()} | {n['total']} | {tipos} | {n['rechazadas']}")
    mayor = "0"
    if por_dia:
        dia_max, n_max = max(por_dia.items(), key=lambda kv: (kv[1]["total"], kv[0]))
        mayor = f"{n_max['total']} ({dia_max.isoformat()})"
    else:
        lineas.append("ninguna")
    limite = motor.reglas_broker.mensajes_dia_max
    lineas.append(
        f"maximo diario: {mayor}; firma_mensajes_dia_max: "
        + (str(limite) if limite is not None else "sin leer")
    )
    return lineas


__all__ = [
    "DEPURACION",
    "NOMBRE_MOTOR",
    "CableadoError",
    "MotorCableado",
    "Sesion",
    "TrazaBroker",
    "comprobar_reloj_unico",
    "construir_motor_cableado",
    "curva_de_equity",
    "detalle_para_visor",
    "informe_simulacion",
    "perfil_del_repo",
    "instante_de",
    "zona_sintetica",
]
