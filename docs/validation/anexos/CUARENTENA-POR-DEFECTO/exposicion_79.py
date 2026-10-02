"""La comprobacion 1a sobre los 79 items que kb ocultaba con el criterio de la cuarta y la quinta orden.

Sexta orden del consultor (2026-10-01), punto 2: «Antes de cambiar nada, pasa la comprobación 1a a
los 79 ítems e imprime solo, para cada uno, el id, el motivo actual y True o False». Se ejecuto con
el codigo de `bc77e2b`, ANTES del cambio de criterio. No escribe nada.

Sigue reproduciendose con el codigo de `0faa9ae`, que restringe `_evidencia_que_copia` a (b):
el unico de los 79 que entraba por copia es de (b). Medido el 2026-10-01 (revisor, tercera
pasada, A2): la salida de los dos es identica byte a byte.

Los 79 son los que ocultaba `construir_indice` en `bc77e2b`: su cita pisa un segmento oculto
(`cuarentena.items_ocultos`) o su texto lo copia (`indice._evidencia_que_copia`). True si trae una
fecha (dia y mes, `cuarentena.fechas_en`) que es un dia de `casos_ocultos`, mirada en TRES sitios:
- los segmentos OCULTOS que su cita pisa o que su texto copia: el propio filtro lo anota al ocultar
  (`Filtro.dias`, `Oculto.fecha_vigilada`), y del texto solo sale el booleano;
- los segmentos VISIBLES que su cita pisa (la cruda filtrada);
- el texto del propio item (cita, afirmacion, valor y notas).
Imprime solo el id, el motivo y True o False: nunca el texto ni la fecha.

    uv run python docs/validation/anexos/CUARENTENA-POR-DEFECTO/exposicion_79.py
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
    fechas_en,
    items_ocultos,
)
from botsito.corpus.manifiestos_transcripcion import activos, cargar_todos, carpeta_de
from botsito.corpus.pipeline_transcripcion import FICHERO_CRUDA, cargar_cruda
from botsito.evidence.modelo import cargar_evidencia
from botsito.retrieval.indice import _evidencia_que_copia, _texto_del_item

RAIZ = Path(__file__).resolve().parents[4]


def main() -> int:
    tramos = cargar_tramos_no_citables(RAIZ)
    dias = dias_de_casos(casos_ocultos(RAIZ))
    if "--control" in sys.argv:
        # CONTROL POSITIVO: todos los dias del año como si fueran reservados. Solo dice si la via
        # puede dar True sobre estos items; las filas no se miran, solo el TOTAL.
        dias = frozenset((m, d) for m in range(1, 13) for d in range(1, 32))
    datos = _carpeta_datos(RAIZ)
    items = cargar_evidencia(RAIZ / "knowledge" / "evidence")
    print("| Item | Motivo actual | Dia de casos_ocultos |")
    print("|---|---|---|")
    total = verdaderos = 0
    for t in activos(cargar_todos(RAIZ)):
        carpeta = carpeta_de(datos, t)
        if not (carpeta / FICHERO_CRUDA).is_file():
            continue
        filtro = Filtro(t.video_id, tramos.get(t.video_id, ()), dias=dias)
        visibles = cargar_cruda(carpeta, filtro)  # anota lo oculto y si trae un dia
        de_video = {it.id: it for it in items if it.video_id == t.video_id}
        por_cita = items_ocultos(filtro, [(i.id, i.t0_ms, i.t1_ms) for i in de_video.values()])
        resto = [it for it in de_video.values() if it.id not in por_cita]
        por_copia = _evidencia_que_copia(datos, t, filtro, resto)
        for iid, o in sorted({**por_cita, **por_copia}.items()):
            it = de_video[iid]
            en_visibles = any(
                fechas_en(s.texto) & dias
                for s in visibles
                if s.t1_ms > it.t0_ms and s.t0_ms < it.t1_ms
            )
            propio = bool(fechas_en(_texto_del_item(it)) & dias)
            dia = o.fecha_vigilada or en_visibles or propio
            print(f"| {iid} | ({o.motivo}) | {dia} |")
            total += 1
            verdaderos += dia
    print(f"TOTAL: {total}; con un dia de casos_ocultos: {verdaderos}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
