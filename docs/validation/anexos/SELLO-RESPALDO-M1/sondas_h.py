"""Diagnostico de H (2026-10-31): sondas con velas y ticks SINTETICOS de 2030, adaptadas de
`docs/validation/anexos/RESPALDO-M1/sonda_z.py`, sobre el codigo del CLON que se nombra. No lee
datos ni escribe nada.

COPIA de `diagH\\sondas_h.py` (scratchpad de una sesion anterior, fuera del repo) traida por
`trabajo/sello-respaldo-m1` el 2026-11-07, con UN cambio: sin el `sys.path.insert` de la raiz, que
la guardia niega (cambia `sys.path` con un valor calculado). `uv run` desde la raiz del clon ya
importa `botsito` de su `src/`, asi que mide lo mismo; la raiz sigue en el primer argumento y el
guion comprueba que `botsito` sale de ella.

    cd C:/cm/main && uv run python <ruta>/sondas_h.py C:/cm/main <main|c|d|e1|e2|c+e2|c2>

La forma solo cambia DONDE decide el motor en las sondas que lo emulan: en (d) en el cierre `t`;
en las demas en `t - 1 ms` (cableado.py:297). Lo demas lo hace el codigo del clon tal cual."""

from __future__ import annotations

import dataclasses
import sys
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from zoneinfo import ZoneInfo

RAIZ = Path(sys.argv[1]).resolve()
FORMA = sys.argv[2]
import botsito  # noqa: E402

if not Path(botsito.__file__).resolve().is_relative_to(RAIZ / "src"):
    raise SystemExit(f"botsito sale de {botsito.__file__}, no de {RAIZ / 'src'}")
from botsito.data.velas import a_minuto  # noqa: E402
from botsito.domain.cierres import CalendarioCierres, Cierre, ReglasCierres  # noqa: E402
from botsito.domain.ticks import MS_POR_MINUTO, MilisegundoUtc, Tick  # noqa: E402
from botsito.domain.valores import Puntos  # noqa: E402
from botsito.domain.velas import MinutoUtc, Vela  # noqa: E402
from botsito.engine.broker import Broker, BrokerError, ReglasBroker  # noqa: E402
from botsito.engine.llenado import Configuracion, Mercado  # noqa: E402

SPREAD = 3
UNO = Decimal(1)
M0 = int(a_minuto(datetime(2030, 1, 15, 8, 0, tzinfo=UTC)))
HORA = 60 * MS_POR_MINUTO


def ms(m: int, s: int = 0) -> int:
    return m * MS_POR_MINUTO + s * 1000


def rel(x: int | None) -> str:
    """Un instante relativo a M0, legible: «M0+2 -1ms»."""
    if x is None:
        return "None"
    m, resto = divmod(x - ms(M0), MS_POR_MINUTO)
    if resto == 0:
        return f"M0+{m}"
    if resto == MS_POR_MINUTO - 1:
        return f"M0+{m + 1} -1ms"
    return f"M0+{m} +{resto}ms"


def decide(m: int) -> int:
    """Donde decide el motor en el cierre de la M1 `m`."""
    return ms(m + 1) if FORMA == "d" else ms(m + 1) - 1


def vela(m: int, o: int, h: int, low: int, c: int) -> Vela:
    return Vela(MinutoUtc(m), Puntos(o), Puntos(h), Puntos(low), Puntos(c), 1)


def tick(m: int, s: int, bid: int) -> Tick:
    return Tick(MilisegundoUtc(ms(m, s)), Puntos(bid + SPREAD), Puntos(bid), 0, 0)


def broker(ticks: list[Tick], m1: list[Vela], cierres: ReglasCierres | None = None) -> Broker:
    reglas = ReglasBroker(
        volumen_max_lotes=Decimal(10),
        ordenes_simultaneas_max=10,
        posiciones_dia_max=10,
        huso_corte=ZoneInfo("UTC"),
        comision_por_lote=Decimal(0),
        comision_por_lado=True,
        swap_largo_puntos=Decimal(0),
        swap_corto_puntos=Decimal(0),
        cierres=cierres,
    )
    cfg = Configuracion(False, 0, lambda _m: SPREAD)
    return Broker(
        dataclasses.replace(reglas), cfg, Mercado(ticks, m1), UNO, 1, stops_level_diagnostico=0
    )


def ev(eventos: list[tuple[int, str, str, str]]) -> list[tuple[str, str, str, str]]:
    return [(rel(t), tipo, i, f) for t, tipo, i, f in eventos]


def s1_marcas_vela_del_llenado() -> None:
    """Limite de compra en 1000 (stop 990) colocada al EMPEZAR M0: la M0 la llena (ASK minimo 973)
    y baja a 970, por debajo del stop; la M0+1 se queda en 1000-1006. Las marcas y la que recibiria
    `cuenta.marcar` (`cableado.py:447-450`: la ultima, si su instante <= hasta)."""
    b = broker([], [vela(M0, 1010, 1012, 970, 1004), vela(M0 + 1, 1004, 1006, 1000, 1005)])
    b.colocar_limite("o", "compra", 1000, UNO, 990, 1030, ms(M0))
    print("S1 eventos al decidir en el cierre de M0:", ev(b.avanzar(decide(M0))))
    p = b.posiciones.get("pos-o")
    if p is None:
        print("S1 sin posicion tras el cierre de M0")
    else:
        print("S1 abierta_ms:", rel(p.abierta_ms), "| marcas:", [(rel(t), v) for t, v in p.marcas],
              "| a cuenta.marcar:", (rel(p.marcas[-1][0]), p.marcas[-1][1]) if p.marcas and
              p.marcas[-1][0] <= decide(M0) else None)  # fmt: skip
    b.avanzar(decide(M0 + 1))
    p = b.posiciones["pos-o"]
    print("S1 tras el cierre de M0+1: abierta", p.abierta, "| marcas:",
          [(rel(t), v) for t, v in p.marcas])  # fmt: skip
    # la ventana de m1_entre del break even (primitivas_broker.py:279): M1 con inicio en
    # [abierta_ms // 60000, instante), con `instante` = el minuto del cierre en que decide
    instante = M0 + 2
    # la formula de primitivas_broker.py:279 tal como queda en cada forma: en (c2), con «+ 1»
    desde = (p.abierta_ms + (1 if FORMA == "c2" else 0)) // MS_POR_MINUTO
    print(
        "S2 m1_entre del break even en el cierre de M0+1 (instante M0+2): inicios",
        [f"M0+{m - M0}" for m in range(desde, instante)],
        "(la vela del llenado es M0)",
    )


def s3_sesion_del_llenado() -> None:
    """La ultima vela de 07-11 llena una venta stop colocada antes; la sesion de la posicion por
    `cableado.py:464-465` (minuto = abierta_ms // 60000; d <= minuto < h)."""
    limite = M0 + 3  # 07-11 acaba en M0+3 (exclusivo) y empieza 11-15
    limites = [("07-11", M0 - 240, limite), ("11-15", limite, limite + 240)]
    m1 = [vela(M0 + k, 1010, 1011, 1005, 1008) for k in range(2)]
    m1 += [vela(M0 + 2, 1008, 1009, 990, 995), vela(M0 + 3, 995, 999, 994, 996)]
    b = broker([], m1)
    b.colocar_stop("v", "venta", 1000, UNO, 1020, 950, ms(M0))
    b.avanzar(decide(M0 + 2))
    b.avanzar(decide(M0 + 3))
    p = b.posiciones["pos-v"]
    # la formula de cableado.py:464 tal como queda en cada forma: en (c2), con «+ 1»
    minuto = (p.abierta_ms + (1 if FORMA == "c2" else 0)) // MS_POR_MINUTO
    sesion = next((n for n, d, h in limites if d <= minuto < h), None)
    print("S3 llenado en la vela M0+2 (la ultima de 07-11): abierta", rel(p.abierta_ms),
          "-> sesion", sesion)  # fmt: skip


def s4_fin_de_la_ventana() -> None:
    """El fin del dia de `cableado.py:350-358`: `ultimo` = M0+2, fin_ms = ultimo*60000 - 1 (en (d),
    ultimo*60000). Una limite viva desde M0 y una posicion viva; la ultima vela (M0+1) cruza la
    limite y el stop de la posicion."""
    ultimo = M0 + 2
    fin_ms = ultimo * MS_POR_MINUTO if FORMA == "d" else ultimo * MS_POR_MINUTO - 1
    m1 = [vela(M0, 1010, 1011, 1005, 1008), vela(M0 + 1, 1008, 1009, 985, 990)]
    m1 += [vela(M0 + 2, 990, 991, 989, 990)]  # la vela de `ultimo`, por si alguien la pide
    b = broker([], m1)
    b.colocar_limite("o", "compra", 995, UNO, 980, 1030, ms(M0))
    b.abrir_conocida("p", "compra", 1005, UNO, 988, 1030, ms(M0))
    b.avanzar(decide(M0))
    try:
        b.avanzar(fin_ms)
        for p in list(b.posiciones.values()):
            if p.abierta:
                b.cerrar_a_mercado(p.id, fin_ms)
        for o in list(b.ordenes.values()):
            if o.estado in ("colocada", "modificada"):
                b.cancelar(o.id, fin_ms)
        b.avanzar(fin_ms)
    except BrokerError as e:
        print("S4 BrokerError:", e)
    print("S4 fin del dia en", rel(fin_ms), "| eventos:", ev(b.traza().eventos))
    print("S4 cierres:", [(p.id, p.motivo_cierre, p.precio_cierre, rel(p.cerrada_ms))
                          for p in b.posiciones.values()])  # fmt: skip


def s5_borde_adr0068() -> None:
    """Una ventana prohibida empieza en W = M0+2 (redondo). Una limite colocada al empezar M0; la
    vela M0+1, que acaba en W, la cruza. Y una posicion viva cuya marca se toma en W."""
    w = ms(M0 + 2)
    margen = 120 * MS_POR_MINUTO
    cal = CalendarioCierres((Cierre(w + margen, w + margen + 3 * HORA, "sintetico"),),
                            ms(M0 - 600), ms(M0 + 6000))  # fmt: skip
    m1 = [vela(M0, 1010, 1011, 1005, 1008), vela(M0 + 1, 1008, 1009, 990, 995)]
    m1 += [vela(M0 + 2, 995, 996, 900, 950), vela(M0 + 3, 950, 951, 949, 950)]
    b = broker([], m1, ReglasCierres(cal, margen, 120 * MS_POR_MINUTO, True))
    b.colocar_limite("o", "compra", 1000, UNO, 960, 1030, ms(M0))
    b.abrir_conocida("p", "compra", 1005, UNO, 800, 1100, ms(M0))
    b.avanzar(decide(M0 + 1))
    b.avanzar(decide(M0 + 2))
    print("S5 al decidir en el cierre de M0+2 (W =", rel(w), "):", ev(b.traza().eventos),
          "| orden:", b.ordenes["o"].estado, "| cierres:",
          [(rel(c.instante_ms), c.id) for c in b.traza().cierres])  # fmt: skip
    print("S5 marcas de la posicion viva p:", [(rel(t), v) for t, v in b.posiciones["p"].marcas])


def s6_cancelada_en_el_cierre() -> None:
    """Los 22 de RESPALDO-M1 §0.l: venta stop en 995 colocada al empezar M0; la M0+1, sin ticks,
    baja a 990; el motor la cancela en el cierre de M0+1 (como hace con una cancelacion RN-035 o un
    cambio de zona). Como el motor: si sigue pendiente al decidir, la cancela."""
    b = broker([], [vela(M0, 1010, 1011, 1005, 1008), vela(M0 + 1, 1008, 1009, 990, 995),
                    vela(M0 + 2, 995, 996, 994, 995)])  # fmt: skip
    b.colocar_stop("v", "venta", 995, UNO, 1010, 950, ms(M0))
    b.avanzar(decide(M0))
    nuevos = b.avanzar(decide(M0 + 1))
    o = b.ordenes["v"]
    if o.estado in ("colocada", "modificada"):
        b.cancelar("v", decide(M0 + 1))
    b.avanzar(decide(M0 + 2))
    print("S6 eventos hasta el cierre de M0+1:", ev(nuevos), "| la orden:", o.estado,
          "| historial:", [(rel(t), e) for t, e in o.historial])  # fmt: skip


def s7_peor_del_minuto() -> None:
    """La sonda 5 de sonda_z.py tal cual: larga desde M0, salta por stop con el respaldo en M0; se
    avanza hasta el instante redondo ms(M0+1). Y 7b: lo mismo sin evento del respaldo, con una
    expiracion en el instante redondo ms(M0+1) y una posicion viva."""
    b = broker([], [vela(M0, 1000, 1001, 989, 1000), vela(M0 + 1, 1000, 1001, 900, 950)])
    b.abrir_conocida("p", "compra", 1000, UNO, 990, 1030, ms(M0))
    b.avanzar(ms(M0 + 1))
    p = b.posiciones["p"]
    print("S7 marcas:", [(rel(t), v) for t, v in p.marcas], "| cerrada en", rel(p.cerrada_ms),
          "| marcas dentro de la operacion:",
          [(m.instante.isoformat()[11:23], str(m.precio)) for m in b.operaciones_cerradas()[0].marcas])  # noqa: E501  # fmt: skip
    b = broker([], [vela(M0, 1000, 1001, 995, 1000), vela(M0 + 1, 1000, 1001, 900, 950),
                    vela(M0 + 2, 950, 951, 949, 950)])  # fmt: skip
    b.abrir_conocida("p", "compra", 1000, UNO, 800, 1100, ms(M0))
    b.colocar_limite("x", "compra", 700, UNO, 690, 1100, ms(M0), expira_ms=ms(M0 + 1))
    b.avanzar(decide(M0 + 1))
    print("S7b expiracion en M0+1 (redondo), marcas de la viva:",
          [(rel(t), v) for t, v in b.posiciones["p"].marcas])  # fmt: skip


def s8_cotizaciones() -> None:
    """Las tres lecturas sin tick de la deuda «Las cotizaciones sin tick del broker no usan la misma
    vela», en el instante en que decide el motor en el cierre de M0: cotizacion (llenado.py:99-119),
    _precio_de_mercado (broker.py:978-990) y precio_de_conversion (broker.py:992-1009). M0-1 cierra
    en 1000, M0 en 1010 y M0+1 en 1020; spread 3."""
    b = broker([], [vela(M0 - 1, 1000, 1001, 999, 1000), vela(M0, 1000, 1015, 985, 1010),
                    vela(M0 + 1, 1010, 1025, 1005, 1020)])  # fmt: skip
    t = decide(M0)
    print("S8 en", rel(t), "| cotizacion:", b.mercado.cotizacion(t, lambda _m: SPREAD),
          "| _precio_de_mercado compra:", b._precio_de_mercado("compra", t),
          "| precio_de_conversion compra:", b.precio_de_conversion("compra", t))  # fmt: skip


def s9_swap_y_dia() -> None:
    """Un llenado del respaldo en la ultima vela antes del corte diario (huso UTC en la sonda;
    medianoche N): el swap (`_swaps`, broker.py:960-974, desde abierta_ms) y el dia local con que
    cuenta `posiciones_dia_max` (broker.py:1089-1092)."""
    n = int(a_minuto(datetime(2030, 1, 16, 0, 0, tzinfo=UTC)))
    m1 = [vela(n - 2, 1010, 1011, 1005, 1008), vela(n - 1, 1008, 1009, 990, 1002)]
    m1 += [vela(n, 1002, 1005, 1000, 1003), vela(n + 1, 1003, 1005, 1001, 1004)]
    b = broker([], m1)
    b.reglas = dataclasses.replace(b.reglas, swap_largo_puntos=Decimal(1))
    b.colocar_limite("o", "compra", 1000, UNO, 980, 1030, ms(n - 2))
    for k in (n - 2, n - 1, n):
        b.avanzar(ms(k + 1) if FORMA == "d" else ms(k + 1) - 1)
    p = b.posiciones["pos-o"]
    from botsito.engine.broker import _dia_local

    print("S9 abierta", (p.abierta_ms - ms(n)), "ms respecto a la medianoche | swaps:",
          [((t - ms(n)), str(v)) for t, v in p.swaps], "| dia local de la apertura:",
          _dia_local(p.abierta_ms, ZoneInfo("UTC")))  # fmt: skip


def main() -> None:
    print("forma:", FORMA, "| botsito de:", Path(botsito.__file__).parent)
    for sonda in (s1_marcas_vela_del_llenado, s3_sesion_del_llenado, s4_fin_de_la_ventana,
                  s5_borde_adr0068, s6_cancelada_en_el_cierre, s7_peor_del_minuto,
                  s8_cotizaciones, s9_swap_y_dia):  # fmt: skip
        try:
            sonda()
        except Exception as e:  # una sonda que rompe se dice y se sigue
            print(f"{sonda.__name__}: {type(e).__name__}: {e}")


main()
