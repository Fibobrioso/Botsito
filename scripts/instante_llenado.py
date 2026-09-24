"""¿El instante del xlsx es el LLENADO o la COLOCACION de la orden? Medida con control.

Documento: `docs/validation/CRITERIO-FIDELIDAD.md`, §1 (2026-09-24, rama
`trabajo/criterio-fidelidad`).
Regla fijada ANTES de medir, por el consultor:

  una operacion esta DENTRO si su entrada cae en [minima - 2, maxima + 2] puntos de la vela M1 de
  su instante (redondeado hacia abajo al minuto, porque el xlsx trae segundos y los datos son M1);
  >= 90 % dentro -> LLENADO; <= 50 % -> COLOCACION; entre medias -> se pregunta al trader.

  CONTROL: el mismo instante desplazado -30 y +30 min. Ahi la tasa tiene que CAER claramente; si no
  cae, el test no discrimina y el resultado no vale.

No es del todo independiente: el mismo test ([minima - 2, maxima + 2] sobre la M1) fijo el huso de
los libros (ADR-0039). Lo nuevo es el control.

  `uv run python scripts/instante_llenado.py --salida <fichero>`

Solo lee los `caso-*.yaml` de `knowledge/cases/dev/` y las velas M1 de sus meses (leer velas no es
abrir, ADR-0021 §1). Imprime SOLO tasas: ni precios ni instantes.
"""

from __future__ import annotations

import sys
from collections import defaultdict
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
MARGEN_PUNTOS = 2
DESPLAZAMIENTOS = {"instante": 0, "-30 min": -30, "+30 min": 30}
LLENADO, COLOCACION = Decimal("0.90"), Decimal("0.50")


@dataclass(frozen=True)
class Operacion:
    mes: str
    instante: datetime
    entrada_puntos: int


@dataclass(frozen=True)
class Rango:
    minima: int
    maxima: int


def minuto(instante: datetime) -> datetime:
    return instante.replace(second=0, microsecond=0)


def tasas(
    operaciones: Iterable[Operacion],
    vela_de: Callable[[str, datetime], Rango | None],
    margen: int = MARGEN_PUNTOS,
    desplazamientos: Mapping[str, int] = DESPLAZAMIENTOS,
) -> dict[tuple[str, str], tuple[int, int, int]]:
    """`(mes|"total", desplazamiento) -> (dentro, total, sin_vela)`.

    Puro: la vela la da quien llama."""
    cuenta: dict[tuple[str, str], list[int]] = defaultdict(lambda: [0, 0, 0])
    for op in operaciones:
        for nombre, dmin in desplazamientos.items():
            vela = vela_de(op.mes, minuto(op.instante + timedelta(minutes=dmin)))
            for clave in ((op.mes, nombre), ("total", nombre)):
                cuenta[clave][1] += 1
                if vela is None:
                    cuenta[clave][2] += 1
                elif vela.minima - margen <= op.entrada_puntos <= vela.maxima + margen:
                    cuenta[clave][0] += 1
    return {k: (v[0], v[1], v[2]) for k, v in cuenta.items()}


def veredicto(cuenta: Mapping[tuple[str, str], tuple[int, int, int]]) -> str:
    """La regla fijada, sobre el total. El control manda primero: si no cae, no vale nada."""
    dentro, total, _ = cuenta[("total", "instante")]
    tasa = Decimal(dentro) / Decimal(total)
    controles = [Decimal(cuenta[("total", n)][0]) / Decimal(cuenta[("total", n)][1])
                 for n in DESPLAZAMIENTOS if n != "instante"]  # fmt: skip
    if any(c >= COLOCACION for c in controles) or any(c >= tasa for c in controles):
        return "la medida NO VALE: el control no cae, el test no discrimina"
    if tasa >= LLENADO:
        return "LLENADO"
    if tasa <= COLOCACION:
        return "COLOCACION"
    return "INDECISO: se pregunta al trader"


def lineas(cuenta: Mapping[tuple[str, str], tuple[int, int, int]]) -> list[str]:
    salida: list[str] = []
    for mes in sorted({m for m, _ in cuenta}, key=lambda m: (m == "total", m)):
        partes = []
        for nombre in DESPLAZAMIENTOS:
            d, n, s = cuenta[(mes, nombre)]
            sin = f" ({s} sin vela)" if s else ""
            partes.append(f"{nombre}: {d}/{n} = {Decimal(100 * d) / Decimal(n):.1f} %{sin}")
        salida.append(f"{mes}: " + " | ".join(partes))
    salida.append(f"== VEREDICTO (regla fijada): {veredicto(cuenta)}")
    return salida


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] != "--salida":
        print("uso: instante_llenado.py --salida <fichero>", file=sys.stderr)
        return 2
    sys.path.insert(0, str(RAIZ / "src"))
    from botsito.comun.yaml_estricto import leer_yaml
    from botsito.config.ajustes import carpeta_datos
    from botsito.data.dataset import buscar_manifiesto, cargar_manifiesto, cargar_serie
    from botsito.data.velas import a_minuto

    datos = carpeta_datos(RAIZ)
    series: dict[str, tuple[dict[int, Rango], int, str]] = {}

    def serie(mes: str) -> tuple[dict[int, Rango], int, str]:
        if mes not in series:
            ruta = buscar_manifiesto(RAIZ, f"eurusd-m1-{mes}")
            s = cargar_serie(cargar_manifiesto(ruta), datos)
            series[mes] = ({v.inicio: Rango(v.minima, v.maxima) for v in s.velas}, s.escala,
                           ruta.stem)  # fmt: skip
        return series[mes]

    def vela_de(mes: str, instante: datetime) -> Rango | None:
        return serie(mes)[0].get(a_minuto(instante))

    operaciones = []
    for f in sorted((RAIZ / "knowledge" / "cases" / "dev").glob("caso-*.yaml")):
        caso = leer_yaml(f)
        mes = str(caso["dia"])[:7]
        escala = serie(mes)[1]
        for op in caso["operaciones"]:
            operaciones.append(
                Operacion(
                    mes,
                    datetime.fromisoformat(str(op["instante_utc"])),
                    int(Decimal(str(op["entrada"])) * escala),
                )
            )
    cuenta = tasas(operaciones, vela_de)
    cabecera = [f"DATASETS: {', '.join(series[m][2] for m in sorted(series))}"]
    texto = "\n".join([*cabecera, *lineas(cuenta)]) + "\n"
    Path(argv[1]).write_text(texto, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
