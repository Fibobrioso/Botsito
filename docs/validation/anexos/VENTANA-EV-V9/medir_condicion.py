"""La condicion del punto e (decision del consultor del 2026-10-05, punto 5), medida sobre el repo
ANTES de activarla en `knowledge validate`, con el item ya corregido: cuantos items ACTIVOS (los que
ningun otro supersede), de todos los videos, tienen una ventana declarada que se solapa mas de 0 ms
con un tramo no citable de su video o con un segmento de su transcripcion que solapa un tramo.

Usa `ventana_no_citable` (`evidence/verificacion.py`) sobre el contexto de `knowledge validate`
(`construir_contexto`); los segmentos salen por `contexto.crudas`, el llamador autorizado, y de
ellos solo se usan `n`, `t0_ms` y `t1_ms`. Imprime ids, videos y milisegundos: nunca texto.

Uso: uv run python docs/validation/anexos/VENTANA-EV-V9/medir_condicion.py
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from botsito.corpus.inventario import cargar_manifiesto
from botsito.evidence.modelo import cargar_evidencia
from botsito.evidence.verificacion import ventana_no_citable
from botsito.validation.contexto_evidencia import construir_contexto
from botsito.validation.knowledge import _carpeta_datos

RAIZ = Path(__file__).resolve().parents[4]


def main() -> None:
    items = cargar_evidencia(RAIZ / "knowledge" / "evidence")
    ruta_manifiesto = RAIZ / "knowledge" / "corpus" / "manifest.yaml"
    manifiesto = cargar_manifiesto(ruta_manifiesto) if ruta_manifiesto.exists() else None
    contexto, _temas = construir_contexto(RAIZ, _carpeta_datos(RAIZ), manifiesto)
    supersedidos = {it.supersede for it in items if it.supersede}
    activos = [it for it in items if it.id not in supersedidos]
    print(f"items: {len(items)}; activos: {len(activos)}; supersedidos: {sorted(supersedidos)}")
    con_tramos = sorted(contexto.tramos_no_citables)
    print(f"videos con tramos no citables: {con_tramos}")
    fallan: list[str] = []
    sin_cruda: Counter[str] = Counter()
    for it in activos:
        segmentos = None
        if it.transcripcion is not None and contexto.crudas is not None:
            segmentos = contexto.crudas(it.transcripcion)
            if segmentos is None and contexto.tramos_no_citables.get(it.video_id):
                sin_cruda[it.transcripcion] += 1
        if ventana_no_citable(contexto, it.video_id, it.t0_ms, it.t1_ms, segmentos) is not None:
            fallan.append(it.id)
    print(f"activos con la cruda ausente (solo se mira el tramo): {dict(sin_cruda) or 'ninguno'}")
    print(f"ACTIVOS QUE INCUMPLEN LA CONDICION: {len(fallan)}")
    for i in fallan:
        it = next(x for x in activos if x.id == i)
        print(f"  {i} ({it.video_id}, {it.t0_ms}-{it.t1_ms} ms)")
    viejo = next(x for x in items if x.id == "ev-v9-003456-9ef48fb5")
    segs = contexto.crudas(viejo.transcripcion) if viejo.transcripcion and contexto.crudas else None
    motivo = ventana_no_citable(contexto, "v9", viejo.t0_ms, viejo.t1_ms, segs)
    print(f"control: el item viejo (supersedido) incumple la condicion: {motivo is not None}")


if __name__ == "__main__":
    main()
