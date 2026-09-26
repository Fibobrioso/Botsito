"""Integridad de los ticks de construccion: M1 reconstruidas desde ticks frente a las M1 del repo.

Rama `trabajo/ticks-llenado` (ADR-0051, Fase 2). TOLERANCIA FIJADA ANTES DE COMPARAR, y no se toca
despues de ver el resultado:

  una M1 CUADRA si existe en las dos fuentes y |ΔO|, |ΔH|, |ΔL| y |ΔC| son todos <= 2 puntos
  (el margen que A-16 y `instante_llenado.py` ya usan: las series de dos proveedores difieren
  1-2 puntos). Una M1 del repo sin ticks en su minuto, o un minuto con ticks sin M1 en el repo,
  NO cuadra y se cuenta por su tipo. El volumen no se compara (unidades distintas).

La M1 reconstruida de un minuto es BID: abierta = primer BID, maxima = max BID, minima = min BID,
cierre = ultimo BID de los ticks de ese minuto (las M1 del repo son BID, ADR-0005). Solo lee los
datasets de ticks y de M1 de los meses de CONSTRUCCION del criterio: se niega a cualquier otro.
Imprime recuentos y porcentajes; ni un precio ni un instante de operacion.

  `uv run python scripts/ticks_integridad.py --salida <fichero>`
"""

from __future__ import annotations

import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
TOLERANCIA_PUNTOS = 2  # FIJADA ANTES DE COMPARAR


@dataclass(frozen=True)
class Ohlc:
    abierta: int
    maxima: int
    minima: int
    cierre: int


def reconstruir_m1(ticks: list[tuple[int, int]]) -> dict[int, Ohlc]:
    """`(minuto, bid)` en orden -> OHLC BID por minuto. Puro."""
    salida: dict[int, Ohlc] = {}
    for minuto, bid in ticks:
        o = salida.get(minuto)
        if o is None:
            salida[minuto] = Ohlc(bid, bid, bid, bid)
        else:
            salida[minuto] = Ohlc(o.abierta, max(o.maxima, bid), min(o.minima, bid), bid)
    return salida


def comparar(
    repo_m1: dict[int, Ohlc], desde_ticks: dict[int, Ohlc], tolerancia: int = TOLERANCIA_PUNTOS
) -> Counter[str]:
    """Recuento por tipo: cuadra, discrepa (con el peor campo), solo_repo, solo_ticks. Puro."""
    cuenta: Counter[str] = Counter()
    for minuto, r in repo_m1.items():
        t = desde_ticks.get(minuto)
        if t is None:
            cuenta["solo_repo"] += 1
            continue
        deltas = {
            "abierta": abs(r.abierta - t.abierta),
            "maxima": abs(r.maxima - t.maxima),
            "minima": abs(r.minima - t.minima),
            "cierre": abs(r.cierre - t.cierre),
        }
        if max(deltas.values()) <= tolerancia:
            cuenta["cuadra"] += 1
        else:
            peor = max(deltas, key=lambda k: deltas[k])
            cuenta["discrepa"] += 1
            cuenta[f"discrepa_{peor}"] += 1
            cuenta["discrepa_mas_de_10" if deltas[peor] > 10 else "discrepa_hasta_10"] += 1
    cuenta["solo_ticks"] = sum(1 for m in desde_ticks if m not in repo_m1)
    return cuenta


def lineas(mes: str, cuenta: Counter[str], horas_perdidas: int) -> list[str]:
    total = cuenta["cuadra"] + cuenta["discrepa"] + cuenta["solo_repo"]
    pct = 100 * cuenta["cuadra"] / total if total else 0.0
    return [
        f"{mes}: M1 del repo {total}; cuadran {cuenta['cuadra']} ({pct:.2f} %); discrepan "
        f"{cuenta['discrepa']} (hasta 10 puntos {cuenta['discrepa_hasta_10']}, mas de 10 "
        f"{cuenta['discrepa_mas_de_10']}; peor campo: abierta {cuenta['discrepa_abierta']}, "
        f"maxima {cuenta['discrepa_maxima']}, minima {cuenta['discrepa_minima']}, cierre "
        f"{cuenta['discrepa_cierre']}); M1 del repo sin ticks {cuenta['solo_repo']}; minutos con "
        f"ticks sin M1 en el repo {cuenta['solo_ticks']}; horas de ticks perdidas {horas_perdidas}"
    ]


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] != "--salida":
        print("uso: ticks_integridad.py --salida <fichero>", file=sys.stderr)
        return 2
    sys.path.insert(0, str(RAIZ / "src"))
    from botsito.cases.criterio_fidelidad import cargar_criterio
    from botsito.config.ajustes import carpeta_datos
    from botsito.data.dataset import buscar_manifiesto, cargar_manifiesto, cargar_serie
    from botsito.data.ticks import buscar_manifiesto_ticks, cargar_manifiesto_ticks, cargar_ticks
    from botsito.domain.ticks import MS_POR_MINUTO

    datos = carpeta_datos(RAIZ)
    criterio = cargar_criterio(RAIZ)
    salida = [
        f"TOLERANCIA (fijada antes de comparar): |delta| <= {TOLERANCIA_PUNTOS} puntos en O, H, "
        "L y C",
        f"MESES: construccion {', '.join(criterio.construccion)} (solo estos)",
    ]
    total: Counter[str] = Counter()
    perdidas_total = 0
    for mes in criterio.construccion:
        m1 = cargar_serie(cargar_manifiesto(buscar_manifiesto(RAIZ, f"eurusd-m1-{mes}")), datos)
        mt = cargar_manifiesto_ticks(buscar_manifiesto_ticks(RAIZ, f"eurusd-ticks-{mes}"))
        ticks = cargar_ticks(mt, datos)
        salida.append(f"DATASETS {mes}: {m1.origen} frente a {ticks.origen}")
        repo = {int(v.inicio): Ohlc(v.abierta, v.maxima, v.minima, v.cierre) for v in m1.velas}
        desde = reconstruir_m1([(t.instante // MS_POR_MINUTO, int(t.bid)) for t in ticks.ticks])
        cuenta = comparar(repo, desde)
        salida += lineas(mes, cuenta, len(ticks.horas_perdidas))
        total.update(cuenta)
        perdidas_total += len(ticks.horas_perdidas)
    salida += lineas("total", total, perdidas_total)
    Path(argv[1]).write_text("\n".join(salida) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(salida))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
