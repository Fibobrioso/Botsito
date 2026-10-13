"""El spread de los ticks de construccion por hora de la ventana del trader (ADR-0051 §6, Fase 2).

Para cada hora NOMINAL de la ventana, de `ventana_inicio` a `ventana_fin` (07:00-15:00 hoy, leidas
del registro), sobre TODOS los ticks de los datasets de construccion: numero de ticks, media,
percentiles 50, 90 y 99 del spread (ASK - BID, en puntos), por mes y en total; y lo mismo fuera de
la ventana. El percentil 90 por hora es lo que `knowledge/simulador/llenado.yaml` toma como spread
supuesto sin ticks (DECISION NOCTURNA 4, conservadora). Recorre los meses de `construccion` de
`criterio_fidelidad.yaml` y ninguno mas, y exige los ticks de cada uno: si a un mes le falta su
manifiesto, sale con 2 nombrandolo, sin medir nada. Imprime recuentos y puntos; nada de operaciones.

**LA HORA SALE DEL RELOJ DE LAS SESIONES** (ADR-0069 §5; `trabajo/entrada-enero`, X): cada tick se
lee con `reloj_de_las_sesiones` -con `rejilla_h4`, la hora nominal que marca la rejilla H4 de
`anclaje_h4`-, la misma puerta con que el motor y `cases/` cuentan la ventana. Hasta esa rama se
leia la hora de pared de `huso_operativa`, que coincide con la rejilla salvo los dias en que Europa
y EE. UU. no han cambiado la hora a la vez (en 2026, del 9 al 27 de marzo y del 26 al 30 de
octubre): esos dias la hora salia corrida una hora. `tests/unit/test_ticks_spread.py` lo rompe a
proposito con un dia de desfase.

  `uv run python scripts/ticks_spread.py --salida <fichero>`
"""

from __future__ import annotations

import sys
from collections import defaultdict
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Protocol

RAIZ = Path(__file__).resolve().parents[1]
FUERA = "fuera"
MS_POR_MINUTO = 60_000
MINUTOS_POR_HORA = 60


class Reloj(Protocol):
    """Lo que se le pide al reloj de las sesiones: de un minuto UTC a (dia, minutos nominales)."""

    def lectura(self, instante: int) -> tuple[object, int]: ...


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


def clave_de_hora(reloj: Reloj, inicio: int, fin: int) -> Callable[[int], str]:
    """De un instante en milisegundos UTC a su clave: la hora nominal «HH» que marca `reloj` si
    cae en [`inicio`, `fin`), y `FUERA` si no. La lectura se guarda por minuto: todos los ticks de
    un minuto caen en la misma hora, y asi la rejilla se calcula una vez por minuto, no por tick."""
    por_minuto: dict[int, str] = {}

    def clave(instante_ms: int) -> str:
        minuto = instante_ms // MS_POR_MINUTO
        if minuto not in por_minuto:
            _, minutos = reloj.lectura(minuto)
            hora = minutos // MINUTOS_POR_HORA
            por_minuto[minuto] = f"{hora:02d}" if inicio <= hora < fin else FUERA
        return por_minuto[minuto]

    return clave


def main(argv: list[str], raiz: Path = RAIZ) -> int:
    if len(argv) != 2 or argv[0] != "--salida":
        print("uso: ticks_spread.py --salida <fichero>", file=sys.stderr)
        return 2
    sys.path.insert(0, str(RAIZ / "src"))
    from botsito.cases.criterio_fidelidad import cargar_criterio
    from botsito.config.ajustes import carpeta_datos
    from botsito.config.registro import cargar_registro
    from botsito.data.ticks import (
        TicksError,
        buscar_manifiesto_ticks,
        cargar_manifiesto_ticks,
        cargar_ticks,
    )
    from botsito.engine.relojes import reloj_de_las_sesiones

    criterio = cargar_criterio(raiz)
    manifiestos: dict[str, Path] = {}
    for mes in criterio.construccion:
        try:
            manifiestos[mes] = buscar_manifiesto_ticks(raiz, f"eurusd-ticks-{mes}")
        except TicksError as exc:
            print(
                f"ERROR: {mes} es de construccion y no tiene ticks ({exc}); no se mide nada",
                file=sys.stderr,
            )
            return 2
    datos = carpeta_datos(raiz)
    registro = cargar_registro(raiz / "knowledge" / "spec" / "parametros.yaml")
    reloj = reloj_de_las_sesiones(registro)
    inicio = registro.hora("ventana_inicio").minutos_del_dia // MINUTOS_POR_HORA
    fin = registro.hora("ventana_fin").minutos_del_dia // MINUTOS_POR_HORA
    por_hora: dict[str, dict[str, list[int]]] = defaultdict(lambda: defaultdict(list))
    salida = [
        f"VENTANA: horas nominales [{inicio:02d}, {fin:02d}) del reloj de las sesiones "
        f"({reloj.opcion}, ADR-0069 §5); spread = ASK - BID en puntos; percentiles por rango "
        f"mas cercano",
        f"MESES: construccion {', '.join(criterio.construccion)} (solo estos)",
    ]
    for mes in criterio.construccion:
        serie = cargar_ticks(cargar_manifiesto_ticks(manifiestos[mes]), datos)
        salida.append(f"DATASET {mes}: {serie.origen}; ticks {len(serie.ticks)}")
        clave = clave_de_hora(reloj, inicio, fin)
        for t in serie.ticks:
            k = clave(t.instante)
            por_hora[mes][k].append(t.spread)
            por_hora["total"][k].append(t.spread)
    for mes in (*criterio.construccion, "total"):
        for k in sorted(por_hora[mes]):
            etiqueta = f"{mes} {k}" if k == FUERA else f"{mes} {k}:00"
            salida.append(linea(etiqueta, resumen(por_hora[mes][k])))
    salida.append("P90 POR HORA (total), para knowledge/simulador/llenado.yaml:")
    for k in sorted(por_hora["total"]):
        salida.append(f"  {k}: {resumen(por_hora['total'][k])['p90']}")
    Path(argv[1]).write_text("\n".join(salida) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(salida))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
