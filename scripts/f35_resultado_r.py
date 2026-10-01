"""El resultado por operacion en R del bot frente al del trader, en los mismos dias de construccion
(docs/validation/F35-ORDEN-STOP-PIVOTE.md §5). DIAGNOSTICO: no es fidelidad.

- BOT: los llenados del JSON de `scripts/embudo_77.py` (modo de la vida de la orden stop), con su R
  sobre el stop inicial.
- TRADER: `scripts/viabilidad_trader.py` (`medir`), las mismas 77 operaciones de construccion en sus
  dos series: ANOTADA, la salida real del libro, y SIMULADA, repetida por el broker sobre ticks. Son
  dias `dev`: su detalle se lee sin puerta (ADR-0037), y es lo que ya leyo VIABILIDAD-TRADER.md.

Da, por mes y en total: los cuartiles de R, el porcentaje de ganadoras y la proporcion de compras y
ventas; y lo mismo solo en los dias en que operan los dos. Solo lee; escribe SOLO en --salida.

    uv run python scripts/f35_resultado_r.py --embudo <json del embudo> --salida <fichero> [--raiz]
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

RAIZ_SCRIPT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ_SCRIPT / "src"))
sys.path.insert(0, str(RAIZ_SCRIPT / "scripts"))


def cuartiles(xs: Sequence[float]) -> str:
    if not xs:
        return "sin datos"
    s = sorted(xs)

    def q(f: float) -> float:
        return s[min(len(s) - 1, int(f * (len(s) - 1) + 0.5))]

    ganadoras = sum(1 for x in s if x > 0)
    return (
        f"n {len(s)}; min {s[0]:.2f}; Q1 {q(0.25):.2f}; mediana {q(0.5):.2f}; Q3 {q(0.75):.2f}; "
        f"max {s[-1]:.2f}; media {sum(s) / len(s):+.2f}; ganadoras {ganadoras} "
        f"({100 * ganadoras / len(s):.0f} %)"
    )


def bloque(titulo: str, bot: list[dict[str, Any]], trader: list[dict[str, Any]]) -> list[str]:
    compras_b = sum(1 for x in bot if x["lado"] == "compra")
    compras_t = sum(1 for x in trader if x["direccion"] == "compra")
    return [
        f"## {titulo}",
        "BOT: " + cuartiles([x["r"] for x in bot if x["r"] is not None]),
        "TRADER, ANOTADA (el libro): " + cuartiles([x["r_anotada"] for x in trader]),
        "TRADER, SIMULADA (broker): "
        + cuartiles([x["r_simulada"] for x in trader if x["r_simulada"] is not None]),
        f"compras / ventas: BOT {compras_b} / {len(bot) - compras_b}; TRADER {compras_t} / "
        f"{len(trader) - compras_t}",
        "",
    ]


def main(argv: Sequence[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--embudo", type=Path, required=True)
    p.add_argument("--raiz", type=Path, default=RAIZ_SCRIPT)
    p.add_argument("--salida", type=Path, required=True)
    args = p.parse_args(argv)
    import viabilidad_trader

    resumen = json.loads(args.embudo.read_text(encoding="utf-8"))["resumen"]
    if resumen.get("modo") != "vida":
        print("el JSON no es del embudo de la vida de la orden stop")
        return 2
    bot = list(resumen["llenados"])
    trader = list(viabilidad_trader.medir(args.raiz.resolve())["por_operacion"])
    dias_bot = {x["dia"] for x in bot}
    dias_trader = {x["dia"] for x in trader}
    comunes = dias_bot & dias_trader
    lineas = [
        "# Resultado por operacion en R: el bot frente al trader (DIAGNOSTICO, no es fidelidad)",
        "cuenta del bot: "
        + ("REINICIADA CADA DIA" if resumen.get("cuenta_diaria") else "arrastrada entre dias"),
        f"dias con operaciones: BOT {len(dias_bot)}, TRADER {len(dias_trader)}, los dos "
        f"{len(comunes)}",
        "",
        *bloque("Todos los dias de construccion", bot, trader),
    ]
    for mes in sorted({x["dia"][:7] for x in trader}):
        lineas += bloque(
            f"Solo {mes}",
            [x for x in bot if x["dia"].startswith(mes)],
            [x for x in trader if x["dia"].startswith(mes)],
        )
    lineas += bloque(
        "Solo los dias en que operan los dos",
        [x for x in bot if x["dia"] in comunes],
        [x for x in trader if x["dia"] in comunes],
    )
    args.salida.write_text("\n".join(lineas) + "\n", encoding="utf-8", newline="\n")
    print(f"OK: {args.salida}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
