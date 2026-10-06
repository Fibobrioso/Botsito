"""Fase 0 b(1) de `trabajo/activacion-a42`: las filtradas de v7-v10, rehechas en su sitio con el
guion de `main` (`--solo-filtrar --video`), frente a B y a A (`FILTRADAS-ESCENARIO-B.md`) y a los
tramos no citables. SIN TEXTO: de cada filtrada solo se leen las marcas `[CUARENTENA mm:ss-mm:ss]`
y `[NO CITABLE mm:ss-mm:ss]` y la marca `[mm:ss]` del principio de cada linea visible; de cada
registro, sus lineas de recuento. Imprime recuentos, marcas, ms y sha256.

Lo que tiene que cumplirse (FILTRADAS-CON-TRAMOS.md §5), y si algo no cuadra sale DIFERENCIA:

  D1  nada visible en la NUEVA que B tapara (NUEVA - B, como multiconjunto de marcas, vacio);
  D2  lo que la NUEVA tapa y B no (B - NUEVA) es EXACTAMENTE lo que tapan los tramos: las lineas
      de B cuya marca cae dentro de un tramo, mas los segmentos que asoman por el INICIO de un
      tramo (empiezan antes y lo pisan mas de 0 ms), que salen con su t0 en ms de la medida de
      VENTANA-EV-V9.md §5 (`medir_recortados-SALIDA.txt`, filas «inicio»);
  D3  el recuento del registro cuadra: «solo por meses» 0, meses = los de B, y «solo por tramos»
      = |B - NUEVA|;
  D4  nada se destapa frente a A dentro de un tramo (NUEVA - A sin ninguna marca en un tramo, ni
      en el segundo anterior);
  D5  ninguna linea visible de la NUEVA tiene la marca dentro de un tramo: los 12 casos del
      segundo de margen (FILTRADAS-ESCENARIO-B.md §5.2) quedan tapados.

Las tres filtradas de cada video salen de la MISMA cruda, asi que se comparan como multiconjuntos
de marcas (leccion de medir_fase1.py: comparar con rangos de bloques da falsos en los bordes).

Uso: uv run python docs/validation/anexos/ACTIVACION-A42/medir_filtradas.py
"""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path

from botsito.corpus.cuarentena import cargar_tramos_no_citables

RAIZ = Path(__file__).resolve().parents[4]
E = Path(r"C:\Users\USER\Desktop")
SESIONES = {
    "v7": (E / "sesion-02-v7-audio", "sesion-02-v7"),
    "v8": (E / "sesion-02-v8-audio", "sesion-02-v8"),
    "v9": (E / "sesion-03-audio", "sesion-03"),
    "v10": (E / "sesion-04-audio", "sesion-04"),
}
RECORTADOS = RAIZ / "docs/validation/anexos/VENTANA-EV-V9/medir_recortados-SALIDA.txt"
# Los 12 tramos con una linea visible en su segundo de margen (FILTRADAS-ESCENARIO-B.md §5.2 y
# `hueco-SALIDA.txt`, «ultimo s»), por su intervalo en h:mm:ss. En v9 hay dos tramos que empiezan
# en el mismo segundo (el original y el que lo completa con el margen): cuenta el del margen.
DOCE = {
    "v10": (
        "0:45:05-0:46:41", "1:03:24-1:03:39", "1:26:34-1:26:41", "1:26:44-1:26:51",
        "1:39:08-1:39:42", "1:55:27-1:55:34", "1:55:58-1:56:03", "1:56:04-1:56:08",
        "2:06:42-2:07:03", "2:07:04-2:07:12",
    ),
    "v9": ("1:13:25-1:13:40", "1:13:55-1:14:05"),
}  # fmt: skip

_MARCA = re.compile(r"^\[(\d+):(\d\d)\] ")
_BLOQUE = re.compile(r"^\[(CUARENTENA|NO CITABLE) (\d+):(\d\d)–(\d+):(\d\d)\]$")
_MESES = re.compile(r"^segmentos en cuarentena: (\d+) en (\d+) bloques$")
_TAPADOS = re.compile(
    r"^segmentos tapados: solo por meses (\d+), solo por tramos (\d+), por ambos (\d+)$"
)
_FILA = re.compile(r"^\| (v\d+) \| (\d+) \| (\d+)-(\d+) \| (inicio|fin) \|")


def lineas(ruta: Path) -> list[str]:
    return ruta.read_text(encoding="utf-8").splitlines()


def visibles(ruta: Path) -> Counter[int]:
    """Las marcas (en ms, truncadas al segundo) de las lineas visibles. El texto no se guarda."""
    salida: Counter[int] = Counter()
    for linea in lineas(ruta):
        if m := _MARCA.match(linea):
            salida[(int(m.group(1)) * 60 + int(m.group(2))) * 1000] += 1
    return salida


def bloques(ruta: Path) -> Counter[str]:
    return Counter(m.group(1) for linea in lineas(ruta) if (m := _BLOQUE.match(linea)))


def recuento(ruta: Path) -> tuple[int | None, tuple[int, int, int] | None]:
    meses, tapados = None, None
    for linea in lineas(ruta):
        if m := _MESES.match(linea):
            meses = int(m.group(1))
        if m := _TAPADOS.match(linea):
            tapados = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return meses, tapados


def asoman_por_el_inicio() -> dict[str, list[tuple[int, int, int]]]:
    """video -> (segmento, t0_ms, t1_ms) de las filas «inicio» de la medida de VENTANA-EV-V9."""
    salida: dict[str, list[tuple[int, int, int]]] = {}
    for linea in lineas(RECORTADOS):
        if (m := _FILA.match(linea)) and m.group(5) == "inicio":
            salida.setdefault(m.group(1), []).append(
                (int(m.group(2)), int(m.group(3)), int(m.group(4)))
            )
    return salida


def hms(ms: int) -> str:
    s = ms // 1000
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"


def lista(marcas: Counter[int]) -> str:
    xs = sorted(marcas.elements())
    return f"{len(xs)}" + (f" ({', '.join(hms(t) for t in xs)})" if xs else "")


def sha(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def main() -> int:
    tramos = cargar_tramos_no_citables(RAIZ)
    inicio = asoman_por_el_inicio()
    diferencias: list[str] = []
    print("sha256 y recuentos de los registros (NUEVA = la rehecha hoy, instalada):")
    datos = {}
    for v, (carpeta, base) in SESIONES.items():
        nueva = carpeta / f"{base}.filtrada.md"
        f_a = carpeta / f"{base}.filtrada-A-condicion.md"
        f_b = carpeta / f"{base}.filtrada-B-condicion.md"
        meses, tapados = recuento(carpeta / f"{base}.registro.txt")
        meses_b, _ = recuento(carpeta / f"{base}.registro-B-condicion.txt")
        datos[v] = (visibles(nueva), visibles(f_a), visibles(f_b), meses, tapados, meses_b)
        print(f"  {v} NUEVA {sha(nueva)}  bloques {dict(sorted(bloques(nueva).items()))}")
        print(f"  {v} A     {sha(f_a)}")
        print(f"  {v} B     {sha(f_b)}")
        print(
            f"  {v} registro NUEVA: en cuarentena {meses}; solo meses / solo tramos / ambos "
            f"{tapados}; registro B: en cuarentena {meses_b}; tramos del video: "
            f"{len(tramos.get(v, ()))}"
        )
    print()
    print(
        "| video | D1: visibles en NUEVA que B tapaba | B - NUEVA (lo que tapan de mas los "
        "tramos) | de ellas, con la marca dentro de un tramo | asoman por el inicio | D2: sin "
        "explicar / esperadas que faltan | D3: registro | D4: NUEVA - A en un tramo | D5: "
        "visibles de NUEVA dentro de un tramo |"
    )
    print("|---|---|---|---|---|---|---|---|---|")
    for v in SESIONES:
        nueva, en_a, en_b, meses, tapados, meses_b = datos[v]
        de_tramos = [(a, b) for a, b, _ in tramos.get(v, ())]

        def dentro(t: int, tr: list[tuple[int, int]] = de_tramos) -> bool:
            return any(x <= t < y for x, y in tr)

        d1 = nueva - en_b
        de_mas = en_b - nueva
        con_marca = Counter({t: n for t, n in de_mas.items() if dentro(t)})
        # Lo esperado: toda linea visible de B con la marca dentro de un tramo, mas los segmentos
        # que asoman por el inicio de un tramo y no empiezan dentro de otro.
        esperado = Counter({t: n for t, n in en_b.items() if dentro(t)})
        asoman: Counter[int] = Counter()
        for _n, t0, _t1 in inicio.get(v, ()):
            marca = t0 // 1000 * 1000
            if not dentro(marca):
                asoman[marca] += 1
        # Un segmento que asoma solo cuenta si en B era visible (si no, ya lo tapaban los meses).
        asoman_visibles = Counter({t: min(n, en_b[t]) for t, n in asoman.items() if en_b[t]})
        esperado += asoman_visibles
        sin_explicar, faltan = de_mas - esperado, esperado - de_mas
        d3 = (
            tapados is not None
            and tapados[0] == 0
            and meses == meses_b
            and tapados[1] == sum(de_mas.values())
        )
        d4 = Counter(
            {
                t: n
                for t, n in (nueva - en_a).items()
                if any(x - 1000 <= t < y for x, y in de_tramos)
            }
        )
        d5 = Counter({t: n for t, n in nueva.items() if dentro(t)})
        for nombre, mal in (
            ("D1", bool(d1)),
            ("D2", bool(sin_explicar) or bool(faltan)),
            ("D3", not d3),
            ("D4", bool(d4)),
            ("D5", bool(d5)),
        ):
            if mal:
                diferencias.append(f"{nombre} {v}")
        print(
            f"| {v} | {lista(d1)} | {sum(de_mas.values())} | {sum(con_marca.values())} | "
            f"{lista(asoman_visibles)} | {lista(sin_explicar)} / {lista(faltan)} | "
            f"{'cuadra' if d3 else 'NO CUADRA'} | {lista(d4)} | {lista(d5)} |"
        )
    print()
    print("los 12 tramos del segundo de margen: lineas visibles con la marca dentro (A, B, NUEVA)")
    print("| video | tramo | A | B | NUEVA |")
    print("|---|---|---|---|---|")
    vistos = 0
    for v, inicios in DOCE.items():
        nueva, en_a, en_b, *_ = datos[v]
        for x, y, _ in tramos.get(v, ()):
            if f"{hms(x)}-{hms(y)}" not in inicios:
                continue
            vistos += 1
            na, nb, nn = (sum(n for t, n in c.items() if x <= t < y) for c in (en_a, en_b, nueva))
            # la linea del segundo de margen: la que empieza en el ultimo segundo del tramo
            ua, ub, un = (c[y - 1000] for c in (en_a, en_b, nueva))
            print(
                f"| {v} | {hms(x)}-{hms(y)} | {na} (ultimo s: {ua}) | {nb} (ultimo s: {ub}) "
                f"| {nn} (ultimo s: {un}) |"
            )
            if nn:
                diferencias.append(f"margen {v} {hms(x)}")
    if vistos != 12:
        diferencias.append(f"se esperaban 12 tramos de margen y hay {vistos}")
    print()
    print("DIFERENCIAS: " + ("; ".join(diferencias) if diferencias else "ninguna"))
    return 1 if diferencias else 0


if __name__ == "__main__":
    raise SystemExit(main())
