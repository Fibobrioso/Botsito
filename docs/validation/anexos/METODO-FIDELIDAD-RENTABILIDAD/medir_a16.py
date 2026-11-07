# ruff: noqa: E501  (textos de salida)
"""A-16 medida (rama trabajo/metodo-fidelidad-rentabilidad, fase 1, punto 3; ADR-0092 §9 y §10;
respuesta del consultor a la PARADA, puntos 7, 8 y 9). Lo que hace el TRADER contra los datos: no es
una corrida del bot y no corre el arnes.

Para cada operacion del trader de los dias dev de construccion (por la compuerta del arnes,
`arnes.dias_de_construccion`, que cruza cada caso con `casos_ocultos` antes de leerlo):
- el minuto del llenado: `instante_utc` truncado al minuto;
- M1: la distancia en puntos de su entrada al rango [minima, maxima] de la M1 BID de Dukascopy de ese
  minuto, 0 si cae dentro;
- ticks: la distancia al tick mas cercano de ese minuto del lado en que se llenaria la orden (el BID
  en una venta, el ASK en una compra) y, aparte, de los dos lados; sin ticks en el minuto, se cuenta.
El mercado de cada dia sale de `simulacion.mercado_de_construccion`, por la misma compuerta, y lee
SOLO la ventana del dia de su propio mes: ni el mes anterior ni ningun dia reservado.

Estadisticos, en total y por mes: N, mediana, p90 (de rango: el valor en la posicion
ceil(0,9 x N) de la lista ordenada) y proporcion dentro del rango (distancia M1 = 0). Y la regla
escrita ANTES de medir (respuesta, punto 7): si la mediana M1 supera 3 puntos o la proporcion
dentro baja del 50 %, cada cifra de fidelidad lo dice y nace una linea en Technical Debt.

Uso: uv run python docs/validation/anexos/METODO-FIDELIDAD-RENTABILIDAD/medir_a16.py <raiz> [--filas]
"""

from __future__ import annotations

import math
import sys
from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

from botsito.cases.criterio_fidelidad import cargar_criterio
from botsito.cases.paquete import cargar_config
from botsito.config.ajustes import carpeta_datos
from botsito.config.registro import cargar_registro
from botsito.domain.ticks import MS_POR_MINUTO
from botsito.engine import arnes
from botsito.engine.simulacion import mercado_de_construccion

UMBRAL_MEDIANA = Decimal(3)  # la regla del punto 7 de la respuesta: 3 puntos
UMBRAL_DENTRO = Fraction(1, 2)  # y el 50 %


def _n(d: Decimal) -> str:
    """Un numero de puntos sin los ceros de escala de Decimal: 0, 1, 2.5."""
    return str(int(d)) if d == d.to_integral_value() else format(d.normalize(), "f")


def _minuto(instante: datetime) -> int:
    return int(instante.timestamp()) // 60


def _distancia_rango(e: Decimal, lo: int, hi: int) -> Decimal:
    if lo <= e <= hi:
        return Decimal(0)
    return min(abs(e - lo), abs(e - hi))


def _p90(valores: list[Decimal]) -> Decimal:
    orden = sorted(valores)
    return orden[math.ceil(Decimal("0.9") * len(orden)) - 1]


def _mediana(valores: list[Decimal]) -> Decimal:
    orden = sorted(valores)
    n = len(orden)
    return orden[n // 2] if n % 2 else (orden[n // 2 - 1] + orden[n // 2]) / 2


def _resumen(
    nombre: str, m1: list[Decimal], lado: list[Decimal], dos: list[Decimal], sin: int
) -> str:
    if not m1:
        return f"{nombre} | 0 | - | - | - | - | - | - | {sin}"
    dentro = Fraction(sum(1 for d in m1 if d == 0), len(m1))
    t = (
        f"{_n(_mediana(lado))} | {_n(_p90(lado))} | {_n(_mediana(dos))} | {_n(_p90(dos))}"
        if lado
        else "- | - | - | -"
    )
    return (
        f"{nombre} | {len(m1)} | {_n(_mediana(m1))} | {_n(_p90(m1))} | "
        f"{float(dentro) * 100:.1f} % | "
        f"{t} | {sin}"
    )


def main() -> None:
    repo = Path(sys.argv[1]).resolve()
    filas = "--filas" in sys.argv[2:]
    criterio = cargar_criterio(repo)
    config = cargar_config(repo / "knowledge" / "cases" / "kit" / "config.yaml")
    registro = cargar_registro(repo / "knowledge" / "spec" / "parametros.yaml")
    datos = carpeta_datos(repo)
    dias = arnes.dias_de_construccion(repo, criterio, criterio.construccion)
    m1_d: dict[str, list[Decimal]] = defaultdict(list)
    lado_d: dict[str, list[Decimal]] = defaultdict(list)
    dos_d: dict[str, list[Decimal]] = defaultdict(list)
    sin_ticks: dict[str, int] = defaultdict(int)
    sin_m1 = 0
    lineas: list[str] = []
    for d in dias:
        if not d.operaciones:
            continue
        md = mercado_de_construccion(repo, datos, criterio, config, registro, d.id)
        velas = {int(v.inicio): v for v in md.m1}
        for op in d.operaciones:
            mes = d.dia[:7]
            minuto = _minuto(op.instante)
            e = op.entrada * md.escala
            vela = velas.get(minuto)
            if vela is None:
                sin_m1 += 1
                lineas.append(f"{d.dia} | {op.sesion} | {op.direccion} | sin M1 en su minuto")
                continue
            dm1 = _distancia_rango(e, int(vela.minima), int(vela.maxima))
            m1_d[mes].append(dm1)
            desde, hasta = minuto * MS_POR_MINUTO, (minuto + 1) * MS_POR_MINUTO
            ticks = [t for t in md.ticks if desde <= int(t.instante) < hasta]
            if ticks:
                precio = (
                    (lambda t: int(t.bid)) if op.direccion == "venta" else (lambda t: int(t.ask))
                )
                dl = min(abs(e - precio(t)) for t in ticks)
                d2 = min(min(abs(e - int(t.bid)), abs(e - int(t.ask))) for t in ticks)
                lado_d[mes].append(dl)
                dos_d[mes].append(d2)
                tick_txt = f"{_n(dl)} | {_n(d2)}"
            else:
                sin_ticks[mes] += 1
                tick_txt = "sin ticks | sin ticks"
            lineas.append(f"{d.dia} | {op.sesion} | {op.direccion} | {_n(dm1)} | {tick_txt}")
    print("# A-16 medida: la entrada del trader (Oanda, FX Replay) contra Dukascopy, por operacion")
    print(
        f"dias dev con operaciones: {sum(1 for d in dias if d.operaciones)}; operaciones sin M1 en su minuto: {sin_m1}"
    )
    print()
    print(
        "mes | N | mediana M1 | p90 M1 | dentro del rango M1 | mediana tick del lado | p90 tick "
        "del lado | mediana tick dos lados | p90 tick dos lados | sin ticks en su minuto"
    )
    total_m1: list[Decimal] = []
    total_l: list[Decimal] = []
    total_2: list[Decimal] = []
    for mes in sorted(m1_d):
        print(_resumen(mes, m1_d[mes], lado_d[mes], dos_d[mes], sin_ticks[mes]))
        total_m1 += m1_d[mes]
        total_l += lado_d[mes]
        total_2 += dos_d[mes]
    print(_resumen("total", total_m1, total_l, total_2, sum(sin_ticks.values())))
    print()
    if total_m1:
        mediana = _mediana(total_m1)
        dentro = Fraction(sum(1 for d in total_m1 if d == 0), len(total_m1))
        dispara = mediana > UMBRAL_MEDIANA or dentro < UMBRAL_DENTRO
        print(
            "la regla escrita antes de medir (respuesta del consultor, punto 7; ADR-0092 §9): "
            f"mediana M1 {_n(mediana)} frente a {UMBRAL_MEDIANA} puntos, dentro del rango "
            f"{float(dentro) * 100:.1f} % frente a 50 %: "
            + ("SE DISPARA" if dispara else "no se dispara")
        )
    if filas:
        print()
        print("dia | sesion | direccion | distancia M1 | tick del lado | tick dos lados (puntos)")
        print("\n".join(lineas))


if __name__ == "__main__":
    main()
