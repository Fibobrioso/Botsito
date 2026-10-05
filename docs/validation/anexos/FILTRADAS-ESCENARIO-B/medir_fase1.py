"""Fase 1 de `trabajo/filtradas-escenario-b`: las filtradas B, rehechas en su sitio con el guion de
`main` (`--solo-filtrar`), frente a ANTES y a A. SIN TEXTO: de cada filtrada solo se leen las
marcas `[CUARENTENA mm:ss-mm:ss]` y la marca `[mm:ss]` del principio de cada linea visible; de cada
registro, su linea de recuento. Imprime recuentos, marcas, limites en ms, ids ev-* y sha256.

- ANTES: la filtrada de antes de la regla por condicion (v9, v10); para v7 y v8, sus tramos.
- A: la filtrada en el escenario A, apartada como `*.filtrada-A-condicion.md`.
- B: la filtrada rehecha en el escenario B, guardada como `*.filtrada-B-condicion.md` (tras la
  parada P2 se restauro A como filtrada oficial; respuesta del consultor, punto 1d).

Las tres paradas (respuesta del consultor a la fase 0, punto 3):
  P1: algun ev-* cae en un bloque de B que no estaba oculto en ANTES (o en sus tramos);
  P2: algun bloque de A que en B no esta tapado cae, aunque sea en parte, en un tramo no citable;
  P3: algun bloque de ANTES que en B no esta tapado.

Uso: uv run python docs/validation/anexos/FILTRADAS-ESCENARIO-B/medir_fase1.py
"""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path

from botsito.corpus.cuarentena import cargar_tramos_no_citables
from botsito.evidence.modelo import cargar_evidencia

RAIZ = Path(__file__).resolve().parents[4]
E = Path(r"C:\Users\USER\Desktop")
# video -> (carpeta, nombre base, tiene ANTES)
SESIONES = {
    "v7": (E / "sesion-02-v7-audio", "sesion-02-v7", False),
    "v8": (E / "sesion-02-v8-audio", "sesion-02-v8", False),
    "v9": (E / "sesion-03-audio", "sesion-03", True),
    "v10": (E / "sesion-04-audio", "sesion-04", True),
}
_BLOQUE = re.compile(r"^\[CUARENTENA (\d+):(\d\d)–(\d+):(\d\d)\]$")
_MARCA = re.compile(r"^\[(\d+):(\d\d)\] ")
_CUENTA = re.compile(r"^segmentos en cuarentena: (\d+) en (\d+) bloques$")


def bloques(ruta: Path) -> list[tuple[int, int]]:
    """(inicio al segundo, final + 1 s) en ms de cada marca de cuarentena."""
    salida = []
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        if m := _BLOQUE.match(linea):
            a = (int(m.group(1)) * 60 + int(m.group(2))) * 1000
            b = (int(m.group(3)) * 60 + int(m.group(4)) + 1) * 1000
            salida.append((a, b))
    return sorted(salida)


def marcas_visibles(ruta: Path) -> list[int]:
    salida = []
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        if m := _MARCA.match(linea):
            salida.append((int(m.group(1)) * 60 + int(m.group(2))) * 1000)
    return salida


def cuenta(ruta: Path) -> str:
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        if m := _CUENTA.match(linea):
            return f"{m.group(1)}/{m.group(2)}"
    return "?"


def cabe(a: int, b: int, x: int, y: int) -> bool:
    """[a, b) cabe en [x, y), con un segundo de tolerancia en el final (ver medir_fase0.py)."""
    return x <= a and b <= y + 1000


def pisa(a: int, b: int, x: int, y: int) -> bool:
    return a < y and b > x


def hms(ms: int) -> str:
    s = ms // 1000
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"


def sha(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def main() -> None:
    tramos = cargar_tramos_no_citables(RAIZ)
    items = list(cargar_evidencia(RAIZ / "knowledge" / "evidence"))
    paradas: list[str] = []
    print(
        "| video | antes | A | B | bloques nuevos de B | items ev-* en ellos | A destapado en B "
        "que pisa un tramo | ANTES destapado en B |"
    )
    print("|---|---|---|---|---|---|---|---|")
    for v, (carpeta, base, con_antes) in SESIONES.items():
        de_tramos = [(a, b) for a, b, _ in tramos.get(v, ())]
        f_b = carpeta / f"{base}.filtrada-B-condicion.md"
        f_a = carpeta / f"{base}.filtrada-A-condicion.md"
        f_antes = carpeta / f"{base}.filtrada-ANTES-condicion.md"
        en_b, en_a = bloques(f_b), bloques(f_a)
        antes = bloques(f_antes) if con_antes else de_tramos
        txt_antes = (
            cuenta(carpeta / f"{base}.registro-ANTES-condicion.txt")
            if con_antes
            else f"{len(de_tramos)} tramos"
        )
        # NUEVOS: bloques de B que no caben en ninguno de ANTES (o de sus tramos).
        nuevos = [(a, b) for a, b in en_b if not any(cabe(a, b, x, y) for x, y in antes)]
        caen = sorted(
            it.id
            for it in items
            if it.video_id == v and any(pisa(it.t0_ms, it.t1_ms, a, b) for a, b in nuevos)
        )
        # DESTAPADOS frente a A: bloques de A que ningun bloque de B cubre; los que pisan un tramo.
        a_destapados = [(a, b) for a, b in en_a if not any(cabe(a, b, x, y) for x, y in en_b)]
        a_en_tramo = [
            (a, b) for a, b in a_destapados if any(pisa(a, b, x, y) for x, y in de_tramos)
        ]
        # DESTAPADOS frente a ANTES: bloques de ANTES que ningun bloque de B cubre.
        antes_destapados = (
            [(a, b) for a, b in bloques(f_antes) if not any(cabe(a, b, x, y) for x, y in en_b)]
            if con_antes
            else []
        )
        if caen:
            paradas.append(f"P1 {v}: {len(caen)} items")
        if a_en_tramo:
            paradas.append(f"P2 {v}: {len(a_en_tramo)} bloques")
        if antes_destapados:
            paradas.append(f"P3 {v}: {len(antes_destapados)} bloques")

        def lista(xs: list[tuple[int, int]]) -> str:
            return f"{len(xs)}" + (f" ({', '.join(hms(a) for a, _ in xs)})" if xs else "")

        print(
            f"| {v} | {txt_antes} | {cuenta(carpeta / f'{base}.registro-A-condicion.txt')} "
            f"| {cuenta(carpeta / f'{base}.registro-B-condicion.txt')} | {lista(nuevos)} "
            f"| {len(caen)}"
            + (f" ({', '.join(caen)})" if caen else "")
            + f" | {lista(a_en_tramo)} "
            f"| {lista(antes_destapados)} |"
        )
    print()
    print("PARADAS por bloques (aproximadas): " + ("; ".join(paradas) if paradas else "ninguna"))
    # La misma comprobacion a nivel de SEGMENTO, que es como la define el consultor: una linea
    # VISIBLE en B cuya marca cae dentro de un bloque oculto de A (o de ANTES). Un bloque de A que
    # B parte en dos no cuenta asi como destapado entero.
    print()
    print(
        "a nivel de segmento, EXACTO: lineas visibles en B que no lo eran en A / en ANTES "
        "(multiconjunto)"
    )
    print(
        "| video | visibles en B que en A estaban ocultas | de ellas, en un tramo | visibles en B "
        "que en ANTES estaban ocultas |"
    )
    print("|---|---|---|---|")
    paradas_seg: list[str] = []
    for v, (carpeta, base, con_antes) in SESIONES.items():
        de_tramos = [(a, b) for a, b, _ in tramos.get(v, ())]
        # EXACTO, sin bordes: las tres filtradas salen de la MISMA cruda, asi que una linea
        # destapada en B es una marca que aparece mas veces entre las visibles de B que entre las
        # de A (multiconjunto). Medido el 2026-10-04: comparar marcas con rangos de bloques daba
        # falsos destapados en los bordes (la marca trunca al segundo), y lo delato v9, cuya B es
        # identica byte a byte a ANTES y aun asi salian 4.
        marcas_b = Counter(marcas_visibles(carpeta / f"{base}.filtrada-B-condicion.md"))
        marcas_a = Counter(marcas_visibles(carpeta / f"{base}.filtrada-A-condicion.md"))
        dest_a = sorted((marcas_b - marcas_a).elements())
        # «aunque sea en parte»: la linea empieza dentro del tramo, o en el segundo anterior.
        dest_a_tramo = [t for t in dest_a if any(x - 1000 <= t < y for x, y in de_tramos)]
        if con_antes:
            marcas_antes = Counter(marcas_visibles(carpeta / f"{base}.filtrada-ANTES-condicion.md"))
            dest_antes = sorted((marcas_b - marcas_antes).elements())
        else:
            dest_antes = []
        if dest_a_tramo:
            paradas_seg.append(f"P2 {v}: {len(dest_a_tramo)} segmentos")
        if dest_antes:
            paradas_seg.append(f"P3 {v}: {len(dest_antes)} segmentos")

        def ts(xs: list[int]) -> str:
            return f"{len(xs)}" + (f" ({', '.join(hms(t) for t in xs)})" if xs else "")

        print(f"| {v} | {ts(dest_a)} | {ts(dest_a_tramo)} | {ts(dest_antes)} |")
    print()
    print("PARADAS por segmento: " + ("; ".join(paradas_seg) if paradas_seg else "ninguna"))
    print()
    print("sha256 de las filtradas (A apartada, B nueva, ANTES):")
    for v, (carpeta, base, con_antes) in SESIONES.items():
        print(f"  {v} A    {sha(carpeta / f'{base}.filtrada-A-condicion.md')}")
        print(f"  {v} B    {sha(carpeta / f'{base}.filtrada-B-condicion.md')}")
        if con_antes:
            print(f"  {v} ANTES {sha(carpeta / f'{base}.filtrada-ANTES-condicion.md')}")
    print()
    print("por tramo no citable: lineas visibles cuya marca cae dentro, en A y en B (sin texto):")
    print("| video | tramo (ms) | lineas en A | lineas en B |")
    print("|---|---|---|---|")
    for v, (carpeta, base, _) in SESIONES.items():
        marcas_a = marcas_visibles(carpeta / f"{base}.filtrada-A-condicion.md")
        marcas_b = marcas_visibles(carpeta / f"{base}.filtrada-B-condicion.md")
        for x, y, _ in tramos.get(v, ()):
            na = sum(1 for t in marcas_a if x <= t < y)
            nb = sum(1 for t in marcas_b if x <= t < y)
            print(f"| {v} | {x}-{y} ({hms(x)}) | {na} | {nb} |")


if __name__ == "__main__":
    main()
