"""El spread de los ticks de construccion por hora de la ventana del trader (ADR-0051 §6, Fase 2).

Para cada hora local de `huso_operativa` entre `ventana_inicio` y `ventana_fin` (07:00-15:00 hoy,
leidas del registro), sobre TODOS los ticks de los datasets de construccion: numero de ticks,
media, percentiles 50, 90 y 99 del spread (ASK - BID, en puntos), por mes y en total; y lo mismo
fuera de la ventana. El percentil 90 por hora es lo que `knowledge/simulador/llenado.yaml` toma
como spread supuesto sin ticks (DECISION NOCTURNA 4, conservadora). Se niega a cualquier mes que
no sea de construccion. Imprime recuentos y puntos; nada de operaciones.

  `uv run python scripts/ticks_spread.py --salida <fichero>`
"""

from __future__ import annotations

import sys
from collections import defaultdict
from collections.abc import Sequence
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
FUERA = "fuera"


def percentil(valores: Sequence[int], p: float) -> int:
    """Percentil por rango mas cercano sobre la lista ORDENADA. Puro."""
    if not valores:
        raise ValueError("sin valores")
    i = max(0, min(len(valores) - 1, round(p * (len(valores) - 1))))
    return valores[i]


def resumen(valores: Sequence[int]) -> dict[str, float | int]:
    ordenados = sorted(valores)
    return {
        "n": len(ordenados),
        "media": sum(ordenados) / len(ordenados),
        "p50": percentil(ordenados, 0.50),
        "p90": percentil(ordenados, 0.90),
        "p99": percentil(ordenados, 0.99),
        "max": ordenados[-1],
    }


def linea(etiqueta: str, r: dict[str, float | int]) -> str:
    return (
        f"{etiqueta}: n {r['n']}, media {r['media']:.2f}, p50 {r['p50']}, p90 {r['p90']}, "
        f"p99 {r['p99']}, max {r['max']}"
    )


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] != "--salida":
        print("uso: ticks_spread.py --salida <fichero>", file=sys.stderr)
        return 2
    sys.path.insert(0, str(RAIZ / "src"))
    from datetime import UTC, datetime, timedelta

    from botsito.cases.criterio_fidelidad import cargar_criterio
    from botsito.comun.husos import huso_canonico
    from botsito.config.ajustes import carpeta_datos
    from botsito.config.registro import cargar_registro
    from botsito.data.ticks import buscar_manifiesto_ticks, cargar_manifiesto_ticks, cargar_ticks

    datos = carpeta_datos(RAIZ)
    criterio = cargar_criterio(RAIZ)
    registro = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
    huso = huso_canonico(registro.texto("huso_operativa"))
    inicio = registro.hora("ventana_inicio").minutos_del_dia // 60
    fin = registro.hora("ventana_fin").minutos_del_dia // 60
    epoca = datetime(1970, 1, 1, tzinfo=UTC)
    por_hora: dict[str, dict[str, list[int]]] = defaultdict(lambda: defaultdict(list))
    salida = [
        f"VENTANA: horas locales [{inicio:02d}, {fin:02d}) en {registro.texto('huso_operativa')}; "
        f"spread = ASK - BID en puntos; percentiles por rango mas cercano",
        f"MESES: construccion {', '.join(criterio.construccion)} (solo estos)",
    ]
    for mes in criterio.construccion:
        mt = cargar_manifiesto_ticks(buscar_manifiesto_ticks(RAIZ, f"eurusd-ticks-{mes}"))
        serie = cargar_ticks(mt, datos)
        salida.append(f"DATASET {mes}: {serie.origen}; ticks {len(serie.ticks)}")
        for t in serie.ticks:
            local = (epoca + timedelta(milliseconds=t.instante)).astimezone(huso)
            clave = f"{local.hour:02d}" if inicio <= local.hour < fin else FUERA
            por_hora[mes][clave].append(t.spread)
            por_hora["total"][clave].append(t.spread)
    for mes in (*criterio.construccion, "total"):
        for clave in sorted(por_hora[mes]):
            etiqueta = f"{mes} {clave}" if clave == FUERA else f"{mes} {clave}:00"
            salida.append(linea(etiqueta, resumen(por_hora[mes][clave])))
    salida.append("P90 POR HORA (total), para knowledge/simulador/llenado.yaml:")
    for clave in sorted(por_hora["total"]):
        salida.append(f"  {clave}: {resumen(por_hora['total'][clave])['p90']}")
    Path(argv[1]).write_text("\n".join(salida) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(salida))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
