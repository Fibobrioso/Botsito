"""El control de la fase 5 (decisiones del consultor del 2026-10-05, puntos 4 y 5), SIN abrir
ninguna filtrada:

- los bloques `[CUARENTENA]` de la filtrada B de v9 y de v10 salen de la salida YA COMMITEADA de
  `FILTRADAS-ESCENARIO-B/tramos_registrados-SALIDA.txt` (con su fin un segundo despues de la marca;
  el de v9 de 34:44, con su fin real 2.096.900): cada uno tiene que caber entero en un tramo
  registrado HOY;
- ningun item ev-* ACTIVO de v7-v10 se solapa mas de 0 ms con un tramo de su video;
- se dice cuantos supersedidos de v7-v10 deja fuera y cuales.

Uso: uv run python docs/validation/anexos/VENTANA-EV-V9/control_activos.py
"""

from __future__ import annotations

import re
from pathlib import Path

from botsito.corpus.cuarentena import cargar_tramos_no_citables
from botsito.evidence.modelo import cargar_evidencia

RAIZ = Path(__file__).resolve().parents[4]
BLOQUES = RAIZ / "docs/validation/anexos/FILTRADAS-ESCENARIO-B/tramos_registrados-SALIDA.txt"
_VIDEO = re.compile(r"^== (v\d+):")
_BLOQUE = re.compile(r"^\s+(\d+)-(\d+):")
SESIONES = {"v7", "v8", "v9", "v10"}


def main() -> None:
    tramos = cargar_tramos_no_citables(RAIZ)
    bloques: list[tuple[str, int, int]] = []
    video = None
    for linea in BLOQUES.read_text(encoding="utf-8").splitlines():
        if m := _VIDEO.match(linea):
            video = m.group(1)
        elif (m := _BLOQUE.match(linea)) and video:
            bloques.append((video, int(m.group(1)), int(m.group(2))))
    caben = 0
    for v, a, b in bloques:
        cabe = any(x <= a and b <= y for x, y, _ in tramos.get(v, ()))
        caben += cabe
        print(f"{v} {a}-{b}: {'cabe' if cabe else 'NO CABE'}")
    print(f"bloques de B que caben enteros en un tramo: {caben} de {len(bloques)}")
    items = cargar_evidencia(RAIZ / "knowledge" / "evidence")
    supersedidos = {it.supersede for it in items if it.supersede}
    fuera = sorted(i for i in supersedidos if any(i.startswith(f"ev-{v}-") for v in SESIONES))
    pisan = sorted(
        it.id
        for it in items
        if it.video_id in SESIONES and it.id not in supersedidos
        for x, y, _ in tramos.get(it.video_id, ())
        if it.t0_ms < y and x < it.t1_ms
    )
    print(f"items ACTIVOS de v7-v10 que solapan un tramo mas de 0 ms: {len(pisan)} {pisan}")
    print(f"supersedidos de v7-v10 que se dejan fuera: {len(fuera)} {fuera}")


if __name__ == "__main__":
    main()
