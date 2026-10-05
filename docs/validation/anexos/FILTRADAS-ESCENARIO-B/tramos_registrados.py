"""Tras registrar los tramos nuevos (segunda respuesta, punto 2; cuarta, punto 2a), SIN TEXTO:

- control positivo: cada bloque `[CUARENTENA …]` de la filtrada B de v9 y de v10, con su final un
  segundo despues de la marca (la cola de su ultimo segmento), cabe ENTERO en un tramo registrado;
  el bloque de v9 de 34:44, que termina en 2.096.900 ms (`ancla_v9.py`), se mide aparte: el tramo
  que lo cubre llega a 2.096.000 y la cola 2.096.000-2.096.900 queda fuera (cuarta respuesta, 2a);
- ningun item ev-* de v7-v10 solapa un tramo registrado de su video mas de 0 ms (la regla de
  `tramo_no_citable`, verificacion.py, que aplica knowledge validate).

Uso: uv run python docs/validation/anexos/FILTRADAS-ESCENARIO-B/tramos_registrados.py
"""

from __future__ import annotations

import re
from pathlib import Path

from botsito.corpus.cuarentena import cargar_tramos_no_citables
from botsito.evidence.modelo import cargar_evidencia

RAIZ = Path(__file__).resolve().parents[4]
E = Path(r"C:\Users\USER\Desktop")
B = {
    "v9": E / "sesion-03-audio" / "sesion-03.filtrada-B-condicion.md",
    "v10": E / "sesion-04-audio" / "sesion-04.filtrada-B-condicion.md",
}
_BLOQUE = re.compile(r"^\[CUARENTENA (\d+):(\d\d)–(\d+):(\d\d)\]$")
FIN_REAL_34_44 = 2_096_900  # ultimo segmento del bloque de v9 de 34:44 (ancla_v9-SALIDA.txt)


def marcas(ruta: Path) -> list[tuple[int, int]]:
    salida = []
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        if m := _BLOQUE.match(linea):
            a = (int(m.group(1)) * 60 + int(m.group(2))) * 1000
            b = (int(m.group(3)) * 60 + int(m.group(4))) * 1000
            salida.append((a, b))
    return sorted(salida)


def main() -> None:
    tramos = cargar_tramos_no_citables(RAIZ)
    fuera = 0
    for v, ruta in B.items():
        print(f"== {v}: control positivo de los bloques de B")
        for a, b in marcas(ruta):
            fin = FIN_REAL_34_44 if (v, a) == ("v9", 2_084_000) else b + 1000
            cabe = any(x <= a and fin <= y for x, y, _ in tramos[v])
            hasta = max((y for x, y, _ in tramos[v] if x <= a < y), default=None)
            if not cabe:
                fuera += 1
            print(f"    {a}-{fin}: {'cabe' if cabe else f'NO CABE (cubierto hasta {hasta})'}")
    print(f"bloques que no caben enteros: {fuera}")
    items = list(cargar_evidencia(RAIZ / "knowledge" / "evidence"))
    pisan = sorted(
        it.id
        for it in items
        if it.video_id in {"v7", "v8", "v9", "v10"}
        for x, y, _ in tramos.get(it.video_id, ())
        if it.t0_ms < y and x < it.t1_ms
    )
    print(f"items de v7-v10 que solapan un tramo mas de 0 ms: {len(pisan)} {pisan}")


if __name__ == "__main__":
    main()
