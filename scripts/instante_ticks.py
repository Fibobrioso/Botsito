"""El instante del xlsx medido con TICKS, solo con las operaciones del trader de construccion.

Fase 7 de `trabajo/ticks-llenado`. La medida original (`scripts/instante_llenado.py`, ADR-0043)
usa la M1 del minuto: dentro si la entrada cae en [minima - 2, maxima + 2]. Con ticks se mide:

- en cuantas operaciones el precio de entrada SE TOCA dentro del minuto del instante del xlsx
  (algun tick cuyo BID o ASK, segun el lado, queda a <= 2 puntos de la entrada), y la distancia en
  segundos desde el instante del xlsx al PRIMER toque del minuto;
- en cuantas una M1 no permite saber el orden de los toques y los ticks si: la M1 del minuto cubre
  la entrada y el stop a la vez (no dice cual se toco antes) y los ticks dicen cual fue primero;
- el MISMO control que la medida original: el instante desplazado -30 y +30 minutos, donde la
  tasa tiene que caer.

Solo lee los casos dev de construccion (por la compuerta), sus ticks y sus M1. Imprime tasas,
recuentos y segundos; ni una entrada, ni un stop, ni un instante de operacion.

  `uv run python scripts/instante_ticks.py --salida <fichero>`
"""

from __future__ import annotations

import sys
from collections import Counter, defaultdict
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
MARGEN_PUNTOS = 2
DESPLAZAMIENTOS = {"instante": 0, "-30 min": -30, "+30 min": 30}


@dataclass(frozen=True)
class TickMin:
    ms: int
    ask: int
    bid: int


def toques(
    ticks: Sequence[TickMin], lado: str, nivel: int, margen: int = MARGEN_PUNTOS
) -> list[int]:
    """Los ms de los ticks del minuto cuyo lado relevante queda a <= margen del nivel. Puro."""
    salida = []
    for t in ticks:
        valor = t.ask if lado == "compra" else t.bid
        if abs(valor - nivel) <= margen:
            salida.append(t.ms)
    return salida


def primero_de(
    ticks: Sequence[TickMin], lado: str, entrada: int, stop: int, margen: int = MARGEN_PUNTOS
) -> str | None:
    """Con ticks: que se toco antes, la entrada o el stop, o None si ninguno. Puro."""
    te, ts = toques(ticks, lado, entrada, margen), toques(ticks, lado, stop, margen)
    if not te and not ts:
        return None
    if te and (not ts or te[0] <= ts[0]):
        return "entrada"
    return "stop"


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] != "--salida":
        print("uso: instante_ticks.py --salida <fichero>", file=sys.stderr)
        return 2
    sys.path.insert(0, str(RAIZ / "src"))
    from botsito.cases import visto
    from botsito.cases.criterio_fidelidad import cargar_criterio
    from botsito.cases.paquete import cargar_config
    from botsito.config.ajustes import carpeta_datos
    from botsito.config.registro import cargar_registro
    from botsito.data.velas import a_minuto
    from botsito.domain.ticks import MS_POR_MINUTO
    from botsito.engine import simulacion
    from botsito.engine.visor import caso_de_construccion

    datos = carpeta_datos(RAIZ)
    criterio = cargar_criterio(RAIZ)
    registro = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
    config = cargar_config(RAIZ / "knowledge" / "cases" / "kit" / "config.yaml")
    cuenta: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    distancias: dict[str, list[float]] = defaultdict(list)
    orden: dict[str, Counter[str]] = defaultdict(Counter)
    cabecera = [
        f"MARGEN: {MARGEN_PUNTOS} puntos (el de instante_llenado.py); toque = algun tick del "
        "minuto con el lado relevante (ASK compra, BID venta) a <= margen de la entrada",
        f"MESES: construccion {', '.join(criterio.construccion)}",
    ]
    for mes in criterio.construccion:
        casos = sorted(c for c, p in visto.asignacion(RAIZ, mes).items() if p == "dev")
        for caso in casos:
            caso_de_construccion(RAIZ, criterio, caso)
            md = simulacion.mercado_de_construccion(
                RAIZ, datos, criterio, config, registro, caso, con_operaciones_del_trader=True
            )
            por_minuto: dict[int, list[TickMin]] = defaultdict(list)
            for t in md.ticks:
                por_minuto[int(t.minuto)].append(TickMin(int(t.instante), int(t.ask), int(t.bid)))
            m1 = {int(v.inicio): v for v in md.m1}
            assert md.operaciones_trader is not None
            for op in md.operaciones_trader:
                entrada = int((op.apertura.precio * md.escala).to_integral_value())
                stop = (
                    int((op.marcas[0].precio * md.escala).to_integral_value())
                    if op.marcas
                    else None
                )
                instante = op.apertura.instante
                for nombre, dmin in DESPLAZAMIENTOS.items():
                    t0 = instante + timedelta(minutes=dmin)
                    minuto = int(a_minuto(t0.replace(second=0, microsecond=0)))
                    ticks = por_minuto.get(minuto)
                    for clave in ((mes, nombre), ("total", nombre)):
                        cuenta[clave]["total"] += 1
                        if ticks is None:
                            cuenta[clave]["sin_ticks"] += 1
                            continue
                        tq = toques(ticks, op.direccion, entrada)
                        if tq:
                            cuenta[clave]["toca"] += 1
                            if nombre == "instante" and clave[0] == mes:
                                ms0 = (
                                    int(a_minuto(t0.replace(second=0, microsecond=0)))
                                    * MS_POR_MINUTO
                                    + t0.second * 1000
                                )
                                distancias[mes].append((tq[0] - ms0) / 1000)
                                distancias["total"].append((tq[0] - ms0) / 1000)
                if (
                    stop is not None
                    and (
                        ticks_i := por_minuto.get(
                            int(a_minuto(instante.replace(second=0, microsecond=0)))
                        )
                    )
                    is not None
                ):
                    vela = m1.get(int(a_minuto(instante.replace(second=0, microsecond=0))))
                    if vela is not None:
                        lo, hi = int(vela.minima) - MARGEN_PUNTOS, int(vela.maxima) + MARGEN_PUNTOS
                        ambos = lo <= entrada <= hi and lo <= stop <= hi
                        for clave in (mes, "total"):
                            orden[clave]["operaciones"] += 1
                            if ambos:
                                orden[clave]["m1_no_distingue"] += 1
                                if primero_de(ticks_i, op.direccion, entrada, stop) is not None:
                                    orden[clave]["ticks_si"] += 1
    salida = list(cabecera)
    for mes in (*criterio.construccion, "total"):
        partes = []
        for nombre in DESPLAZAMIENTOS:
            c = cuenta[(mes, nombre)]
            n = c["total"] - c["sin_ticks"]
            tasa = 100 * c["toca"] / n if n else 0.0
            partes.append(f"{nombre}: {c['toca']}/{n} = {tasa:.1f} % ({c['sin_ticks']} sin ticks)")
        salida.append(f"{mes}: " + " | ".join(partes))
        d = sorted(distancias[mes])
        if d:
            mediana = d[len(d) // 2]
            salida.append(
                f"{mes}: distancia al primer toque (s) sobre {len(d)} tocadas: mediana "
                f"{mediana:.1f}, min {d[0]:.1f}, max {d[-1]:.1f}; en el mismo segundo o antes "
                f"{sum(1 for x in d if x <= 0)}"
            )
        o = orden[mes]
        salida.append(
            f"{mes}: la M1 del minuto cubre entrada y stop a la vez en {o['m1_no_distingue']} de "
            f"{o['operaciones']}; en {o['ticks_si']} de esas los ticks dicen cual se toco antes"
        )
    inst = cuenta[("total", "instante")]
    ctrl = [cuenta[("total", n)] for n in DESPLAZAMIENTOS if n != "instante"]
    n_i = inst["total"] - inst["sin_ticks"]
    tasa_i = inst["toca"] / n_i if n_i else 0
    tasas_c = [
        (c["toca"] / (c["total"] - c["sin_ticks"])) if (c["total"] - c["sin_ticks"]) else 0
        for c in ctrl
    ]
    salida.append(
        "== CONTROL: "
        + (
            "cae claramente"
            if all(t < tasa_i / 2 for t in tasas_c)
            else "NO cae: el test no discrimina"
        )
    )
    Path(argv[1]).write_text("\n".join(salida) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(salida))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
