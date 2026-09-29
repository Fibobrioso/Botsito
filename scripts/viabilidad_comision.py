"""La viabilidad del trader con la comisión más probable y con las variantes de gestión del stop
(A-18). Rama `trabajo/viabilidad-comision`, 2026-09-28 (docs/validation/VIABILIDAD-COMISION.md).

Es una MEDICIÓN: no cambia la estrategia, el bot, el bróker ni ningún parámetro del perfil; la
comisión de cada escenario vive solo en esta corrida. Estos resultados NO se enseñan al trader.

Las 77 operaciones de construcción (abril y agosto) se cargan como en `viabilidad_trader.py` y se
repiten por el bróker simulado sobre los ticks de Dukascopy, al 0,5 % de riesgo sobre el saldo
realizado, con tres comisiones de ida y vuelta por lote (3, 5 y 10 USD, cobradas la mitad en cada
lado) y cuatro variantes de A-18. SUPUESTO de las variantes: la entrada es el 0 de la caja y el
stop inicial del libro (`initialSL`) es su 1; la distancia 0 -> 1 es D.

- V1: stop en el 1, lote para el 1, objetivo a 3 D (la de hoy; con el movimiento documentado de
  v7-3, como en `viabilidad_trader.py`).
- V2: stop en el 0,8, lote para el 0,8, objetivo a 3 D (RR efectivo 3 / 0,8 = 3,75).
- V3: lote para el 1, stop movido al 0,8 en el instante del llenado, objetivo a 3 D.
- V4: lote para el 1, stop movido al 0,8 en el instante del llenado, objetivo a 3 veces 0,8 D.

R es el riesgo nominal de cada variante: lo que se pierde por lote hasta la distancia con la que se
calcula el lote (D en V1, V3 y V4; 0,8 D en V2). La serie ANOTADA usa la salida real del libro, con
el lote para el 1: solo depende de la comisión. Lee el repositorio en --raiz; escribe en --salida.

    uv run python scripts/viabilidad_comision.py --salida <fichero> [--raiz <repo>]
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections.abc import Sequence
from dataclasses import dataclass, replace
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

RAIZ_SCRIPT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ_SCRIPT / "src"))
sys.path.insert(0, str(RAIZ_SCRIPT / "scripts"))

import viabilidad_trader as vt  # noqa: E402

RIESGO_PCT = Decimal("0.5")  # `riesgo_por_operacion`, CONFIRMED
# comision de ida y vuelta por lote, en USD: 3 (FTMO en otros pares, terceros), 5 (API), 10 (perfil)
COMISIONES_IDA_Y_VUELTA = (Decimal(3), Decimal(5), Decimal(10))
VARIANTES = ("V1", "V2", "V3", "V4")
PUNTOS_POR_PIP = 10  # EURUSD a 5 decimales


# ------------------------------------------------------------------------------------ puras


@dataclass(frozen=True)
class Niveles:
    """Los precios de una variante, en puntos: el stop con el que abre, el stop al que se mueve en
    el llenado (si se mueve), el objetivo y la distancia con la que se calcula el lote."""

    stop_inicial: int
    stop_tras_llenado: int | None
    objetivo: int
    distancia_lote: int


def niveles(variante: str, direccion: str, entrada: int, stop_en_el_1: int) -> Niveles:
    """Los niveles de la variante, con la entrada en el 0 y el stop del libro en el 1. Puro."""
    d = abs(entrada - stop_en_el_1)
    if d == 0:
        raise ValueError("stop en la entrada")
    s = 1 if direccion == "compra" else -1  # sentido de la ganancia
    d08 = int(
        (Decimal(d) * Decimal("0.8")).to_integral_value()
    )  # al punto mas cercano: 0,8 D nunca cae en medio punto
    stop_08 = entrada - s * d08
    if variante == "V1":
        return Niveles(stop_en_el_1, None, entrada + s * 3 * d, d)
    if variante == "V2":
        return Niveles(stop_08, None, entrada + s * 3 * d, d08)
    if variante == "V3":
        return Niveles(stop_en_el_1, stop_08, entrada + s * 3 * d, d)
    if variante == "V4":
        return Niveles(stop_en_el_1, stop_08, entrada + s * 3 * d08, d)
    raise ValueError(f"variante {variante!r} desconocida")


def r_nominal(direccion: str, entrada: int, cierre: int, distancia_lote: int) -> float:
    """El resultado en R de la variante: lo movido a favor entre la distancia del lote."""
    signo = 1 if direccion == "compra" else -1
    return signo * (cierre - entrada) / distancia_lote


def pips(puntos: float) -> float:
    return puntos / PUNTOS_POR_PIP


def coste_en_r(
    comision_ida_y_vuelta: Decimal,
    spread_puntos: int,
    distancia_lote: int,
    contrato: Decimal,
    escala: int,
) -> tuple[float, float]:
    """(comision, spread) en R: por lote, entre lo que se pierde por lote hasta la distancia del
    lote. Con EURUSD y cuenta en USD un punto por lote es un dolar, asi que 10 USD cuestan
    10 / distancia R. El spread se da como coste informativo: ya va dentro de los precios."""
    por_lote = Decimal(distancia_lote) / escala * contrato
    spread_usd = Decimal(spread_puntos) / escala * contrato
    return float(comision_ida_y_vuelta / por_lote), float(spread_usd / por_lote)


def celda(esperanza: float, ic_bajo: float, ic_alto: float, veredictos: Sequence[str]) -> str:
    """Una celda de la tabla resumen: esperanza neta [IC] y los tres veredictos."""
    return (
        f"{esperanza:+.2f} [{ic_bajo:+.2f}; {ic_alto:+.2f}] · " + " / ".join(veredictos)
    ).replace(".", ",")


# ------------------------------------------------------------------------------- medicion


def medir(raiz: Path) -> dict[str, Any]:
    from botsito.data.velas import a_minuto
    from botsito.domain.ticks import MS_POR_MINUTO
    from botsito.engine.broker import Broker, BrokerError
    from botsito.engine.cuenta import Cargo, Marca, Operacion, evaluar_fase

    ctx = vt.cargar(raiz)
    rf, contrato = ctx.reglas_fase, ctx.contrato
    ops = ctx.ops

    def pts(precio: Decimal, escala: int) -> int:
        return int((precio * escala).to_integral_value())

    def ms_de(t: datetime) -> int:
        return int(a_minuto(t.replace(second=0, microsecond=0))) * MS_POR_MINUTO + t.second * 1000

    def spread_en(md: Any, ms: int) -> int:
        """El spread del ultimo tick anterior o igual al llenado."""
        previos = [x for x in md.ticks if int(x.instante) <= ms]
        return int(previos[-1].ask) - int(previos[-1].bid) if previos else 0

    def simular(
        tramo: Sequence[vt.OpTrader], variante: str, comision: Decimal
    ) -> tuple[list[Any], dict[str, dict[str, Any]]]:
        reglas = replace(
            ctx.reglas_broker, comision_por_lote=comision / 2, comision_por_lado=True
        )  # la mitad en cada lado: la ida y vuelta entera
        cerradas: list[Any] = []
        det: dict[str, dict[str, Any]] = {}
        saldo = rf.capital_inicial
        for dia in sorted({o.dia for o in tramo}):
            md = ctx.mercados[dia]
            b = Broker(reglas, ctx.cfg, md.mercado(), contrato, md.escala)
            vistas = 0
            for o in sorted((x for x in tramo if x.dia == dia), key=lambda x: x.instante):
                ms = ms_de(o.instante)
                b.avanzar(ms - 1)
                nuevas = b.operaciones_cerradas()[vistas:]
                saldo += sum((vt._pnl(c, contrato) for c in nuevas), Decimal(0))
                vistas += len(nuevas)
                entrada = pts(o.entrada, md.escala) - vt.DESFASE_PUNTOS
                stop1 = pts(o.stop, md.escala) - vt.DESFASE_PUNTOS
                n = niveles(variante, o.direccion, entrada, stop1)
                lotes = vt.lote_por_riesgo(
                    saldo * RIESGO_PCT / 100, n.distancia_lote, contrato, md.escala
                )
                det[o.id] = {
                    "entrada": entrada,
                    "distancia_lote": n.distancia_lote,
                    "stop_efectivo": abs(entrada - (n.stop_tras_llenado or n.stop_inicial)),
                    "spread": spread_en(md, ms),
                    "lotes": str(lotes),
                }
                if lotes <= 0:
                    det[o.id]["fuera"] = "lote 0"
                    continue
                try:
                    b.abrir_conocida(
                        f"p-{o.id}", o.direccion, entrada, lotes, n.stop_inicial, n.objetivo,  # type: ignore[arg-type]
                        ms, "caso",
                    )  # fmt: skip
                except BrokerError as exc:
                    det[o.id]["fuera"] = str(exc).rsplit("(", 1)[-1].rstrip(")")
                    continue
                pid = f"p-{o.id}"
                if n.stop_tras_llenado is not None:
                    b.mover_stop(pid, n.stop_tras_llenado, ms)
                mov = vt.MOVIMIENTOS.get((o.instante.isoformat(), str(o.entrada)))
                if variante == "V1" and mov is not None:  # como viabilidad_trader.py
                    t_mov = datetime.fromisoformat(mov[0])
                    b.avanzar(ms_de(t_mov) - 1)
                    if b.posiciones[pid].abierta:
                        b.mover_stop(
                            pid, pts(Decimal(mov[1]), md.escala) - vt.DESFASE_PUNTOS, ms_de(t_mov)
                        )
            b.avanzar(md.hasta_ms - 1)
            for p in list(b.posiciones.values()):
                if p.abierta:
                    b.cerrar_a_mercado(p.id, md.hasta_ms - 1)
            nuevas = b.operaciones_cerradas()[vistas:]
            saldo += sum((vt._pnl(c, contrato) for c in nuevas), Decimal(0))
            for p in b.posiciones.values():
                det[p.id.removeprefix("p-")]["cierre"] = p.precio_cierre
            cerradas.extend(replace(c, id=f"{dia}/{c.id}") for c in b.operaciones_cerradas())
        return cerradas, det

    def anotadas(tramo: Sequence[vt.OpTrader], comision: Decimal) -> list[Any]:
        salida: list[Any] = []
        saldo = rf.capital_inicial
        pendientes: list[tuple[datetime, Decimal]] = []
        for o in sorted(tramo, key=lambda x: x.instante):
            saldo += sum((q for t, q in pendientes if t <= o.instante), Decimal(0))
            pendientes = [(t, q) for t, q in pendientes if t > o.instante]
            d = abs(pts(o.entrada, 100_000) - pts(o.stop, 100_000))
            lotes = vt.lote_por_riesgo(saldo * RIESGO_PCT / 100, d, contrato, 100_000)
            if lotes <= 0 or lotes > ctx.reglas_broker.volumen_max_lotes:
                continue
            op = Operacion(
                id=o.id,
                direccion=o.direccion,  # type: ignore[arg-type]
                lotes=lotes,
                apertura=Marca(o.instante, o.entrada),
                cierre=Marca(o.instante_cierre, o.cierre_anotado),
                cargos=(
                    Cargo(o.instante, comision / 2 * lotes, "comision"),
                    Cargo(o.instante_cierre, comision / 2 * lotes, "comision"),
                ),
            )
            salida.append(op)
            pendientes.append((o.instante_cierre, vt._pnl(op, contrato)))
        return salida

    def cuenta(cerradas: Sequence[Any]) -> dict[str, Any]:
        r = evaluar_fase(cerradas, rf, contrato)
        capital = rf.capital_inicial
        peor_dia = max(
            (d.saldo_corte - (d.equity_minima if d.equity_minima is not None else d.saldo_corte)
             for d in r.dias),
            default=Decimal(0),
        )  # fmt: skip
        return {
            "estado": r.estado.value,
            "instante": r.instante.isoformat() if r.instante else None,
            "motivo": r.motivo[:120],
            "peor_dia_pct": f"{100 * peor_dia / capital:.2f}",
            "dias_de_trading": r.dias_de_trading,
        }

    def resumen_r(rs: Sequence[float], netas: Sequence[float]) -> dict[str, Any]:
        e = vt.estadisticas(list(netas))
        return {
            "n": len(rs),
            "acierto": round(sum(1 for r in rs if vt.clase(r) == "gana") / len(rs), 3),
            "esperanza_bruta": round(statistics.fmean(rs), 3),
            "esperanza_neta": round(e.esperanza, 3),
            "ic_bajo": round(e.ic_bajo, 3),
            "ic_alto": round(e.ic_alto, 3),
        }

    tramos = {
        "abril": [o for o in ops if o.dia.startswith("2026-04")],
        "agosto": [o for o in ops if o.dia.startswith("2026-08")],
        "abril+agosto": list(ops),
    }
    resultado: dict[str, Any] = {"combinaciones": {}, "anotada": {}}
    for comision in COMISIONES_IDA_Y_VUELTA:
        for variante in VARIANTES:
            fila: dict[str, Any] = {}
            for nombre, tramo in tramos.items():
                cerradas, det = simular(tramo, variante, comision)
                fila[nombre] = cuenta(cerradas)
                if nombre != "abril+agosto":
                    continue
                dentro = {i: v for i, v in det.items() if "cierre" in v}
                por_id = {o.id: o for o in ops}
                rs, netas, ganan, pierden, com_r, spr_r = [], [], [], [], [], []
                for i, v in dentro.items():
                    r = r_nominal(
                        por_id[i].direccion, v["entrada"], v["cierre"], v["distancia_lote"]
                    )
                    c, s = coste_en_r(comision, v["spread"], v["distancia_lote"], contrato, 100_000)
                    rs.append(r)
                    netas.append(r - c)
                    com_r.append(c)
                    spr_r.append(s)
                    movido = (v["cierre"] - v["entrada"]) * (
                        1 if por_id[i].direccion == "compra" else -1
                    )
                    (
                        ganan
                        if vt.clase(r) == "gana"
                        else pierden
                        if vt.clase(r) == "pierde"
                        else []
                    ).append(pips(movido))
                stops = [pips(v["stop_efectivo"]) for v in det.values()]
                fila["r"] = resumen_r(rs, netas)
                fila["fuera_por_volumen"] = sum(
                    1 for v in det.values() if v.get("fuera") == "volumen_max_lotes"
                )
                fila["pips_ganadoras"] = round(statistics.fmean(ganan), 2) if ganan else None
                fila["pips_perdedoras"] = round(statistics.fmean(pierden), 2) if pierden else None
                fila["stop_pips_medio"] = round(statistics.fmean(stops), 2)
                fila["stop_pips_mediano"] = round(statistics.median(stops), 2)
                fila["comision_r_media"] = round(statistics.fmean(com_r), 3)
                fila["spread_r_medio"] = round(statistics.fmean(spr_r), 3)
            resultado["combinaciones"][f"{comision}/{variante}"] = fila
        # la anotada: la salida real del libro, lote para el 1
        fila_a: dict[str, Any] = {}
        for nombre, tramo in tramos.items():
            fila_a[nombre] = cuenta(anotadas(tramo, comision))
        rs, netas, ganan, pierden, com_r = [], [], [], [], []
        for o in ops:
            e, s, c = pts(o.entrada, 100_000), pts(o.stop, 100_000), pts(o.cierre_anotado, 100_000)
            d = abs(e - s)
            r = r_nominal(o.direccion, e, c, d)
            cr, _ = coste_en_r(comision, 0, d, contrato, 100_000)
            rs.append(r)
            netas.append(r - cr)
            com_r.append(cr)
            movido = (c - e) * (1 if o.direccion == "compra" else -1)
            (ganan if vt.clase(r) == "gana" else pierden if vt.clase(r) == "pierde" else []).append(
                pips(movido)
            )
        fila_a["r"] = resumen_r(rs, netas)
        fila_a["pips_ganadoras"] = round(statistics.fmean(ganan), 2)
        fila_a["pips_perdedoras"] = round(statistics.fmean(pierden), 2)
        fila_a["stop_pips_medio"] = round(
            statistics.fmean(
                pips(abs(pts(o.entrada, 100_000) - pts(o.stop, 100_000))) for o in ops
            ),
            2,
        )
        fila_a["stop_pips_mediano"] = round(
            statistics.median(
                pips(abs(pts(o.entrada, 100_000) - pts(o.stop, 100_000))) for o in ops
            ),
            2,
        )
        fila_a["comision_r_media"] = round(statistics.fmean(com_r), 3)
        resultado["anotada"][str(comision)] = fila_a
    return resultado


def main(argv: Sequence[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else None)
    p.add_argument("--raiz", type=Path, default=RAIZ_SCRIPT)
    p.add_argument("--salida", type=Path, required=True)
    args = p.parse_args(argv)
    resultado = medir(args.raiz)
    args.salida.write_text(
        json.dumps(resultado, indent=1, ensure_ascii=False, default=str), encoding="utf-8"
    )
    print(json.dumps({k: v["r"] for k, v in resultado["combinaciones"].items()}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
