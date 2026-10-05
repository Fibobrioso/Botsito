"""Fase 0 de `trabajo/ventana-ev-v9-003456`, punto b) y c), SIN TEXTO: la ventana declarada nueva de
ev-v9-003456-9ef48fb5, medida por la misma via que `FILTRADAS-ESCENARIO-B/ancla_v9.py`: el contexto
de `knowledge validate` (`construir_contexto`), sus segmentos por `contexto.crudas` (solo `n`,
`t0_ms` y `t1_ms`) y `verificar_citas`, el llamador autorizado. No imprime texto, palabras ni
longitudes de cita; de los problemas de cita, solo cuantos hay.

- «Segmento en cuarentena»: todo segmento de la cruda de v9 que se solapa mas de 0 ms con algun
  tramo no citable de v9, contando el tramo de margen 0:34:44-0:34:57 que entra en esta rama
  (punto c), anadido aqui EN MEMORIA.
- Cada ventana candidata empieza en un segundo entero y termina en el t1 actual (2.100.000); se
  prueba con el mismo item, cambiando solo su `t0` en memoria (`dataclasses.replace`).

Uso: uv run python docs/validation/anexos/VENTANA-EV-V9/medir_ventana.py
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from botsito.corpus.inventario import cargar_manifiesto
from botsito.evidence.modelo import cargar_evidencia, verificar_citas
from botsito.validation.contexto_evidencia import construir_contexto
from botsito.validation.knowledge import _carpeta_datos

RAIZ = Path(__file__).resolve().parents[4]
ITEM = "ev-v9-003456-9ef48fb5"
MARGEN = (2_084_000, 2_097_000, "margen 0:34:44-0:34:57 (punto c, en memoria)")
T1 = 2_100_000


def hms(ms: int) -> str:
    s = ms // 1000
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"


def main() -> None:
    items = cargar_evidencia(RAIZ / "knowledge" / "evidence")
    ruta_manifiesto = RAIZ / "knowledge" / "corpus" / "manifest.yaml"
    manifiesto = cargar_manifiesto(ruta_manifiesto) if ruta_manifiesto.exists() else None
    contexto, _temas = construir_contexto(RAIZ, _carpeta_datos(RAIZ), manifiesto)
    item = next(i for i in items if i.id == ITEM)
    assert item.transcripcion is not None and contexto.crudas is not None
    segmentos = list(contexto.crudas(item.transcripcion) or [])
    por_n = {s.n: s for s in segmentos}
    tramos = [*contexto.tramos_no_citables.get("v9", ()), MARGEN]
    cuarentena = [s for s in segmentos if any(s.t1_ms > a and s.t0_ms < b for a, b, _ in tramos)]
    en_cuarentena = {s.n for s in cuarentena}

    print(f"== {ITEM}: ventana declarada hoy {item.t0_ms}-{item.t1_ms} ms")
    for n in (611, 612, 613, 614):
        s = por_n[n]
        print(f"segmento {n}: {s.t0_ms}-{s.t1_ms} ms; en cuarentena: {n in en_cuarentena}")
    print(f"tramo de margen (punto c): {MARGEN[0]}-{MARGEN[1]} ms")

    p, _avisos, loc = verificar_citas([item], contexto)
    hoy = loc.get(item.id)
    print(
        f"hoy: problemas {len(p)}; apariciones {hoy.coincidencias if hoy else '-'}; segmentos de "
        f"la cita {list(hoy.segmentos) if hoy else '-'}; palabras {hoy.t0_ms if hoy else '-'}-"
        f"{hoy.t1_ms if hoy else '-'} ms"
    )
    print()
    print(
        "| t0 candidato | solapa segmentos en cuarentena | solapa un tramo | problemas | "
        "apariciones | cumple |"
    )
    print("|---|---|---|---|---|---|")
    primero = None
    for segundo in range(2094, 2099):
        t0 = segundo * 1000
        candidato = replace(item, t0=hms(t0))
        segs = [s.n for s in cuarentena if s.t1_ms > t0 and s.t0_ms < T1]
        tramo = any(a < T1 and t0 < b for a, b, _ in tramos)
        p, _avisos, loc = verificar_citas([candidato], contexto)
        c = loc.get(candidato.id)
        apariciones = c.coincidencias if c else 0
        cumple = not segs and not tramo and not p and apariciones == 1
        if cumple and primero is None:
            primero = t0
        print(
            f"| {t0} ({hms(t0)}) | {segs or 'ninguno'} | {tramo} | {len(p)} | {apariciones} | "
            f"{'SI' if cumple else 'no'} |"
        )
    print()
    print(f"VENTANA NUEVA: {primero}-{T1} ms ({hms(primero) if primero else '-'}-{hms(T1)})")
    if primero is not None:
        a, b = MARGEN[0], MARGEN[1]
        print(f"solape con el tramo de margen: {max(0, min(b, T1) - max(a, primero))} ms")


if __name__ == "__main__":
    main()
