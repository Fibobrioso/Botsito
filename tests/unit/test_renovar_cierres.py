"""El calendario de cierres caduca por la FECHA SIMULADA, nunca por la de hoy (rama
`trabajo/renovar-cierres`, decisiones del consultor del 2026-10-03, puntos 2 y 3).

- El cable trampa, permanente: con el reloj de pared saboteado -leerlo lanza una excepcion-, cargar
  el calendario real y simular un dia fijo por el motor cableado pasa. Una variante del predicado
  que lee el reloj, rota a proposito, falla.
- Simular un dia posterior a `hasta` se niega: `motor arnes --simular` sale con 2 y nombra el dia.
  Por la CLI de verdad, con el calendario recortado y sin `data/` (las velas no se leen y el
  mercado de cada dia es sintetico), asi corre tambien en la CI. La construccion del motor y la
  comprobacion de `cubre` son las de verdad.

La excepcion: `logging` lee `time.time` para fechar cada registro (medido con el cable trampa en
docs/validation/RENOVAR-CIERRES.md §0.1). Fecha el log; no decide nada, y se le deja.
"""

from __future__ import annotations

import re
import sys
import time
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import pytest

from botsito import cli
from botsito.domain import cierres as dominio_cierres
from botsito.domain.cierres import (
    MOTIVO_CIERRE,
    MOTIVO_SIN_CALENDARIO,
    CalendarioCierres,
    ReglasCierres,
)
from botsito.domain.ticks import MS_POR_MINUTO
from botsito.domain.velas import MinutoUtc
from botsito.engine import arnes as modulo_arnes
from botsito.engine import broker as modulo_broker
from botsito.engine import cableado, calendario_cierres, simulacion
from botsito.engine.broker import PETICION_COLOCAR
from botsito.engine.simulacion import MercadoDia
from tests.unit import test_cableado as tc
from tests.unit import test_cierres_de_mercado as tcm

RAIZ = Path(__file__).resolve().parents[2]
PERFIL = "ftmo-2step-swing-100k"
_TIME_REAL = time.time


class RelojLeidoError(AssertionError):
    """Alguien leyo el reloj de pared."""


def _prohibido(*_a: object, **_k: object) -> Any:
    raise RelojLeidoError("los cierres leyeron el reloj de pared")


def _time_saboteado() -> float:
    if sys._getframe(1).f_globals.get("__name__") == "logging":
        return _TIME_REAL()  # la hora del registro del log (ver arriba)
    _prohibido()
    return 0.0


class _DateTimeSaboteado(datetime):
    @classmethod
    def now(cls, tz: Any = None) -> Any:
        _prohibido()

    @classmethod
    def utcnow(cls) -> Any:
        _prohibido()

    @classmethod
    def today(cls) -> Any:
        _prohibido()


class _DateSaboteado(date):
    @classmethod
    def today(cls) -> Any:
        _prohibido()


def _sabotear_reloj(monkeypatch: pytest.MonkeyPatch) -> None:
    """El reloj de pared, saboteado en todos los modulos por los que pasan los cierres."""
    for modulo in (dominio_cierres, calendario_cierres, modulo_broker, cableado, simulacion):
        if hasattr(modulo, "datetime"):
            monkeypatch.setattr(modulo, "datetime", _DateTimeSaboteado)
        if hasattr(modulo, "date"):
            monkeypatch.setattr(modulo, "date", _DateSaboteado)
    monkeypatch.setattr(time, "time", _time_saboteado)
    monkeypatch.setattr(time, "time_ns", _prohibido)
    monkeypatch.setattr(time, "localtime", _prohibido)
    # `gmtime()` sin argumento es la hora de hoy; con un instante, solo lo convierte (revisor, a1).
    # `monotonic` y `perf_counter` miden intervalos y no dan una fecha: no deciden un dia
    gmtime_real = time.gmtime
    monkeypatch.setattr(
        time, "gmtime", lambda *a: _prohibido() if not a or a[0] is None else gmtime_real(*a)
    )


def _simular_dia_con_cierre() -> cableado.MotorCableado:
    """El dia sintetico de `test_cableado` por el motor cableado, con una ventana de cierre abierta
    antes de que la limite se coloque: la colocacion se niega por el predicado."""
    base = tcm._corrida(None)
    colocada = base.brokers[tc.DIA.isoformat()].ordenes["o1"].colocada_ms
    return tcm._corrida(tcm._cierres_con_ventana_en(colocada - 60_000))


def test_con_el_reloj_saboteado_el_calendario_y_el_dia_simulado_salen(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _sabotear_reloj(monkeypatch)
    cal = calendario_cierres.cargar_calendario(
        calendario_cierres.ruta_calendario(RAIZ, PERFIL)
    ).calendario()
    assert cal.cubre_hasta_ms > cal.cubre_desde_ms
    # el dia sintetico (2030) con el calendario REAL: cae fuera de lo que cubre y se niega por la
    # fecha simulada (revisor, a3)
    real = tcm._corrida(ReglasCierres(cal, tcm.MARGEN, tcm.MINIMO, True))
    tb_real = real.trazas_broker[tc.DIA.isoformat()]
    assert tb_real.cierres and {c.motivo for c in tb_real.cierres} == {MOTIVO_SIN_CALENDARIO}
    # y con una ventana de cierre abierta antes de colocar: se niega por el predicado
    motor = _simular_dia_con_cierre()
    tb = motor.trazas_broker[tc.DIA.isoformat()]
    assert (tb.cierres[0].tipo, tb.cierres[0].motivo) == (PETICION_COLOCAR, MOTIVO_CIERRE)
    with pytest.raises(RelojLeidoError):  # el sabotaje esta puesto: leerlo falla
        vars(modulo_broker)["datetime"].now(UTC)


def test_un_predicado_que_lee_el_reloj_lo_caza_el_sabotaje(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """La guardia rota a proposito: una variante del predicado que mira la hora de hoy."""
    original = dominio_cierres.ventana_prohibida_por_cierre

    def lee_el_reloj(*a: Any, **k: Any) -> Any:
        vars(modulo_broker)["datetime"].now(UTC)
        return original(*a, **k)

    monkeypatch.setattr(modulo_broker, "ventana_prohibida_por_cierre", lee_el_reloj)
    _sabotear_reloj(monkeypatch)
    with pytest.raises(RelojLeidoError):
        _simular_dia_con_cierre()


# ------------------------------------------- un dia posterior a `hasta`: exit 2 y el dia nombrado

FIN_CORTO = datetime(2026, 4, 2, 4, 0, tzinfo=UTC)  # `hasta` = 2026-04-01 en Nueva York (EDT)


_CALENDARIO_DEL_PERFIL = cableado.calendario_del_perfil  # el de verdad, antes de sustituirlo


def _calendario_corto(repo: Path, perfil: str) -> CalendarioCierres:
    real = _CALENDARIO_DEL_PERFIL(repo, perfil)
    fin = int(FIN_CORTO.timestamp() * 1000)
    return CalendarioCierres(
        tuple(c for c in real.cierres if c.inicio_ms < fin), real.cubre_desde_ms, fin
    )


def _mercado_sintetico(*args: Any) -> MercadoDia:
    """El mercado de un dia sin leer `data/`: solo sus limites (05:00 a 13:00 UTC, verano)."""
    caso = str(args[-1])
    m = re.search(r"\d{4}-\d{2}-\d{2}", caso)
    assert m is not None, caso
    dia = date.fromisoformat(m.group(0))
    inicio = int(datetime(dia.year, dia.month, dia.day, 5, tzinfo=UTC).timestamp() * 1000)
    return MercadoDia(
        caso, dia, MinutoUtc(inicio // MS_POR_MINUTO),
        MinutoUtc(inicio // MS_POR_MINUTO + 8 * 60), 100_000, (), (), (), (),
    )  # fmt: skip


def test_simular_un_dia_posterior_a_hasta_sale_con_2_y_lo_nombra(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(cableado, "calendario_del_perfil", _calendario_corto)
    monkeypatch.setattr(cableado, "mercado_de_construccion", _mercado_sintetico)
    # las velas que el arnes lee antes de construir el motor: sin `data/` en la CI, y aqui no
    # llegan a usarse, porque la construccion se niega antes
    monkeypatch.setattr(modulo_arnes, "dias_de_mercado", lambda *_a, **_k: {})
    r = cli.main(
        [
            "--repo", str(RAIZ), "motor", "arnes", "--simular", "--meses", "2026-04",
            "--diagnostico-a35", "cierre_vela_contraria", "--diagnostico-a44", "sin_tope",
            "--diagnostico-a21", "solo_una_zona_de_control",
            "--salida", str(tmp_path / "arnes.txt"),
        ]
    )  # fmt: skip
    err = capsys.readouterr().err
    assert r == 2, err
    assert "dias fuera del calendario de cierres" in err
    assert "'2026-04-02'" in err and "'2026-04-01'" not in err
    assert not list(tmp_path.iterdir())  # no escribe nada
