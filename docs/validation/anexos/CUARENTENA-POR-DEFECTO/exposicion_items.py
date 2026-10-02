"""¿El segmento que cita cada item afectado trae una fecha que es un dia de `casos_ocultos`?

Orden del consultor del 2026-10-01 (cuarta orden, punto 1a): «Para cada ítem, comprueba por código
si el segmento citado contiene una fecha que sea un día de casos_ocultos. Imprime solo el id del
ítem y True o False, nunca el texto ni la fecha». No escribe nada.

Los items son los que `auditoria_knowledge.py` encuentra (su intervalo pisa un segmento que hoy se
oculta por (b) o (c)). La comprobacion la hace el propio filtro al ocultar
(`Filtro.dias` y `Oculto.fecha_vigilada`): lee por `cargar_cruda` FILTRADA, y lo unico que sale
del texto es un booleano por segmento.

Uso: uv run python docs/validation/anexos/CUARENTENA-POR-DEFECTO/exposicion_items.py
"""

from __future__ import annotations

import sys
from pathlib import Path

from botsito.cases.holdout import casos_ocultos
from botsito.cli import _carpeta_datos
from botsito.corpus.cuarentena import (
    MOTIVO_SESION,
    Filtro,
    cargar_tramos_no_citables,
    dias_de_casos,
)
from botsito.corpus.manifiestos_transcripcion import cargar_todos, carpeta_de
from botsito.corpus.pipeline_transcripcion import FICHERO_CRUDA, cargar_cruda
from botsito.evidence.modelo import cargar_evidencia

RAIZ = Path(__file__).resolve().parents[4]


def main() -> int:
    tramos = cargar_tramos_no_citables(RAIZ)
    dias = dias_de_casos(casos_ocultos(RAIZ))
    datos = _carpeta_datos(RAIZ)
    filtros: dict[str, Filtro] = {}
    for t in cargar_todos(RAIZ):
        carpeta = carpeta_de(datos, t)
        if (carpeta / FICHERO_CRUDA).is_file():
            filtro = Filtro(t.video_id, tramos.get(t.video_id, ()), dias=dias)
            cargar_cruda(carpeta, filtro)  # el filtro anota lo que oculta y si trae un dia
            filtros[t.id] = filtro
    print("| Item | Fecha de un dia de casos_ocultos |")
    print("|---|---|")
    for it in sorted(cargar_evidencia(RAIZ / "knowledge" / "evidence"), key=lambda i: i.id):
        filtro = filtros.get(it.transcripcion or "")
        if filtro is None:
            continue
        citados = [o for o in filtro.ocultos_entre(it.t0_ms, it.t1_ms) if o.motivo != MOTIVO_SESION]
        if citados:
            print(f"| {it.id} | {any(o.fecha_vigilada for o in citados)} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
