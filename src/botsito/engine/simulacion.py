"""La simulacion de punta a punta (ADR-0052 §4, PROPUESTO): mercado de un dia -> estrategia ->
broker -> capa de cuenta -> veredicto de la firma.

Une lo que ya existe sin cablear el motor de reglas: el `Mercado` de un dia de CONSTRUCCION (ticks
donde los hay, M1 de respaldo donde no), una `Estrategia` -cualquier cosa que decida minuto a
minuto sobre un `Broker`- y `cuenta.evaluar_fase` sobre las operaciones cerradas. La estrategia
real (el interprete de la spec) NO esta enchufada aqui: el contrato que tendra que cumplir es el
de `Estrategia`, y ADR-0052 §5 lo deja escrito.

SOLO CONSTRUCCION Y POR LA COMPUERTA: el dia sale de `visor.caso_de_construccion`, que valida el
mes contra el criterio y cruza el reparto con los ocultos antes de leer nada. Los datasets de
ticks se buscan por mes; si no hay ninguno, todo el dia es respaldo M1 y queda marcado.

SIN MIRAR AL FUTURO: la estrategia decide al CIERRE de cada M1 y solo ve las velas cerradas hasta
ese minuto; el broker procesa los eventos hasta ese mismo instante antes de dejarle decidir.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, replace
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Protocol

from botsito.cases.criterio_fidelidad import Criterio
from botsito.cases.paquete import Config
from botsito.config.registro import Registro
from botsito.data.dataset import DatasetError, buscar_manifiesto, cargar_manifiesto, cargar_ventana
from botsito.data.ticks import (
    TicksError,
    cargar_manifiesto_ticks,
    cargar_ticks,
    manifiestos_ticks,
)
from botsito.domain.ticks import MS_POR_MINUTO, Tick
from botsito.domain.velas import MinutoUtc, Vela
from botsito.engine.arnes import DiaTrader
from botsito.engine.broker import Broker, ReglasBroker
from botsito.engine.cuenta import Operacion, ReglasFase, ResultadoFase, evaluar_fase
from botsito.engine.llenado import Configuracion, Mercado
from botsito.engine.perfil_cuenta import PerfilCuenta
from botsito.engine.visor import _minuto_local, caso_de_construccion


@dataclass(frozen=True)
class MercadoDia:
    """El mercado de UN dia de construccion, ya leido: el broker no toca ficheros."""

    caso: str
    dia: date
    desde: MinutoUtc  # primer minuto de la ventana del dia
    hasta: MinutoUtc  # primer minuto que ya no pertenece a la ventana
    escala: int
    m1: tuple[Vela, ...]
    ticks: tuple[Tick, ...]
    origen_ticks: tuple[str, ...]  # datasets de ticks usados (vacio = todo respaldo)
    horas_perdidas: tuple[str, ...]
    operaciones_trader: tuple[Operacion, ...] | None = None  # las del caso, si se piden

    @property
    def desde_ms(self) -> int:
        return int(self.desde) * MS_POR_MINUTO

    @property
    def hasta_ms(self) -> int:
        return int(self.hasta) * MS_POR_MINUTO

    def mercado(self) -> Mercado:
        return Mercado(self.ticks, self.m1)

    def minutos_con_ticks(self) -> int:
        return len({int(t.minuto) for t in self.ticks})


class Estrategia(Protocol):
    """El contrato que el motor de reglas tendra que cumplir (ADR-0052 §5): decidir al cierre de
    cada M1 con lo que el broker le deja hacer -colocar, modificar, cancelar, cerrar a mercado- y
    leer sus hechos de origen broker."""

    def decidir(self, broker: Broker, minuto: MinutoUtc, cerradas: Sequence[Vela]) -> None: ...

    def al_cerrar_la_ventana(self, broker: Broker, instante_ms: int) -> None: ...


def reglas_broker_de(perfil: PerfilCuenta) -> ReglasBroker:
    """Los limites y los costes del perfil de cuenta, leidos por su nombre (ADR-0050)."""
    return ReglasBroker(
        volumen_max_lotes=perfil.lotes("firma_volumen_max_lotes"),
        ordenes_simultaneas_max=perfil.entero("firma_ordenes_simultaneas_max"),
        posiciones_dia_max=perfil.entero("firma_posiciones_dia_max"),
        huso_corte=perfil.huso_corte(),
        comision_por_lote=perfil.decimal("firma_comision_usd_por_lote"),
        comision_por_lado=perfil.booleano("firma_comision_por_lado"),
        swap_largo_puntos=perfil.decimal("firma_swap_largo_puntos"),
        swap_corto_puntos=perfil.decimal("firma_swap_corto_puntos"),
    )


def _ticks_del_dia(
    repo: Path, carpeta_datos: Path, desde_ms: int, hasta_ms: int
) -> tuple[tuple[Tick, ...], tuple[str, ...], tuple[str, ...]]:
    ticks: list[Tick] = []
    origenes: list[str] = []
    perdidas: list[str] = []
    for ruta in manifiestos_ticks(repo):
        m = cargar_manifiesto_ticks(ruta)
        serie = cargar_ticks(m, carpeta_datos, desde_ms, hasta_ms)
        if serie.ticks:
            ticks.extend(serie.ticks)
            origenes.append(serie.origen)
            perdidas.extend(serie.horas_perdidas)
    ticks.sort(key=lambda t: t.instante)
    return tuple(ticks), tuple(origenes), tuple(sorted(set(perdidas)))


def mercado_de_construccion(
    repo: Path,
    carpeta_datos: Path,
    criterio: Criterio,
    config: Config,
    registro: Registro,
    caso: str,
    *,
    con_operaciones_del_trader: bool = False,
) -> MercadoDia:
    """El mercado de un dia dev de construccion, por la compuerta del arnes."""
    dt: DiaTrader = caso_de_construccion(repo, criterio, caso)
    dia = date.fromisoformat(dt.dia)
    huso = registro.texto("huso_operativa")
    desde = _minuto_local(dia, config.ventana_local[0], huso)
    hasta = _minuto_local(dia, config.ventana_local[1], huso)
    try:
        ruta = buscar_manifiesto(repo, f"{config.dataset_prefijo}{dt.dia[:7]}")
    except DatasetError as exc:
        raise TicksError(f"{caso}: sin dataset M1 de su mes ({exc})") from exc
    serie = cargar_ventana(cargar_manifiesto(ruta), carpeta_datos, desde, hasta)
    ticks, origenes, perdidas = _ticks_del_dia(
        repo, carpeta_datos, int(desde) * MS_POR_MINUTO, int(hasta) * MS_POR_MINUTO
    )
    return MercadoDia(
        caso=dt.id,
        dia=dia,
        desde=desde,
        hasta=hasta,
        escala=serie.escala,
        m1=tuple(serie.velas),
        ticks=ticks,
        origen_ticks=origenes,
        horas_perdidas=perdidas,
        operaciones_trader=None if not con_operaciones_del_trader else _del_trader(repo, dt),
    )


def _del_trader(repo: Path, dt: DiaTrader) -> tuple[Operacion, ...]:
    """Las operaciones del caso como `cuenta.Operacion` SIN cierre real: el caso no lo trae. El
    cierre lo pone quien las repita por el broker (Fase 6), y lo dice."""
    from botsito.engine.cuenta import Marca
    from botsito.engine.visor import _stops

    salida: list[Operacion] = []
    for op, stop in zip(dt.operaciones, _stops(repo, dt), strict=True):
        salida.append(
            Operacion(
                id=f"{dt.id}-{len(salida) + 1}",
                direccion=op.direccion,  # type: ignore[arg-type]  # compra | venta, validado al ingerir
                lotes=Decimal(0),  # sin lote en el caso: lo pone el escenario
                apertura=Marca(op.instante, op.entrada),
                cierre=Marca(op.instante, op.entrada),  # sin salida en el caso
                cargos=(),
                marcas=(Marca(op.instante, stop),) if stop is not None else (),
            )
        )
    return tuple(salida)


def simular_dia(
    md: MercadoDia,
    estrategia: Estrategia,
    reglas: ReglasBroker,
    config: Configuracion,
    contrato: Decimal,
) -> Broker:
    """Un dia: al cierre de cada M1 de la ventana, el broker procesa hasta ese instante y la
    estrategia decide con las velas cerradas; al cerrar la ventana, la estrategia recoge."""
    broker = Broker(reglas, config, md.mercado(), contrato, md.escala)
    cerradas: list[Vela] = []
    velas = {int(v.inicio): v for v in md.m1}
    for m in range(int(md.desde), int(md.hasta)):
        fin_ms = (m + 1) * MS_POR_MINUTO - 1
        broker.avanzar(fin_ms)
        v = velas.get(m)
        if v is not None:
            cerradas.append(v)
        estrategia.decidir(broker, MinutoUtc(m), cerradas)
    # el ultimo milisegundo de la ventana: el minuto de `hasta` ya no pertenece al dia y no tiene
    # M1 cargada, asi que un cierre a mercado ahi no tendria precio
    broker.avanzar(md.hasta_ms - 1)
    estrategia.al_cerrar_la_ventana(broker, md.hasta_ms - 1)
    return broker


@dataclass(frozen=True)
class ResultadoSimulacion:
    fase: ResultadoFase
    brokers: Mapping[str, Broker]
    por_fuente: Mapping[str, int]
    rechazos: int


def simular_fase(
    dias: Sequence[MercadoDia],
    estrategia_de: Callable[[MercadoDia], Estrategia],
    reglas: ReglasBroker,
    config: Configuracion,
    contrato: Decimal,
    reglas_fase: ReglasFase,
) -> ResultadoSimulacion:
    """Varios dias, en orden, con la cuenta persistiendo entre ellos (ADR-0049 H6, ADR-0050)."""
    brokers: dict[str, Broker] = {}
    operaciones: list[Operacion] = []
    por_fuente: dict[str, int] = {}
    rechazos = 0
    for md in sorted(dias, key=lambda d: (d.dia, d.caso)):
        b = simular_dia(md, estrategia_de(md), reglas, config, contrato)
        brokers[md.caso] = b
        # el id de la posicion es del dia; entre dias se prefija con el caso para que la cuenta
        # -que exige ids unicos- los distinga
        operaciones.extend(replace(op, id=f"{md.caso}/{op.id}") for op in b.operaciones_cerradas())
        for fuente, n in b.traza().por_fuente().items():
            por_fuente[fuente] = por_fuente.get(fuente, 0) + n
        rechazos += len(b.traza().rechazos)
    fase = evaluar_fase(operaciones, reglas_fase, contrato)
    return ResultadoSimulacion(fase, brokers, por_fuente, rechazos)


__all__ = [
    "Estrategia",
    "MercadoDia",
    "ResultadoSimulacion",
    "mercado_de_construccion",
    "reglas_broker_de",
    "simular_dia",
    "simular_fase",
]
