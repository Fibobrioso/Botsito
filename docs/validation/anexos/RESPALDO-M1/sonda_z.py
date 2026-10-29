"""Fase 0 de trabajo/respaldo-m1, a) (RESPALDO-M1.md §0.a): seis sondas con velas y ticks
SINTETICOS de 2030. Se corrieron el 2026-10-29 sobre el codigo de `main` (0e021bf, igual a la rama
en `src/` antes de la fase 1); con el de la rama, las sondas 1 a 3 ya no dan lo de §0.a (es Z
corregido) y las 4 a 6 si, porque `cotizacion`, `_precio_de_mercado`, `precio_de_conversion` y
`_peor_del_minuto` no cambian. La 5 es la de `_peor_del_minuto` (la marca de la vela siguiente al
avanzar hasta un instante redondo) que la Next Action H y R3.6 heredan (respuesta del consultor a
la PARADA, punto 2). No lee datos ni escribe nada.

    uv run python -B docs/validation/anexos/RESPALDO-M1/sonda_z.py
"""

from __future__ import annotations

import dataclasses
from datetime import UTC, datetime
from decimal import Decimal
from zoneinfo import ZoneInfo

from botsito.data.velas import a_minuto
from botsito.domain.ticks import MS_POR_MINUTO, MilisegundoUtc, Tick
from botsito.domain.valores import Puntos
from botsito.domain.velas import MinutoUtc, Vela
from botsito.engine.broker import Broker, ReglasBroker
from botsito.engine.llenado import Configuracion, Mercado

SPREAD = 3
UNO = Decimal(1)
M0 = int(a_minuto(datetime(2030, 1, 15, 8, 0, tzinfo=UTC)))


def ms(m: int, s: int = 0) -> int:
    return m * MS_POR_MINUTO + s * 1000


def vela(m: int, o: int, h: int, low: int, c: int) -> Vela:
    return Vela(MinutoUtc(m), Puntos(o), Puntos(h), Puntos(low), Puntos(c), 1)


def tick(m: int, s: int, bid: int) -> Tick:
    return Tick(MilisegundoUtc(ms(m, s)), Puntos(bid + SPREAD), Puntos(bid), 0, 0)


def broker(ticks: list[Tick], m1: list[Vela]) -> Broker:
    reglas = ReglasBroker(
        volumen_max_lotes=Decimal(10),
        ordenes_simultaneas_max=3,
        posiciones_dia_max=5,
        huso_corte=ZoneInfo("America/New_York"),
        comision_por_lote=Decimal(0),
        comision_por_lado=True,
        swap_largo_puntos=Decimal(0),
        swap_corto_puntos=Decimal(0),
    )
    cfg = Configuracion(False, 0, lambda _m: SPREAD)
    return Broker(
        dataclasses.replace(reglas), cfg, Mercado(ticks, m1), UNO, 1, stops_level_diagnostico=0
    )


def main() -> None:
    cierre = ms(M0 + 1) - 1  # el cierre de la M1 de M0 menos 1 ms: donde decide el motor
    # 1. limite de compra en 1000 colocada en el cierre de M0, que bajo a 990; M0+1 no baja
    b = broker([], [vela(M0, 1010, 1011, 990, 1005), vela(M0 + 1, 1005, 1008, 1004, 1006)])
    b.avanzar(cierre)
    b.colocar_limite("o", "compra", 1000, UNO, 990, 1030, cierre)
    print("1 limite:", b.avanzar(ms(M0 + 3)))
    # 2. lo mismo con una venta stop en 995
    b = broker([], [vela(M0, 1010, 1011, 990, 1005), vela(M0 + 1, 1005, 1008, 1004, 1006)])
    b.avanzar(cierre)
    b.colocar_stop("v", "venta", 995, UNO, 1010, 950, cierre)
    print("2 stop:", b.avanzar(ms(M0 + 3)))
    # 3. stop movido al cierre de M0 (respaldo) contra la vela M0
    b = broker([], [vela(M0 - 1, 1000, 1001, 999, 1000), vela(M0, 1000, 1015, 985, 1010),
                    vela(M0 + 1, 1010, 1012, 1008, 1011)])  # fmt: skip
    b.abrir_conocida("p", "compra", 1000, UNO, 990, 1030, ms(M0))
    b.avanzar(cierre)
    b.mover_stop("p", 1000, cierre)
    b.avanzar(ms(M0 + 3))
    p = b.posiciones["p"]
    print("3 stop movido:", p.motivo_cierre, p.precio_cierre, p.cerrada_ms, "== fin de M0:",
          p.cerrada_ms == ms(M0 + 1), "| el stop original 990, tocado en M0 (minima 985)")  # fmt: skip  # noqa: E501
    # 4. cotizacion frente a precio_de_conversion en el cierre de M0 sin ticks
    b = broker([], [vela(M0 - 1, 1000, 1001, 999, 1000), vela(M0, 1000, 1015, 985, 1010)])
    print("4 cotizacion:", b.mercado.cotizacion(cierre, lambda _m: SPREAD),
          "| precio_de_conversion compra:", b.precio_de_conversion("compra", cierre),
          "| _precio_de_mercado compra:", b._precio_de_mercado("compra", cierre))  # fmt: skip
    # 5. _peor_del_minuto: una posicion viva que cierra por stop del respaldo al fin de M0; la marca
    # del minuto siguiente M0+1 (que baja a 900) se toma al sellar el evento en ms(M0+1)
    b = broker([], [vela(M0, 1000, 1001, 989, 1000), vela(M0 + 1, 1000, 1001, 900, 950)])
    b.abrir_conocida("p", "compra", 1000, UNO, 990, 1030, ms(M0))
    b.avanzar(ms(M0 + 1))
    p = b.posiciones["p"]
    print("5 marcas:", [(m - ms(M0), v) for m, v in p.marcas], "cerrada en", p.cerrada_ms - ms(M0))
    # 6. minuto con ticks pero sin ninguno anterior al instante
    b = broker([tick(M0, 30, 1020)], [vela(M0, 1000, 1025, 999, 1020)])
    print("6 en ms(M0,10):", b._precio_de_mercado("compra", ms(M0, 10)),
          b.precio_de_conversion("compra", ms(M0, 10)),
          b.mercado.cotizacion(ms(M0, 10), lambda _m: SPREAD))  # fmt: skip


main()
