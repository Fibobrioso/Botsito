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

from collections import Counter
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
from botsito.domain.cierres import CalendarioCierres
from botsito.domain.ticks import MS_POR_MINUTO
from botsito.domain.velas import MinutoUtc
from botsito.engine.arnes import DiaTrader
from botsito.engine.broker import (
    CANCELADA,
    LLENADA,
    MANUAL,
    PETICION_CANCELAR,
    PETICION_COLOCAR,
    RECHAZADA,
    TIPOS_PETICION,
    Broker,
    Peticion,
    ReglasBroker,
    peticiones_por_dia,
)
from botsito.engine.calendario_cierres import (
    CalendarioError,
    cargar_calendario,
    ruta_calendario,
)
from botsito.engine.cuenta import CuentaViva, EstadoCuenta, ReglasFase, reglas_de_fase
from botsito.engine.diagnostico import DiagnosticoRechazadoError
from botsito.engine.freno import Corte
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
from botsito.engine.racha import SeguidorRacha, seguidor_del_registro
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
# el instante del break even de RN-014 (ADR-0065): `tocar` es al tick; `cierre`, al cierre de la M1
PARAMETRO_BREAK_EVEN = "break_even_condicion"
BREAK_EVEN_AL_TOCAR = "tocar"
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
    cortes: list[Corte] = field(default_factory=list)  # el freno de peticiones (ADR-0067)
    cierres: list[Corte] = field(default_factory=list)  # los cierres de mercado (ADR-0068)
    equity_fin: Decimal = Decimal(0)
    saldo_fin: Decimal = Decimal(0)
    depuracion: bool = False
    # ordenes pendientes que cancelo la red de seguridad al terminar el dia (ADR-0053 §6): lo que
    # RN-035 (a ventana_fin) y RN-036 (la racha) no retiraron antes
    cancelados_fin_dia: int = 0
    # la vida de la orden, SOLO para el informe (rama trabajo/corrida-construccion, respuesta del
    # consultor a la PARADA 2, punto 1.b): por cada peticion de cancelar, (instante ms, id de la
    # orden, motivo), donde el motivo es lo que el cableado puede leer sin decidir nada: las reglas
    # que dispararon en ese cierre de M1 y donde cayo el cierre (al abrir otra sesion, en
    # ventana_fin), o la red de seguridad del fin del dia
    cancelaciones: list[tuple[int, str, str]] = field(default_factory=list)
    limites: tuple[tuple[str, int, int], ...] = ()  # (sesion, desde, hasta) en minutos UTC
    # SOLO SALIDA (rama trabajo/margen-lote, fase 1): por orden, (margen requerido, margen libre,
    # riesgo en % del saldo) al colocarla, lo que anota `colocar_orden_limite` en el contexto
    # (`ContextoDia.margen_al_colocar`, el mismo diccionario). None en lo que no se pudo medir
    margen_al_colocar: dict[str, tuple[Decimal | None, Decimal | None, Decimal | None]] = field(
        default_factory=dict
    )


MOTIVO_FIN_DIA = "viva al cerrar el dia: cancelada por la red de seguridad (ADR-0053 §6)"
MOTIVO_SIN_REGLA = "sin regla disparada en ese cierre"


def _motivo_de_cancelacion(
    instante: int, limites: Sequence[tuple[str, int, int]], disparadas: Sequence[str]
) -> str:
    """Donde cayo el cierre de M1 que cancelo y que reglas dispararon en el: es lo que la traza
    deja leer. `instante` es el minuto UTC del cierre."""
    donde = ""
    if any(instante == desde for _, desde, _ in limites[1:]):
        donde = "al abrir otra sesion; "
    elif limites and instante == max(hasta for _, _, hasta in limites):
        donde = "en ventana_fin; "
    reglas = ", ".join(sorted(set(disparadas))) or MOTIVO_SIN_REGLA
    return f"{donde}reglas disparadas en ese cierre: {reglas}"


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
    # la racha de perdidas seguidas del trader (RN-036, A-51; ADR-0077): persiste entre dias como
    # la cuenta y el seguidor del tope, y se reinicia con `cuenta_diaria` como ellos
    racha: SeguidorRacha | None = None
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
        limites = [(n, int(a), int(b)) for n, a, b in dia.limites()]  # por la puerta (ADR-0069)
        primero = min(d for _, d, _ in limites)
        ultimo = max(h for _, _, h in limites)
        if self.cuenta_diaria:
            self.cuenta, self.seguidor, self.racha = None, None, None
        if self.cuenta is None:
            self.cuenta = CuentaViva(self.reglas_fase, self.contrato, primero * MS_POR_MINUTO - 1)
        if self.racha is None:
            self.racha = seguidor_del_registro(self.registro)
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
        ctx = ContextoDia(
            broker, self.cuenta, self.contrato, md.escala, tope=self.tope, racha=self.racha
        )
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
        tb = TrazaBroker(
            depuracion=self.depuracion or not md.origen_ticks,
            limites=tuple(limites),
            margen_al_colocar=ctx.margen_al_colocar,
        )
        vistos = 0
        peticiones_vistas = 0  # para anotar las cancelaciones de cada cierre (solo el informe)
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
            desde = next((d for n, d, _ in limites if n == sesion), None)
            momento = Momento(MinutoUtc(instante), sesion, abre, dia.datos, desde, primero)
            ctx.break_even_vigilable = None
            evento = interprete.evento(self.reglas, momento, estado)
            # el break even de RN-014 AL TICK (ADR-0065): el nivel que el predicado vio en este
            # cierre se vigila en los ticks que vienen; el instante lo dice break_even_condicion
            if ctx.break_even_vigilable is not None and (
                self.registro.opcion(PARAMETRO_BREAK_EVEN) == BREAK_EVEN_AL_TOCAR
            ):
                posicion, nivel = ctx.break_even_vigilable
                broker.vigilar_break_even(posicion, nivel, hasta_ms)
            if sesion is not None:
                traza = trazas[sesion]
                traza.fijados += [(instante, r, h, v) for r, h, v in evento.fijados]
                traza.no_implementadas |= evento.no_implementadas
                traza.bloqueadas |= evento.bloqueadas
                traza.disparadas |= set(evento.disparadas)
                traza.empates |= set(evento.empates)
            # la vida de la orden, para el informe: que cancelaciones pidio este cierre y que
            # reglas dispararon en el (lectura de la traza; no decide nada)
            peticiones = broker.traza().peticiones
            for pet in peticiones[peticiones_vistas:]:
                if pet.tipo == PETICION_CANCELAR:
                    motivo = _motivo_de_cancelacion(instante, limites, evento.disparadas)
                    tb.cancelaciones.append((pet.instante_ms, pet.id, motivo))
            peticiones_vistas = len(peticiones)
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
                tb.cancelados_fin_dia += 1
                tb.cancelaciones.append((fin_ms, o.id, MOTIVO_FIN_DIA))
        nuevos = broker.avanzar(fin_ms)
        self._a_la_cuenta(broker, ctx, tb, nuevos, vistos, fin_ms)
        tb.huecos |= ctx.huecos
        tb.rechazos = len(broker.traza().rechazos)
        tb.peticiones = list(broker.traza().peticiones)
        tb.cortes = list(broker.traza().cortes)
        tb.cierres = list(broker.traza().cierres)
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
                por = ctx.por_de_orden.get(p.orden_id)
                ctx.eventos.append(EventoBroker(ms, tipo, id, por, resultado))
                # para los intentos de cada escenario (acumulador `cartuchos`, ADR-0066)
                ctx.cierres.append((p.orden_id, resultado, por))
                # y para la racha de perdidas del trader, que cruza los dias (RN-036, ADR-0077)
                if self.racha is not None:
                    self.racha.registrar(ms, resultado, por)
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
    es el stops level hipotetico de A-27 (ADR-0057): se rechaza si el perfil ya lo tiene.

    El calendario de cierres del perfil (`knowledge/cuentas/cierres/`, ADR-0068) entra siempre: sin
    el no se corre, y tampoco un dia fuera de lo que cubre, para que un calendario vencido no
    cambie una medida en silencio."""
    calendario = calendario_del_perfil(repo, perfil.nombre)
    reglas_broker = reglas_broker_de(perfil, registro, calendario)
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
    comprobar_que_cubre(calendario, mercados, perfil.nombre)
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


def calendario_del_perfil(repo: Path, perfil: str) -> CalendarioCierres:
    """El calendario de cierres del perfil (`knowledge/cuentas/cierres/`, ADR-0068); sin el, el
    motor no corre."""
    try:
        return cargar_calendario(ruta_calendario(repo, perfil)).calendario()
    except CalendarioError as exc:
        raise CableadoError(f"el perfil {perfil} sin calendario de cierres: {exc}") from exc


def comprobar_que_cubre(
    calendario: CalendarioCierres, mercados: Mapping[str, MercadoDia], perfil: str
) -> None:
    """Cada dia pedido, entero dentro de lo que cubre el calendario; si no, el motor no corre, para
    que un calendario vencido no cambie una medida en silencio (ADR-0068 §7)."""
    fuera = sorted(
        dia
        for dia, md in mercados.items()
        if not calendario.cubre_desde_ms <= md.desde_ms < md.hasta_ms <= calendario.cubre_hasta_ms
    )
    if fuera:
        raise CableadoError(
            f"dias fuera del calendario de cierres de {perfil} (ADR-0068): {fuera}; se alarga "
            "`cubre` revisando las Trading Updates de esas semanas"
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
        "RACHA DE PERDIDAS (RN-036, A-51): "
        + (motor.racha.descripcion() if motor.racha is not None else "sin dias corridos"),
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
    return "\n".join(lineas + _informe_ordenes(motor) + _informe_peticiones(motor)) + "\n"


# ------------------------------------------- la vida de la orden (R3.1, PARADA 2, punto 1.b)
#
# Una linea por orden que el bot intento colocar, con su resultado y el motivo que da el broker
# (un rechazo: precio_invalido, stops_level, ...) o el cableado (una cancelacion: las reglas que
# dispararon en ese cierre y donde cayo; la red de seguridad del fin del dia). Solo LEE la traza:
# `broker.ordenes`, `broker.traza().rechazos` y `TrazaBroker.cancelaciones`. Determinista.

CABECERA_ORDENES = (
    "### Ordenes (dia | sesion | id | colocada UTC | precio | resultado | motivo | instante del "
    "resultado | lote | distancia (puntos) | margen requerido (USD) | margen libre al colocar (USD)"
    " | riesgo (% del saldo))"
)
# las cuatro ultimas columnas (rama trabajo/margen-lote, fase 1) son SOLO salida: el lote pedido,
# la distancia de la orden a su stop, y el margen y el riesgo medidos al colocar con la unica
# funcion de margen (`broker.margen_requerido`); `-` en lo que no se pudo medir (perfil sin
# apalancamiento, minuto sin precio). Van al final para que lo que ya leia las filas siga leyendolas
SIN_MEDIDA = "-"
RESULTADO_LLENADA = "llenada"
RESULTADO_RECHAZADA = "rechazada"
RESULTADO_CANCELADA = "cancelada"
RESULTADO_VIVA = "viva al cerrar el dia"


def _sesion_de(colocada_ms: int, limites: Sequence[tuple[str, int, int]]) -> str:
    """La sesion de una orden, por el CIERRE de M1 en que se coloco: el motor la coloca en
    `instante * MS_POR_MINUTO - 1` y asigna la sesion por `instante` (`_sesion`, el cierre), asi
    que el minuto de la orden es `(colocada_ms + 1) // MS_POR_MINUTO`. Con `colocada_ms //
    MS_POR_MINUTO` la orden del primer cierre de una sesion salia en la anterior o en «-»
    (revisor de trabajo/corrida-construccion, b1). Fuera de las sesiones, «-»."""
    sesion, _ = _sesion(limites, (colocada_ms + 1) // MS_POR_MINUTO)
    return sesion or "-"


FilaOrden = tuple[
    str,  # dia
    str,  # sesion
    str,  # id
    datetime,  # colocada
    Decimal,  # precio
    str,  # resultado
    str,  # motivo
    datetime | None,  # instante del resultado
    Decimal,  # lote pedido
    int,  # distancia al stop, en puntos
    Decimal | None,  # margen requerido al colocar (moneda); None si no se pudo medir
    Decimal | None,  # margen libre de la cuenta al colocar (moneda); None si no se pudo medir
    Decimal | None,  # riesgo al colocar, en % del saldo; None si no se pudo medir
]


def vida_de_las_ordenes(motor: MotorCableado) -> list[FilaOrden]:
    """(dia, sesion, id, colocada, precio, resultado, motivo, instante del resultado, lote,
    distancia, margen requerido, margen libre, riesgo) por orden, por dia y por instante de
    colocacion. Las cinco ultimas son SOLO salida (rama trabajo/margen-lote, fase 1)."""
    salida: list[FilaOrden] = []
    for dia in sorted(motor.trazas_broker):
        broker = motor.brokers.get(dia)
        tb = motor.trazas_broker[dia]
        if broker is None:
            continue
        rechazo_de = {r.orden_id: r for r in broker.traza().rechazos}
        cancelacion_de = {id: (ms, motivo) for ms, id, motivo in tb.cancelaciones}
        llenada_en = {p.orden_id: p.abierta_ms for p in broker.posiciones.values()}
        for o in sorted(broker.ordenes.values(), key=lambda o: (o.colocada_ms, o.id)):
            sesion = _sesion_de(o.colocada_ms, tb.limites)
            cuando: int | None = None
            if o.estado == RECHAZADA:
                r = rechazo_de.get(o.id)
                resultado, motivo = RESULTADO_RECHAZADA, r.motivo if r else "sin motivo en la traza"
                cuando = r.instante_ms if r else o.colocada_ms
            elif o.estado == LLENADA or o.id in llenada_en:
                resultado, motivo = RESULTADO_LLENADA, "-"
                cuando = llenada_en.get(o.id, o.ultimo_cambio_ms)
            elif o.estado == CANCELADA:
                ms, motivo = cancelacion_de.get(
                    o.id, (o.ultimo_cambio_ms, "sin motivo en la traza")
                )
                resultado = RESULTADO_VIVA if motivo == MOTIVO_FIN_DIA else RESULTADO_CANCELADA
                cuando = ms
            else:
                resultado, motivo, cuando = o.estado, "-", o.ultimo_cambio_ms
            requerido, libre, riesgo = tb.margen_al_colocar.get(o.id, (None, None, None))
            salida.append(
                (
                    dia,
                    sesion,
                    o.id,
                    _instante(o.colocada_ms),
                    _precio(o.precio, broker.escala),
                    resultado,
                    motivo,
                    _instante(cuando) if cuando is not None else None,
                    o.lotes,
                    abs(o.precio - o.stop),
                    requerido,
                    libre,
                    riesgo,
                )
            )
    return salida


def _moneda(valor: Decimal | None) -> str:
    return SIN_MEDIDA if valor is None else f"{valor:.2f}"


def _informe_ordenes(motor: MotorCableado) -> list[str]:
    lineas = ["", CABECERA_ORDENES]
    filas = vida_de_las_ordenes(motor)
    for (
        dia,
        sesion,
        id,
        colocada,
        precio,
        resultado,
        motivo,
        cuando,
        lote,
        dist,
        req,
        lib,
        rg,
    ) in filas:
        lineas.append(
            f"{dia} | {sesion} | {id} | {colocada.isoformat()} | {precio} | {resultado} | "
            f"{motivo} | {cuando.isoformat() if cuando is not None else '-'} | {lote} | {dist} | "
            f"{_moneda(req)} | {_moneda(lib)} | {SIN_MEDIDA if rg is None else f'{rg:.3f}'}"
        )
    if not filas:
        lineas.append("ninguna")
    resumen = Counter(f[5] for f in filas)
    lineas.append(
        "ordenes: " + (", ".join(f"{k} {v}" for k, v in sorted(resumen.items())) if filas else "0")
    )
    # los rechazos del broker por motivo y por mes: los de colocar (la orden nace rechazada) y los
    # de modificar (la orden sigue como estaba), por separado
    por_motivo: Counter[tuple[str, str, str]] = Counter()
    for dia in sorted(motor.trazas_broker):
        broker = motor.brokers.get(dia)
        if broker is None:
            continue
        for r in broker.traza().rechazos:
            o = broker.ordenes.get(r.orden_id)
            tipo = PETICION_COLOCAR if o is not None and o.estado == RECHAZADA else "modificar"
            por_motivo[(dia[:7], r.motivo, tipo)] += 1
    lineas += ["", "### Rechazos por motivo (mes | motivo | peticion | rechazos)"]
    lineas += [
        f"{mes} | {motivo} | {tipo} | {n}" for (mes, motivo, tipo), n in sorted(por_motivo.items())
    ]
    if not por_motivo:
        lineas.append("ninguno")
    return lineas


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
    return lineas + _informe_freno(motor) + _informe_cierres(motor)


def _informe_freno(motor: MotorCableado) -> list[str]:
    """El freno de peticiones (ADR-0067): sus umbrales y, por dia, cada aviso y cada peticion
    negada con su motivo. Un dia sin nada que contar no sale."""
    f = motor.reglas_broker.freno
    umbrales = (
        f"aviso {f.aviso}, corte {f.corte}, bucle {f.bucle_repeticiones} iguales en "
        f"{(f.bucle_ms or 0) // MS_POR_MINUTO} min"
        if f is not None
        else f"sin umbrales del registro: corta en firma_mensajes_dia_max "
        f"({motor.reglas_broker.mensajes_dia_max})"
    )
    lineas = ["", "### El freno de peticiones (ADR-0067)", f"umbrales: {umbrales}"]
    for dia in sorted(motor.trazas_broker):
        for c in motor.trazas_broker[dia].cortes:
            lineas.append(f"{dia} | {c.instante_ms} | {c.motivo} | {c.tipo} | {c.id}")
    if len(lineas) == 3:
        lineas.append("ningun aviso ni ninguna peticion negada")
    return lineas


def _informe_cierres(motor: MotorCableado) -> list[str]:
    """Los cierres de mercado (ADR-0068): el calendario que se uso y, por dia, cada colocacion o
    modificacion negada y cada pendiente cancelada, con su motivo. Un dia sin nada no sale."""
    c = motor.reglas_broker.cierres
    if c is None:
        cabecera = "sin calendario: el broker no comprueba los cierres"
    else:
        cabecera = (
            f"cubre {_instante(c.calendario.cubre_desde_ms):%Y-%m-%d %H:%M} a "
            f"{_instante(c.calendario.cubre_hasta_ms):%Y-%m-%d %H:%M} UTC, "
            f"{len(c.calendario.cierres)} cierres; margen {c.margen_ms // MS_POR_MINUTO} min, "
            f"minimo {c.minimo_ms // MS_POR_MINUTO} min; pendientes: "
            + ("se cancelan" if c.cancelar_pendientes else "se mantienen")
        )
    lineas = ["", "### Los cierres de mercado (ADR-0068)", f"calendario: {cabecera}"]
    for dia in sorted(motor.trazas_broker):
        for k in motor.trazas_broker[dia].cierres:
            lineas.append(f"{dia} | {k.instante_ms} | {k.motivo} | {k.tipo} | {k.id}")
    if len(lineas) == 3:
        lineas.append("ninguna peticion negada ni ninguna pendiente cancelada")
    return lineas


__all__ = [
    "DEPURACION",
    "NOMBRE_MOTOR",
    "CableadoError",
    "MotorCableado",
    "Sesion",
    "TrazaBroker",
    "calendario_del_perfil",
    "comprobar_que_cubre",
    "comprobar_reloj_unico",
    "construir_motor_cableado",
    "curva_de_equity",
    "detalle_para_visor",
    "informe_simulacion",
    "perfil_del_repo",
    "instante_de",
    "zona_sintetica",
]
