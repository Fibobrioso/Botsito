"""Cuanto oculta la cuarentena, por video y en las propuestas (`trabajo/cuarentena-por-defecto`).

Orden del consultor (2026-10-01): «por cada video: total de segmentos, cuantos oculta (a), (b) y
(c), y el porcentaje. Solo numeros, nunca contenido ni que mes o dia disparo la regla»; y la
auditoria de `knowledge/_proposals/`: «cuantos ficheros y segmentos caen en (a), (b) o (c). Solo
cuentas y nombres de fichero, sin imprimir contenido. No los borres ni los edites».

No escribe nada. Lee por las MISMAS funciones que la CLI, FILTRADAS: el texto de lo oculto no sale
de `cargar_cruda`, y este guion solo cuenta `Filtro.ocultos`, que no lleva texto. Las propuestas
se cuentan con `Filtro.motivos`, que solo devuelve posiciones y motivos.

Uso: uv run python docs/validation/anexos/CUARENTENA-POR-DEFECTO/recuento.py
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

from botsito.cli import _carpeta_datos
from botsito.corpus.cuarentena import Filtro, cargar_tramos_no_citables
from botsito.corpus.manifiestos_transcripcion import activos, cargar_todos, carpeta_de
from botsito.corpus.pipeline_transcripcion import FICHERO_CRUDA, cargar_cruda
from botsito.evidence.propuestas import DIRECTORIO_PROPUESTAS, cargar_propuestas

RAIZ = Path(__file__).resolve().parents[4]


def _pct(n: int, total: int) -> str:
    return f"{100 * n / total:.1f} %" if total else "-"


def main() -> int:
    tramos = cargar_tramos_no_citables(RAIZ)
    datos = _carpeta_datos(RAIZ)
    print("| Video | Segmentos | (a) | (b) | (c) | Ocultos | % |")
    print("|---|---|---|---|---|---|---|")
    transcripciones = sorted(activos(cargar_todos(RAIZ)), key=lambda t: int(t.video_id[1:]))
    for t in transcripciones:
        carpeta = carpeta_de(datos, t)
        if not (carpeta / FICHERO_CRUDA).is_file():
            print(f"| {t.video_id} | no esta en esta maquina | | | | | |")
            continue
        filtro = Filtro(t.video_id, tramos.get(t.video_id, ()))
        visibles = cargar_cruda(carpeta, filtro)
        cuenta = Counter(o.motivo for o in filtro.ocultos.values())
        ocultos = sum(cuenta.values())
        total = len(visibles) + ocultos
        print(
            f"| {t.video_id} | {total} | {cuenta['a']} | {cuenta['b']} | {cuenta['c']} | "
            f"{ocultos} | {_pct(ocultos, total)} |"
        )
    print()
    propuestas = cargar_propuestas(RAIZ / DIRECTORIO_PROPUESTAS)
    print(f"Propuestas en {DIRECTORIO_PROPUESTAS}: {len(propuestas)} ficheros")
    print("| Fichero | Segmentos | (a) | (b) | (c) |")
    print("|---|---|---|---|---|")
    con_algo = 0
    for doc in propuestas:
        segmentos = [SimpleNamespace(**s) for s in doc["contexto"]["segmentos"]]
        filtro = Filtro(str(doc["video_id"]), tramos.get(str(doc["video_id"]), ()))
        cuenta = Counter(filtro.motivos(segmentos).values())
        if cuenta:
            con_algo += 1
            print(
                f"| {doc['propuesta_id']}.yaml | {len(segmentos)} | {cuenta['a']} | "
                f"{cuenta['b']} | {cuenta['c']} |"
            )
    print(f"Ficheros con algun segmento en (a), (b) o (c): {con_algo} de {len(propuestas)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
