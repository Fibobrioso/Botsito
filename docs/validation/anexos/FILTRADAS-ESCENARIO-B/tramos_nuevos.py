"""Los tramos nuevos de la segunda respuesta del consultor (punto 2), calculados SIN TEXTO: solo las
marcas `[CUARENTENA mm:ss-mm:ss]` de las filtradas y los tiempos de los tramos y de los items.

- v9: un tramo nuevo por cada uno de los 8 bloques de su cuarentena mecanica (los de su filtrada
  ANTES, que es tambien su B), del inicio al segundo al final MAS UN SEGUNDO; completa el tramo
  original, registrado sin ese margen.
- v10: el bloque de B que empieza en 1:55:27, del inicio al segundo al final mas un segundo.

Para cada uno: el control positivo (el bloque de B cabe entero en el tramo nuevo) y la parada (algun
item ev-* pisa los segundos que el tramo nuevo cubre y que no cubria ningun tramo de antes).

Uso: uv run python docs/validation/anexos/FILTRADAS-ESCENARIO-B/tramos_nuevos.py
"""

from __future__ import annotations

import re
from pathlib import Path

from botsito.corpus.cuarentena import cargar_tramos_no_citables
from botsito.evidence.modelo import cargar_evidencia

RAIZ = Path(__file__).resolve().parents[4]
E = Path(r"C:\Users\USER\Desktop")
B_V9 = E / "sesion-03-audio" / "sesion-03.filtrada-B-condicion.md"
B_V10 = E / "sesion-04-audio" / "sesion-04.filtrada-B-condicion.md"
_BLOQUE = re.compile(r"^\[CUARENTENA (\d+):(\d\d)–(\d+):(\d\d)\]$")
INICIO_V10 = (1 * 3600 + 55 * 60 + 27) * 1000


def marcas(ruta: Path) -> list[tuple[int, int]]:
    """(inicio, final) en ms de cada marca, SIN margen: el final es el segundo truncado."""
    salida = []
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        if m := _BLOQUE.match(linea):
            a = (int(m.group(1)) * 60 + int(m.group(2))) * 1000
            b = (int(m.group(3)) * 60 + int(m.group(4))) * 1000
            salida.append((a, b))
    return sorted(salida)


def hms(ms: int) -> str:
    s = ms // 1000
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"


def descubierto(a: int, b: int, previos: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Las partes de [a, b) que no cubre ningun tramo de `previos`."""
    trozos = [(a, b)]
    for x, y in previos:
        nuevos = []
        for p, q in trozos:
            if q <= x or p >= y:
                nuevos.append((p, q))
                continue
            if p < x:
                nuevos.append((p, x))
            if q > y:
                nuevos.append((y, q))
        trozos = nuevos
    return trozos


def main() -> None:
    tramos = cargar_tramos_no_citables(RAIZ)
    items = list(cargar_evidencia(RAIZ / "knowledge" / "evidence"))
    propuestos: list[tuple[str, int, int, str]] = []
    for a, b in marcas(B_V9):
        original = next(
            ((x, y) for x, y, _ in tramos["v9"] if x == a and y == b), None
        )  # el tramo de la sesion 3, sin margen
        propuestos.append(("v9", a, b + 1000, f"{hms(a)}-{hms(original[1])}" if original else "?"))
    bloque_v10 = next((a, b) for a, b in marcas(B_V10) if a == INICIO_V10)
    propuestos.append(("v10", bloque_v10[0], bloque_v10[1] + 1000, ""))
    print(
        "| video | tramo nuevo (ms) | h:mm:ss | completa a | control positivo | items en lo nuevo |"
    )
    print("|---|---|---|---|---|---|")
    paradas = 0
    for v, t0, t1, original in propuestos:
        bloques_b = marcas(B_V9 if v == "v9" else B_V10)
        cabe = any(t0 <= a and b + 1000 <= t1 for a, b in bloques_b if a == t0)
        previos = [(x, y) for x, y, _ in tramos[v]]
        nuevo = descubierto(t0, t1, previos)
        caen = sorted(
            it.id
            for it in items
            if it.video_id == v and any(it.t1_ms > p and it.t0_ms < q for p, q in nuevo)
        )
        paradas += len(caen)
        print(
            f"| {v} | {t0}-{t1} | {hms(t0)}-{hms(t1)} | {original or '-'} | "
            f"{'cabe' if cabe else 'NO CABE'} | {len(caen)}" + (f" {caen}" if caen else "") + " |"
        )
    print()
    print(f"PARADA (items en los segundos nuevos): {paradas}")


if __name__ == "__main__":
    main()
