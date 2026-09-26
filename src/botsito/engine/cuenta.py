"""La capa de cuenta del simulador (ADR-0050): la mitad que dice si una cuenta pasa o se suspende.

FUNCIONES PURAS. Reciben la secuencia de operaciones -instantes, precios, lotes y cargos- y las
reglas de UNA fase, ya leidas del perfil, y devuelven el resultado. Sin IO, sin reloj de pared,
sin broker y sin ticks: el broker simulado, que produce las operaciones y sus cargos, va en otra
rama, y el cableado con el motor de estrategia tambien. Nada aqui asume un instrumento ni una
firma: el tamano del contrato entra como argumento y toda cifra de negocio viene de las reglas.

LO QUE SE LLEVA, evento a evento, en una linea de tiempo ordenada por instante:
- saldo y equity: el saldo cambia al cerrar (P/L realizado) y con cada cargo (comision, swap); la
  equity es el saldo mas el P/L flotante de lo abierto, a su ultimo precio observado;
- el dia de la firma, en el huso del perfil: un corte a cada medianoche local, ANTES de cualquier
  evento de ese instante, que fija el saldo del corte y con el, el limite del dia;
- la perdida diaria: la magnitud vigilada no puede caer POR DEBAJO del limite del dia
  (`saldo_corte - perdida_diaria_max % del capital`, o sobre el capital si la base lo dice);
- la perdida total: estatica sobre el capital inicial, o arrastrando el saldo maximo si el
  perfil lo declara;
- el objetivo de la fase y sus dias minimos: se supera en el primer cierre que deja el saldo en
  el objetivo o por encima, sin posiciones vivas y con los dias de trading cumplidos. Un dia de
  trading es un dia local en el que se ABRE una posicion;
- el estado final: EN_CURSO, SUPERADA o SUSPENDIDA, con el motivo y el instante EXACTOS. La
  primera suspension o superacion es terminal: lo que venga despues no se evalua y se cuenta;
- la guardia de tamano de posicion, SOLO como aviso: nunca cambia el estado. Sin cifra en el
  perfil no se evalua, y el resultado lo dice nombrando el parametro.

CONVENIOS DECLARADOS (ADR-0050): el limite se infringe al caer estrictamente por debajo, que es
lo que dice la fuente («drops below»); el objetivo se cumple al llegar (mayor o igual); a igual
instante, un cierre se procesa antes que un cargo, una marca o una apertura; el P/L se calcula en
la moneda de cotizacion del instrumento y se trata como moneda de la cuenta (la conversion cruzada
es del broker); las magnitudes son `Decimal`.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal
from enum import StrEnum
from statistics import median
from typing import Literal
from zoneinfo import ZoneInfo

from botsito.domain.valores import CIEN, Porcentaje
from botsito.engine.perfil_cuenta import PerfilCuenta, nombre_de_fase

Direccion = Literal["compra", "venta"]
CAPITAL_INICIAL = "saldo_inicial_cuenta"
BASE_CAPITAL = "saldo_inicial_cuenta"
BASE_CORTE = "saldo_corte_diario"
MAGNITUD_EQUITY = "equity"
MAGNITUD_SALDO = "saldo"
RATIO_AVISO = "firma_tamano_posicion_ratio_aviso"


class EstadoCuenta(StrEnum):
    EN_CURSO = "EN_CURSO"
    SUPERADA = "SUPERADA"
    SUSPENDIDA = "SUSPENDIDA"


class OperacionError(ValueError):
    """Una operacion mal formada: el motor no adivina."""


# ---------------------------------------------------------------------------------- la entrada


@dataclass(frozen=True)
class Marca:
    """Un precio observado en un instante (aware, UTC)."""

    instante: datetime
    precio: Decimal


@dataclass(frozen=True)
class Cargo:
    """Un coste con su instante: positivo resta del saldo. `concepto` es libre (comision, swap)."""

    instante: datetime
    importe: Decimal
    concepto: str


@dataclass(frozen=True)
class Operacion:
    id: str
    direccion: Direccion
    lotes: Decimal
    apertura: Marca
    cierre: Marca
    cargos: tuple[Cargo, ...] = ()
    marcas: tuple[Marca, ...] = ()  # precios observados con la posicion viva


@dataclass(frozen=True)
class ReglasFase:
    """Las reglas de UNA fase, ya leidas del perfil: el motor no vuelve a tocar el perfil."""

    perfil: str
    fase: str
    capital_inicial: Decimal
    huso_corte: ZoneInfo
    perdida_diaria_max: Porcentaje
    base_perdida_diaria: str
    perdida_total_max: Porcentaje
    perdida_total_arrastra: bool
    magnitud_vigilada: str
    objetivo: Porcentaje | None  # None: la fase no tiene objetivo
    dias_minimos: int | None  # None: la fase no exige dias
    guardia_tamano_aplica: bool
    ratio_aviso_tamano: Decimal | None  # None: la firma no da cifra


def reglas_de_fase(perfil: PerfilCuenta, fase: str) -> ReglasFase:
    """Lee del perfil todo lo que la fase necesita. Un parametro sin valor que haga falta para
    DECIDIR levanta `ParametroSinValorError` con su nombre; el de la guardia de tamano no decide
    nada y solo deja la guardia sin evaluar."""
    if fase not in perfil.fases():
        raise ValueError(f"el perfil {perfil.nombre} no tiene la fase {fase!r}: {perfil.fases()}")
    objetivo = (
        perfil.porcentaje(nombre_de_fase(fase, "objetivo"))
        if perfil.booleano(nombre_de_fase(fase, "objetivo_aplica"))
        else None
    )
    dias_minimos = (
        perfil.entero(nombre_de_fase(fase, "dias_minimos"))
        if perfil.booleano(nombre_de_fase(fase, "dias_minimos_aplica"))
        else None
    )
    guardia_aplica = perfil.booleano("firma_tamano_posicion_aviso_aplica")
    ratio: Decimal | None = None
    if guardia_aplica and RATIO_AVISO not in perfil.sin_valor():
        ratio = perfil.decimal(RATIO_AVISO)
    return ReglasFase(
        perfil=perfil.nombre,
        fase=fase,
        capital_inicial=perfil.decimal(CAPITAL_INICIAL),
        huso_corte=perfil.huso_corte(),
        perdida_diaria_max=perfil.porcentaje("firma_perdida_diaria_max"),
        base_perdida_diaria=perfil.opcion("firma_base_perdida_diaria"),
        perdida_total_max=perfil.porcentaje("firma_perdida_total_max"),
        perdida_total_arrastra=perfil.booleano("firma_perdida_total_arrastra"),
        magnitud_vigilada=perfil.opcion("firma_magnitud_vigilada"),
        objetivo=objetivo,
        dias_minimos=dias_minimos,
        guardia_tamano_aplica=guardia_aplica,
        ratio_aviso_tamano=ratio,
    )


# ----------------------------------------------------------------------------------- la salida


@dataclass(frozen=True)
class DiaDeCuenta:
    """Lo que la cuenta vio en un dia de la firma."""

    dia: date
    saldo_corte: Decimal
    limite_dia: Decimal
    equity_minima: Decimal | None  # None: ningun evento ese dia
    saldo_final: Decimal
    con_apertura: bool  # cuenta como dia de trading


@dataclass(frozen=True)
class GuardiaTamano:
    estado: Literal["evaluada", "no_evaluable", "no_aplica"]
    motivo: str
    avisos: tuple[str, ...] = ()


@dataclass(frozen=True)
class ResultadoFase:
    perfil: str
    fase: str
    estado: EstadoCuenta
    motivo: str
    instante: datetime | None
    saldo_final: Decimal
    equity_final: Decimal
    limite_total_final: Decimal
    dias_de_trading: int
    dias: tuple[DiaDeCuenta, ...]
    guardia_tamano: GuardiaTamano
    operaciones_evaluadas: int
    operaciones_tras_el_final: int


# ----------------------------------------------------------------------------- comprobaciones


def _aware(instante: datetime, donde: str) -> None:
    if instante.tzinfo is None or instante.utcoffset() is None:
        raise OperacionError(f"{donde}: el instante {instante!r} no lleva huso")


def comprobar_operacion(op: Operacion) -> None:
    _aware(op.apertura.instante, f"{op.id} apertura")
    _aware(op.cierre.instante, f"{op.id} cierre")
    if op.direccion not in ("compra", "venta"):
        raise OperacionError(f"{op.id}: direccion invalida {op.direccion!r}")
    if op.lotes <= 0:
        raise OperacionError(f"{op.id}: lotes no positivos ({op.lotes})")
    if op.cierre.instante < op.apertura.instante:
        raise OperacionError(f"{op.id}: cierra antes de abrir")
    for m in op.marcas:
        _aware(m.instante, f"{op.id} marca")
        if not op.apertura.instante <= m.instante <= op.cierre.instante:
            raise OperacionError(f"{op.id}: marca fuera de la vida de la operacion ({m.instante})")
    for c in op.cargos:
        _aware(c.instante, f"{op.id} cargo")
        if not op.apertura.instante <= c.instante <= op.cierre.instante:
            raise OperacionError(f"{op.id}: cargo fuera de la vida de la operacion ({c.instante})")


def pnl(op: Operacion, precio: Decimal, contrato: Decimal) -> Decimal:
    """P/L de la operacion al precio dado, en la moneda de cotizacion del instrumento."""
    signo = 1 if op.direccion == "compra" else -1
    return signo * (precio - op.apertura.precio) * op.lotes * contrato


# ------------------------------------------------------------------------- la linea de tiempo

_ORDEN = {"cierre": 0, "cargo": 1, "marca": 2, "apertura": 3}


@dataclass(frozen=True, order=True)
class _Evento:
    instante: datetime
    orden: int
    op_id: str
    secuencia: int
    tipo: str = field(compare=False)
    op: Operacion = field(compare=False)
    precio: Decimal | None = field(compare=False, default=None)
    cargo: Cargo | None = field(compare=False, default=None)


def _eventos(operaciones: Sequence[Operacion]) -> list[_Evento]:
    eventos: list[_Evento] = []
    for op in sorted(operaciones, key=lambda o: (o.apertura.instante, o.id)):
        eventos.append(_Evento(op.apertura.instante, _ORDEN["apertura"], op.id, 0, "apertura", op))
        for i, m in enumerate(op.marcas):
            eventos.append(
                _Evento(m.instante, _ORDEN["marca"], op.id, i + 1, "marca", op, precio=m.precio)
            )
        for i, c in enumerate(op.cargos):
            eventos.append(_Evento(c.instante, _ORDEN["cargo"], op.id, i + 1, "cargo", op, cargo=c))
        eventos.append(
            _Evento(op.cierre.instante, _ORDEN["cierre"], op.id, 0, "cierre", op, op.cierre.precio)
        )
    return sorted(eventos)


def _medianoche(dia: date, huso: ZoneInfo) -> datetime:
    return datetime.combine(dia, time(0), tzinfo=huso).astimezone(UTC)


def _dia_local(instante: datetime, huso: ZoneInfo) -> date:
    return instante.astimezone(huso).date()


# ---------------------------------------------------------------------------------- el estado


@dataclass
class _Cuenta:
    reglas: ReglasFase
    contrato: Decimal
    saldo: Decimal
    saldo_maximo: Decimal
    dia: date
    saldo_corte: Decimal
    limite_dia: Decimal
    limite_total: Decimal
    abiertas: dict[str, tuple[Operacion, Decimal]] = field(default_factory=dict)
    dias_de_trading: set[date] = field(default_factory=set)
    dias: list[DiaDeCuenta] = field(default_factory=list)
    equity_minima_dia: Decimal | None = None
    con_apertura_dia: bool = False

    @property
    def equity(self) -> Decimal:
        flotante = sum(
            (pnl(op, precio, self.contrato) for op, precio in self.abiertas.values()), Decimal(0)
        )
        return self.saldo + flotante

    @property
    def vigilada(self) -> Decimal:
        return self.equity if self.reglas.magnitud_vigilada == MAGNITUD_EQUITY else self.saldo

    def limite_del_dia(self) -> Decimal:
        r = self.reglas
        base = self.saldo_corte if r.base_perdida_diaria == BASE_CORTE else r.capital_inicial
        return base - r.capital_inicial * r.perdida_diaria_max.valor / CIEN

    def limite_del_total(self) -> Decimal:
        r = self.reglas
        base = self.saldo_maximo if r.perdida_total_arrastra else r.capital_inicial
        return base - r.capital_inicial * r.perdida_total_max.valor / CIEN

    def cerrar_dia(self) -> None:
        self.dias.append(
            DiaDeCuenta(
                dia=self.dia,
                saldo_corte=self.saldo_corte,
                limite_dia=self.limite_dia,
                equity_minima=self.equity_minima_dia,
                saldo_final=self.saldo,
                con_apertura=self.con_apertura_dia,
            )
        )

    def cortar(self, dia: date) -> None:
        """La medianoche local: el saldo de ese instante fija el limite del dia nuevo."""
        self.cerrar_dia()
        self.dia = dia
        self.saldo_corte = self.saldo
        self.limite_dia = self.limite_del_dia()
        self.equity_minima_dia = None
        self.con_apertura_dia = False

    def anotar_saldo(self, saldo: Decimal) -> None:
        self.saldo = saldo
        if saldo > self.saldo_maximo:
            self.saldo_maximo = saldo
            self.limite_total = self.limite_del_total()

    def observar(self) -> None:
        e = self.equity
        if self.equity_minima_dia is None or e < self.equity_minima_dia:
            self.equity_minima_dia = e

    def infracciones(self) -> list[str]:
        v = self.vigilada
        motivos: list[str] = []
        if v < self.limite_dia:
            motivos.append(
                f"perdida diaria: {self.reglas.magnitud_vigilada} {v} por debajo del limite "
                f"del dia {self.limite_dia} (saldo al corte {self.saldo_corte})"
            )
        if v < self.limite_total:
            motivos.append(
                f"perdida total: {self.reglas.magnitud_vigilada} {v} por debajo del limite total "
                f"{self.limite_total}"
            )
        return motivos

    def superada(self) -> str | None:
        r = self.reglas
        if r.objetivo is None or self.abiertas:
            return None
        meta = r.capital_inicial * (CIEN + r.objetivo.valor) / CIEN
        if self.saldo < meta:
            return None
        if r.dias_minimos is not None and len(self.dias_de_trading) < r.dias_minimos:
            return None
        dias = (
            f"{len(self.dias_de_trading)} dias de trading"
            if r.dias_minimos is None
            else f"{len(self.dias_de_trading)} dias de trading (minimo {r.dias_minimos})"
        )
        return f"objetivo: saldo {self.saldo} en o sobre {meta} sin posiciones vivas, {dias}"


# ------------------------------------------------------------------------------ la guardia


def guardia_tamano_posicion(operaciones: Sequence[Operacion], reglas: ReglasFase) -> GuardiaTamano:
    """Aviso por una operacion cuyo lote supera `ratio` veces la mediana de los lotes de LAS
    DEMAS. Solo avisa: no cambia ningun estado. Sin cifra en el perfil, no se evalua y se dice."""
    if not reglas.guardia_tamano_aplica:
        return GuardiaTamano("no_aplica", "el perfil no pide coherencia de tamano de posicion")
    if reglas.ratio_aviso_tamano is None:
        return GuardiaTamano(
            "no_evaluable",
            f"{RATIO_AVISO} no tiene valor en el perfil {reglas.perfil}: la firma no da cifra",
        )
    ops = sorted(operaciones, key=lambda o: (o.apertura.instante, o.id))
    if len(ops) < 2:
        return GuardiaTamano("evaluada", "menos de dos operaciones: nada con lo que comparar")
    avisos: list[str] = []
    for op in ops:
        otras = [o.lotes for o in ops if o.id != op.id]
        mediana = median(otras)
        if op.lotes > mediana * reglas.ratio_aviso_tamano:
            avisos.append(
                f"{op.id}: {op.lotes} lotes supera {reglas.ratio_aviso_tamano} veces la mediana "
                f"{mediana} de las demas"
            )
    return GuardiaTamano(
        "evaluada",
        f"ratio {reglas.ratio_aviso_tamano} sobre la mediana de las demas operaciones",
        tuple(avisos),
    )


# ------------------------------------------------------------------------------- el motor


def evaluar_fase(
    operaciones: Sequence[Operacion], reglas: ReglasFase, contrato: Decimal
) -> ResultadoFase:
    """Corre UNA fase desde el capital inicial sobre la secuencia de operaciones. Pura y
    determinista: el orden de entrada no importa, la linea de tiempo se ordena por instante."""
    ids = [op.id for op in operaciones]
    if len(set(ids)) != len(ids):
        raise OperacionError(f"ids de operacion repetidos: {sorted(ids)}")
    for op in operaciones:
        comprobar_operacion(op)
    if contrato <= 0:
        raise OperacionError(f"contrato no positivo ({contrato})")
    guardia = guardia_tamano_posicion(operaciones, reglas)
    eventos = _eventos(operaciones)
    if not eventos:
        return ResultadoFase(
            perfil=reglas.perfil,
            fase=reglas.fase,
            estado=EstadoCuenta.EN_CURSO,
            motivo="sin operaciones",
            instante=None,
            saldo_final=reglas.capital_inicial,
            equity_final=reglas.capital_inicial,
            limite_total_final=reglas.capital_inicial
            - reglas.capital_inicial * reglas.perdida_total_max.valor / CIEN,
            dias_de_trading=0,
            dias=(),
            guardia_tamano=guardia,
            operaciones_evaluadas=0,
            operaciones_tras_el_final=0,
        )
    huso = reglas.huso_corte
    primer_dia = _dia_local(eventos[0].instante, huso)
    cuenta = _Cuenta(
        reglas=reglas,
        contrato=contrato,
        saldo=reglas.capital_inicial,
        saldo_maximo=reglas.capital_inicial,
        dia=primer_dia,
        saldo_corte=reglas.capital_inicial,
        limite_dia=Decimal(0),
        limite_total=Decimal(0),
    )
    # el primer dia: el saldo del corte es el capital inicial (R2, «On the first day of trading»)
    cuenta.limite_dia = cuenta.limite_del_dia()
    cuenta.limite_total = cuenta.limite_del_total()

    estado = EstadoCuenta.EN_CURSO
    motivo = "sin objetivo alcanzado ni limite infringido"
    instante_final: datetime | None = None
    evaluadas: set[str] = set()
    tras_el_final: set[str] = set()

    for ev in eventos:
        if estado is not EstadoCuenta.EN_CURSO:
            tras_el_final.add(ev.op_id)
            continue
        # los cortes de medianoche local que quedan ANTES de este evento, incluido su instante
        siguiente = cuenta.dia + timedelta(days=1)
        while _medianoche(siguiente, huso) <= ev.instante:
            cuenta.cortar(siguiente)
            siguiente = cuenta.dia + timedelta(days=1)
        evaluadas.add(ev.op_id)
        if ev.tipo == "apertura":
            cuenta.abiertas[ev.op_id] = (ev.op, ev.op.apertura.precio)
            cuenta.dias_de_trading.add(cuenta.dia)
            cuenta.con_apertura_dia = True
        elif ev.tipo == "marca":
            assert ev.precio is not None
            cuenta.abiertas[ev.op_id] = (ev.op, ev.precio)
        elif ev.tipo == "cargo":
            assert ev.cargo is not None
            cuenta.anotar_saldo(cuenta.saldo - ev.cargo.importe)
        else:  # cierre
            assert ev.precio is not None
            realizado = pnl(ev.op, ev.precio, contrato)
            del cuenta.abiertas[ev.op_id]
            cuenta.anotar_saldo(cuenta.saldo + realizado)
        cuenta.observar()
        infracciones = cuenta.infracciones()
        if infracciones:
            estado = EstadoCuenta.SUSPENDIDA
            motivo = "; ".join(infracciones) + f" [{ev.tipo} de {ev.op_id}]"
            instante_final = ev.instante
            continue
        if ev.tipo == "cierre":
            logro = cuenta.superada()
            if logro is not None:
                estado = EstadoCuenta.SUPERADA
                motivo = f"{logro} [cierre de {ev.op_id}]"
                instante_final = ev.instante
    cuenta.cerrar_dia()
    return ResultadoFase(
        perfil=reglas.perfil,
        fase=reglas.fase,
        estado=estado,
        motivo=motivo,
        instante=instante_final,
        saldo_final=cuenta.saldo,
        equity_final=cuenta.equity,
        limite_total_final=cuenta.limite_total,
        dias_de_trading=len(cuenta.dias_de_trading),
        dias=tuple(cuenta.dias),
        guardia_tamano=guardia,
        operaciones_evaluadas=len(evaluadas),
        operaciones_tras_el_final=len(tras_el_final - evaluadas),
    )
