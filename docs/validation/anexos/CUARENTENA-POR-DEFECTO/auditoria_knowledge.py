"""¿Alguna evidencia o regla aceptada de knowledge/ cita un segmento que hoy cae en (b) o (c)?

Orden del consultor del 2026-10-01 (`trabajo/cuarentena-por-defecto`): «solo con cuentas e ids, sin
contenido [...] Para cada caso, da el id de la evidencia o regla, el video y el motivo, (b) o (c).
No toques nada de knowledge/». No escribe nada.

Un item de evidencia CITA los segmentos de su transcripcion (`transcripcion`) que pisan su
intervalo [t0, t1]; si alguno de esos segmentos lo oculta hoy el filtro por (b) o (c), el item sale.
Una regla de la spec o un termino del glosario salen si su `cita` es uno de esos items. La (a) -las
sesiones en cuarentena- no se pregunta: sus items se citaron de la version filtrada.

Uso: uv run python docs/validation/anexos/CUARENTENA-POR-DEFECTO/auditoria_knowledge.py
"""

from __future__ import annotations

import sys
from pathlib import Path

from botsito.cli import _carpeta_datos
from botsito.comun.documentos import activos
from botsito.corpus.cuarentena import MOTIVO_SESION, Filtro, cargar_tramos_no_citables
from botsito.corpus.manifiestos_transcripcion import cargar_todos, carpeta_de
from botsito.corpus.pipeline_transcripcion import FICHERO_CRUDA, cargar_cruda
from botsito.evidence.modelo import cargar_evidencia
from botsito.spec.modelo import cargar_glosario, cargar_reglas

RAIZ = Path(__file__).resolve().parents[4]


def main() -> int:
    tramos = cargar_tramos_no_citables(RAIZ)
    datos = _carpeta_datos(RAIZ)
    filtros: dict[str, Filtro] = {}
    sin_datos: set[str] = set()
    for t in cargar_todos(RAIZ):
        carpeta = carpeta_de(datos, t)
        if not (carpeta / FICHERO_CRUDA).is_file():
            sin_datos.add(t.id)
            continue
        filtro = Filtro(t.video_id, tramos.get(t.video_id, ()))
        cargar_cruda(carpeta, filtro)  # solo para que el filtro anote lo que oculta
        filtros[t.id] = filtro

    items = cargar_evidencia(RAIZ / "knowledge" / "evidence")
    vivos = {i.id for i in activos(items)}
    afectados: dict[str, tuple[str, str]] = {}
    sin_comprobar = 0
    for it in items:
        if it.transcripcion is None:
            continue
        filtro = filtros.get(it.transcripcion)
        if filtro is None:
            sin_comprobar += 1
            continue
        motivos = sorted(
            {
                o.motivo
                for o in filtro.ocultos_entre(it.t0_ms, it.t1_ms)
                if o.motivo != MOTIVO_SESION
            }
        )
        if motivos:
            afectados[it.id] = (it.video_id, ", ".join(f"({m})" for m in motivos))

    print("Evidencia que cita un segmento oculto hoy por (b) o (c):")
    print("| Item | Video | Motivo | Vivo |")
    print("|---|---|---|---|")
    for iid, (video, motivo) in sorted(afectados.items()):
        print(f"| {iid} | {video} | {motivo} | {'si' if iid in vivos else 'supersedido'} |")
    print(f"Total: {len(afectados)} de {len(items)} items")
    if sin_comprobar:
        print(f"Sin comprobar ({sin_comprobar} items): su transcripcion no esta en esta maquina")

    spec = RAIZ / "knowledge" / "spec"
    citas = [(r.id, r.cita) for r in cargar_reglas(spec / "strategy_spec.yaml")]
    citas += [(f"termino {t.termino}", t.cita) for t in cargar_glosario(spec / "glossary.yaml")]
    print()
    print("Reglas y terminos del glosario que citan uno de esos items:")
    print("| Regla o termino | Cita | Video | Motivo |")
    print("|---|---|---|---|")
    n = 0
    for quien, cita in citas:
        if cita in afectados:
            n += 1
            video, motivo = afectados[cita]
            print(f"| {quien} | {cita} | {video} | {motivo} |")
    print(f"Total: {n} de {len(citas)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
