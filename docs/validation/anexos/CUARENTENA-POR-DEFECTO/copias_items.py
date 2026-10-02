"""Los items de evidencia que COPIAN el texto de un segmento oculto sin que su cita lo pise.

Quinta orden del consultor (2026-10-01): kb los oculta por contenido, «y se repite la comprobacion
1a sobre estos dos (id y True/False)». Este anexo lista TODOS los que el criterio encuentra en el
repositorio real (no solo los dos que midio `citas_de_salidas.py`) y, para cada uno, si el segmento
oculto que copia trae una fecha que es un dia de `casos_ocultos`. Imprime solo el id, el motivo y
True o False: nunca el texto ni la fecha. No escribe nada.

La lectura de la cruda entera la hace la funcion AUTORIZADA del indice
(`botsito.retrieval.indice._evidencia_que_copia`), que devuelve ids y motivos; el booleano lo pone
el propio filtro (`Filtro.dias`, `Oculto.fecha_vigilada`).

Uso: uv run python docs/validation/anexos/CUARENTENA-POR-DEFECTO/copias_items.py
"""

from __future__ import annotations

import sys
from pathlib import Path

from botsito.cases.holdout import casos_ocultos
from botsito.cli import _carpeta_datos
from botsito.corpus.cuarentena import (
    Filtro,
    cargar_tramos_no_citables,
    dias_de_casos,
    items_ocultos,
)
from botsito.corpus.manifiestos_transcripcion import activos, cargar_todos, carpeta_de
from botsito.corpus.pipeline_transcripcion import FICHERO_CRUDA, cargar_cruda
from botsito.evidence.modelo import cargar_evidencia
from botsito.retrieval.indice import _evidencia_que_copia

RAIZ = Path(__file__).resolve().parents[4]


def main() -> int:
    tramos = cargar_tramos_no_citables(RAIZ)
    dias = dias_de_casos(casos_ocultos(RAIZ))
    datos = _carpeta_datos(RAIZ)
    items = cargar_evidencia(RAIZ / "knowledge" / "evidence")
    print("| Item | Motivo | Fecha de un dia de casos_ocultos |")
    print("|---|---|---|")
    total = 0
    for t in activos(cargar_todos(RAIZ)):
        carpeta = carpeta_de(datos, t)
        if not (carpeta / FICHERO_CRUDA).is_file():
            continue
        filtro = Filtro(t.video_id, tramos.get(t.video_id, ()), dias=dias)
        cargar_cruda(carpeta, filtro)  # el filtro anota lo que oculta y si trae un dia
        de_video = [it for it in items if it.video_id == t.video_id]
        por_cita = items_ocultos(filtro, [(it.id, it.t0_ms, it.t1_ms) for it in de_video])
        resto = [it for it in de_video if it.id not in por_cita]
        for iid, o in sorted(_evidencia_que_copia(datos, t, filtro, resto).items()):
            print(f"| {iid} | {o.motivo} | {o.fecha_vigilada} |")
            total += 1
    print(f"TOTAL: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
