"""Punta a punta con una estrategia SINTETICA (Fase 5, ADR-0052 §4): mercado -> estrategia ->
broker -> llenado -> capa de cuenta -> veredicto. La estrategia de juguete vive AQUI, fuera de
src, y esta marcada como sintetica. Dias sinteticos de 2030 con ticks en zigzag; y, si hay datos
y un dataset de ticks en la maquina, un dia dev de construccion real por la compuerta."""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from decimal import Decimal
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from botsito.data.velas import a_minuto
from botsito.domain.ticks import MS_POR_MINUTO, MilisegundoUtc, Tick
from botsito.domain.valores import Porcentaje, Puntos
from botsito.domain.velas import MinutoUtc, Vela
from botsito.engine import simulacion
from botsito.engine.broker import Broker, ReglasBroker
from botsito.engine.cuenta import EstadoCuenta, ReglasFase
from botsito.engine.llenado import RESPALDO_M1, TICKS, Configuracion
from botsito.engine.simulacion import MercadoDia, simular_dia, simular_fase

RAIZ = Path(__file__).resolve().parents[2]
HUSO = ZoneInfo("Europe/Madrid")
SPREAD = 3
UNO = Decimal(1)
ESCALA = 1  # contrato 1 y escala 1: el P/L es la diferencia de puntos por lote


def _reglas_broker() -> ReglasBroker:
    return ReglasBroker(Decimal(100), 200, 2000, HUSO, Decimal(0), True, Decimal(0), Decimal(0))


def _reglas_fase(
    capital: int, diaria: int, total: int, objetivo: int | None, dias: int | None
) -> ReglasFase:
    return ReglasFase(
        "sintetico", "unica", Decimal(capital), HUSO, Porcentaje(diaria), "saldo_corte_diario",
        Porcentaje(total), False, "equity", Porcentaje(objetivo) if objetivo is not None else None,
        dias, False, None,
    )  # fmt: skip


def _cfg() -> Configuracion:
    return Configuracion(False, 0, lambda _m: SPREAD)


def _dia_sintetico(dia: date, base: int, pendiente: int, con_ticks: bool = True) -> MercadoDia:
    """Ventana 07:00-15:00 Madrid (05:00-13:00Z en verano; en enero 06:00-14:00Z). El BID sube
    `pendiente` puntos por minuto en zigzag; ticks cada 20 s si `con_ticks`."""
    desde = a_minuto(datetime(dia.year, dia.month, dia.day, 7, 0, tzinfo=HUSO))
    hasta = a_minuto(datetime(dia.year, dia.month, dia.day, 15, 0, tzinfo=HUSO))
    m1: list[Vela] = []
    ticks: list[Tick] = []
    for i, m in enumerate(range(int(desde), int(hasta))):
        centro = base + pendiente * i
        o, c = centro - 2, centro + 2
        zig = int(4 * math.sin(i / 7))
        m1.append(
            Vela(
                MinutoUtc(m),
                Puntos(o),
                Puntos(max(o, c) + 5 + abs(zig)),
                Puntos(min(o, c) - 5 - abs(zig)),
                Puntos(c),
                1,
            )
        )
        if con_ticks:
            for k, seg in enumerate((0, 20, 40)):
                bid = centro + (-5 - abs(zig), zig, 5 + abs(zig))[k]
                ticks.append(
                    Tick(
                        MilisegundoUtc(m * MS_POR_MINUTO + seg * 1000),
                        Puntos(bid + SPREAD),
                        Puntos(bid),
                        0,
                        0,
                    )
                )
    return MercadoDia(
        f"caso-x-{dia.isoformat()}",
        dia,
        desde,
        hasta,
        ESCALA,
        tuple(m1),
        tuple(ticks),
        ("sintetico",) if con_ticks else (),
        (),
    )


# ---------------------------------------------------------------------- la estrategia sintetica


@dataclass
class EstrategiaSintetica:
    """SINTETICA, solo para los tests. A los `minuto_entrada` minutos de la ventana coloca una
    limite al ultimo cierre menos `descuento` con stop y objetivo a distancias fijas; al cerrar la
    ventana cierra a mercado lo que quede vivo. No sabe nada de la spec."""

    lado: str
    minuto_entrada: int
    descuento: int
    stop_puntos: int
    objetivo_puntos: int
    lotes: Decimal = UNO
    colocadas: int = field(default=0)

    def decidir(self, broker: Broker, minuto: MinutoUtc, cerradas: Sequence[Vela]) -> None:
        if len(cerradas) == self.minuto_entrada and self.colocadas == 0:
            ultimo = int(cerradas[-1].cierre)
            if self.lado == "compra":
                precio = ultimo - self.descuento
                broker.colocar_limite(
                    "s1",
                    "compra",
                    precio,
                    self.lotes,
                    precio - self.stop_puntos,
                    precio + self.objetivo_puntos,
                    (int(minuto) + 1) * MS_POR_MINUTO - 1,
                )
            else:
                precio = ultimo + self.descuento
                broker.colocar_limite(
                    "s1",
                    "venta",
                    precio,
                    self.lotes,
                    precio + self.stop_puntos,
                    precio - self.objetivo_puntos,
                    (int(minuto) + 1) * MS_POR_MINUTO - 1,
                )
            self.colocadas += 1

    def al_cerrar_la_ventana(self, broker: Broker, instante_ms: int) -> None:
        for p in list(broker.posiciones.values()):
            if p.abierta:
                broker.cerrar_a_mercado(p.id, instante_ms)
        for o in list(broker.ordenes.values()):
            if o.estado in ("colocada", "modificada"):
                broker.cancelar(o.id, instante_ms)


def _pierde_siempre(md: MercadoDia) -> EstrategiaSintetica:
    # vende contra una tendencia alcista: el stop salta
    return EstrategiaSintetica("venta", 10, 3, 40, 400, lotes=Decimal(50))


def _gana_poco(md: MercadoDia) -> EstrategiaSintetica:
    # compra a favor de la tendencia con objetivo corto: gana unos puntos
    return EstrategiaSintetica("compra", 10, 3, 400, 30, lotes=Decimal(2))


# -------------------------------------------------------------------------------- los tests


def test_determinismo_de_punta_a_punta() -> None:
    dias = [
        _dia_sintetico(date(2030, 1, 15), 100_000, 1),
        _dia_sintetico(date(2030, 1, 16), 100_500, 1),
    ]
    reglas = _reglas_fase(10_000, 5, 10, 8, 4)
    uno = simular_fase(dias, _gana_poco, _reglas_broker(), _cfg(), UNO, reglas)
    dos = simular_fase(dias, _gana_poco, _reglas_broker(), _cfg(), UNO, reglas)
    assert uno.fase == dos.fase and uno.por_fuente == dos.por_fuente
    assert uno.fase.operaciones_evaluadas == 2 and uno.por_fuente[TICKS] > 0


def test_sin_mirar_al_futuro() -> None:
    """La decision del minuto k solo ve k velas cerradas, y lo que el broker hizo hasta un instante
    no cambia si se recortan los ticks posteriores."""
    md = _dia_sintetico(date(2030, 1, 15), 100_000, 1)
    vistas: list[int] = []

    class Espia(EstrategiaSintetica):
        def decidir(self, broker: Broker, minuto: MinutoUtc, cerradas: Sequence[Vela]) -> None:
            vistas.append(len(cerradas))
            assert all(int(v.fin) <= int(minuto) + 1 for v in cerradas)
            super().decidir(broker, minuto, cerradas)

    b = simular_dia(md, Espia("compra", 10, 3, 400, 30), _reglas_broker(), _cfg(), UNO)
    assert vistas == list(range(1, int(md.hasta) - int(md.desde) + 1))
    llenada = next(e for e in b.traza().eventos if e[1] == "llenada")
    recortado = MercadoDia(
        **{
            **md.__dict__,
            "ticks": tuple(t for t in md.ticks if t.instante <= llenada[0]),
            "m1": tuple(
                v for v in md.m1 if int(v.fin) * MS_POR_MINUTO <= llenada[0] + MS_POR_MINUTO
            ),
        }
    )
    b2 = Broker(_reglas_broker(), _cfg(), recortado.mercado(), UNO, ESCALA)
    e = EstrategiaSintetica("compra", 10, 3, 400, 30)
    cerradas: list[Vela] = []
    velas = {int(v.inicio): v for v in recortado.m1}
    for m in range(int(md.desde), llenada[0] // MS_POR_MINUTO + 1):
        b2.avanzar((m + 1) * MS_POR_MINUTO - 1)
        if m in velas:
            cerradas.append(velas[m])
        e.decidir(b2, MinutoUtc(m), cerradas)
    assert [x for x in b2.traza().eventos if x[1] == "llenada"] == [llenada]


def test_una_estrategia_que_pierde_siempre_acaba_suspendida_en_el_instante_exacto() -> None:
    """Vende 50 lotes contra una tendencia alcista con el stop a 40 puntos: cada dia pierde
    ~2.000 sobre 10.000. Con un limite diario del 5 % y total del 10 %, la suspension llega en el
    primer dia, en el instante de la marca o del stop que cruza 9.500."""
    dias = [_dia_sintetico(date(2030, 1, 15 + i), 100_000, 1) for i in range(3)]
    r = simular_fase(
        dias, _pierde_siempre, _reglas_broker(), _cfg(), UNO, _reglas_fase(10_000, 5, 10, 8, 4)
    )
    assert r.fase.estado is EstadoCuenta.SUSPENDIDA
    assert r.fase.instante is not None and r.fase.instante.date() == date(2030, 1, 15)
    b = r.brokers["caso-x-2030-01-15"]
    stop = next(e for e in b.traza().eventos if e[1] == "stop")
    # la suspension no llega despues del stop del primer dia: la marca que cruza el limite es
    # esa o una anterior
    assert r.fase.instante <= datetime.fromtimestamp(stop[0] / 1000, UTC)
    assert "perdida diaria" in r.fase.motivo


def test_una_que_gana_poco_sin_los_dias_minimos_queda_en_curso() -> None:
    dias = [_dia_sintetico(date(2030, 1, 15 + i), 100_000 + 700 * i, 1) for i in range(2)]
    r = simular_fase(
        dias, _gana_poco, _reglas_broker(), _cfg(), UNO, _reglas_fase(10_000, 5, 10, 8, 4)
    )
    assert r.fase.estado is EstadoCuenta.EN_CURSO
    assert r.fase.saldo_final > Decimal(10_000) and r.fase.dias_de_trading == 2
    assert r.rechazos == 0


def test_un_dia_sin_ticks_va_entero_por_el_respaldo_y_queda_marcado() -> None:
    md = _dia_sintetico(date(2030, 1, 15), 100_000, 1, con_ticks=False)
    b = simular_dia(md, _gana_poco(md), _reglas_broker(), _cfg(), UNO)
    fuentes = b.traza().por_fuente()
    assert fuentes[TICKS] == 0 and fuentes[RESPALDO_M1] >= 2
    assert md.minutos_con_ticks() == 0 and md.origen_ticks == ()


def test_un_dia_dev_de_construccion_real_por_la_compuerta_si_hay_datos() -> None:
    from botsito.cases import visto
    from botsito.cases.criterio_fidelidad import cargar_criterio
    from botsito.cases.paquete import cargar_config
    from botsito.config.ajustes import carpeta_datos
    from botsito.config.registro import cargar_registro
    from botsito.data.dataset import DatasetError

    criterio = cargar_criterio(RAIZ)
    mes = criterio.construccion[0]
    if mes not in visto.artefactos(RAIZ):
        pytest.skip("sin reparto dev-visto")
    caso = sorted(c for c, p in visto.asignacion(RAIZ, mes).items() if p == "dev")[0]
    registro = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
    config = cargar_config(RAIZ / "knowledge" / "cases" / "kit" / "config.yaml")
    try:
        md = simulacion.mercado_de_construccion(
            RAIZ,
            carpeta_datos(RAIZ),
            criterio,
            config,
            registro,
            caso,
            con_operaciones_del_trader=True,
        )
    except (DatasetError, Exception) as exc:  # noqa: BLE001
        if "falta en disco" in str(exc) or "sin dataset" in str(exc):
            pytest.skip("sin datos en esta maquina")
        raise
    assert md.m1 and md.desde < md.hasta
    b = simular_dia(
        md, EstrategiaSintetica("compra", 30, 20, 100, 300), _reglas_broker(), _cfg(), Decimal(1)
    )
    assert b.ahora_ms == md.hasta_ms
    assert md.operaciones_trader is not None
