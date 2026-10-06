"""M3c de RELOJ-INVIERNO.md: el eje de horas de un fotograma de ENERO de v4, contra Dukascopy, con
eje UTC+1 y con eje UTC+2.

No hay leyenda O/H/L/C legible en los fotogramas de M3 (la tapa la barra del replay), asi que se
leen las VELAS mismas: por cada columna de pixeles del area de precio, el pixel mas alto y el mas
bajo de color de vela (rojo o verde vivos), agrupados por minuto con la rejilla del propio
grafico. La rejilla da la calibracion: sus lineas verticales estan en las etiquetas de hora del
eje y las horizontales en las de precio (medidas en una zona vacia del fotograma y leidas en sus
etiquetas). Cada minuto da un maximo y un minimo del grafico, que se comparan con la vela M1 de
Dukascopy (BID) del minuto UTC = hora del eje - desfase, para desfase 1 h y 2 h.

Un maximo se descarta si su pixel toca una zona tapada (la barra del replay, la de dibujo, el
borde superior): ahi la vela sigue por debajo de lo que tapa y el maximo leido no es el suyo.

Lo que se imprime: por desfase, cuantos minutos se comparan, y la mediana y el maximo de la
diferencia absoluta en puntos (1e-5), de maximos y de minimos.

    python docs/validation/anexos/RELOJ-INVIERNO/eje_contra_dukascopy.py
    (un Python con Pillow, que no es dependencia del proyecto; las velas las lee `uv run`)
"""

from __future__ import annotations

import json
import os
import statistics
import subprocess
import sys
from pathlib import Path

from PIL import Image

RAIZ = Path(os.environ.get("BOTSITO_RAIZ") or Path(__file__).resolve().parents[4])

# Calibracion de cada fotograma: la medida de la rejilla y la lectura de sus etiquetas.
#   x0: columna de la linea vertical de la etiqueta `h0` del eje; pxmin: pixeles por minuto.
#   y0: fila de la linea horizontal de la etiqueta `p0` (puntos de 1e-5); pxpt: pixeles por punto.
#   tapado: rectangulos (x1, y1, x2, y2) donde una vela puede quedar oculta.
FOTOGRAMAS = {
    "001200000": {
        "dia": "2026-01-29",
        "h0": "08:00",
        "x0": 681.5,
        "pxmin": 94.9 / 15,
        "p0": 119800,
        "y0": 247.0,
        "pxpt": 42.05 / 20,
        "area": (0, 158, 1658, 675),
        # La interfaz: la barra del replay con su interruptor y el texto de variacion (arriba a la
        # izquierda), las dos barras de dibujo y el borde superior. Sus pixeles NO se leen, y un
        # maximo que toca una de ellas se descarta.
        "tapado": [(0, 150, 760, 214), (845, 168, 920, 212), (845, 226, 1395, 274), (0, 150, 1660, 160)],
        # La caja de la posicion (entrada, stop y objetivo) tine las mechas que caen dentro: sus
        # minutos se cuentan aparte.
        "caja": (938, 1360),
    },
    "001248000": {
        "dia": "2026-01-27",
        "h0": "07:05",
        "x0": 265.5,
        "pxmin": (1510.5 - 265.5) / 65,
        "p0": 118745,
        "y0": 513.5,
        "pxpt": (763.5 - 429.5) / 40,
        # por debajo empieza el volumen: un minimo que toca el borde inferior se descarta
        "area": (0, 158, 1658, 745),
        "tapado": [(0, 150, 760, 214), (845, 168, 920, 212), (845, 226, 1395, 274), (0, 150, 1660, 160)],
        "caja": (743, 1380),
    },
    "001149000": {
        "dia": "2026-01-30",
        "h0": "11:20",
        "x0": 195.5,
        "pxmin": (1650.5 - 195.5) / 110,
        "p0": 119360,
        "y0": 299.5,
        "pxpt": (814.5 - 299.5) / 220,
        "area": (0, 158, 1658, 750),
        "tapado": [(0, 150, 760, 214), (845, 168, 920, 212), (845, 226, 1395, 274), (0, 150, 1660, 160)],
        "caja": (1263, 1415),
    },
}


def es_vela(rgb: tuple[int, int, int]) -> bool:
    r, g, b = rgb
    rojo = r > 170 and g < 110 and b < 120
    verde = g > 120 and r < 90 and b > 90
    return rojo or verde


def tapado(x: int, y: int, zonas) -> bool:
    return any(x1 <= x <= x2 and y1 <= y <= y2 + 1 for x1, y1, x2, y2 in zonas)


def velas_del_grafico(nombre: str, c: dict) -> dict[int, tuple[float | None, float]]:
    """minuto del eje (desde 00:00) -> (maximo o None si tapado, minimo), en puntos."""
    im = Image.open(RAIZ / "data/fotogramas/v4/png-1fps" / f"{nombre}.png").convert("RGB")
    px = im.load()
    x1, y1, x2, y2 = c["area"]
    h, m = (int(v) for v in c["h0"].split(":"))
    m0 = h * 60 + m
    por_min: dict[int, list[tuple[int, int]]] = {}
    for x in range(x1, x2):
        ys = [y for y in range(y1, y2) if es_vela(px[x, y]) and not tapado(x, y, c["tapado"])]
        if not ys:
            continue
        minuto = m0 + round((x - c["x0"]) / c["pxmin"])
        por_min.setdefault(minuto, []).append((min(ys), max(ys)))
        por_min[minuto] = por_min[minuto]
    salida = {}
    for minuto, col in por_min.items():
        if len(col) < 2:
            continue  # una sola columna: borde de otra vela, no se usa
        arriba = min(a for a, _ in col)
        abajo = max(b for _, b in col)
        xs_arriba = [x for x in range(x1, x2) if m0 + round((x - c["x0"]) / c["pxmin"]) == minuto]
        censurado = any(tapado(x, arriba, c["tapado"]) for x in xs_arriba)
        precio = lambda y: c["p0"] + (c["y0"] - y) / c["pxpt"]  # noqa: E731
        suelo = abajo >= y2 - 1
        salida[minuto] = (None if censurado else precio(arriba), None if suelo else precio(abajo))
    return salida


def velas_dukascopy(dia: str) -> dict[int, tuple[int, int]]:
    codigo = (
        "import json,sys\n"
        "from datetime import UTC, datetime\n"
        "from pathlib import Path\n"
        f"sys.path.insert(0, {str(RAIZ / 'src')!r})\n"
        "from botsito.cases.fidelidad import cargar_config\n"
        "from botsito.config.ajustes import carpeta_datos\n"
        "from botsito.data.dataset import buscar_manifiesto, cargar_manifiesto, cargar_serie\n"
        f"R=Path({str(RAIZ)!r})\n"
        "ruta=buscar_manifiesto(R, cargar_config(R).dataset_prefijo + '2026-01')\n"
        "s=cargar_serie(cargar_manifiesto(ruta), carpeta_datos(R))\n"
        "out={}\n"
        "for v in s.velas:\n"
        "    t=datetime.fromtimestamp(int(v.inicio)*60, tz=UTC)\n"
        f"    if t.date().isoformat()=={dia!r}: out[t.hour*60+t.minute]=(int(v.maxima),int(v.minima))\n"
        "print(json.dumps(out))\n"
    )
    r = subprocess.run(["uv", "run", "python", "-c", codigo], cwd=RAIZ, capture_output=True,
                       text=True, check=True)
    return {int(k): tuple(v) for k, v in json.loads(r.stdout).items()}


def main() -> int:
    for nombre, c in FOTOGRAMAS.items():
        grafico = velas_del_grafico(nombre, c)
        duk = velas_dukascopy(c["dia"])
        ms = sorted(grafico)
        print(f"== fr-v4-9ad0ebb8/{int(nombre)} ({c['dia']}): {len(ms)} minutos con vela en el "
              f"grafico, de {ms[0] // 60:02d}:{ms[0] % 60:02d} a {ms[-1] // 60:02d}:{ms[-1] % 60:02d} "
              f"del eje; maximos tapados: {sum(1 for m in ms if grafico[m][0] is None)}; minimos "
              f"tapados: {sum(1 for m in ms if grafico[m][1] is None)}")
        x1c, x2c = c["caja"]
        h, mm = (int(v) for v in c["h0"].split(":"))
        def en_caja(m):
            x = c["x0"] + (m - (h * 60 + mm)) * c["pxmin"]
            return x1c <= x <= x2c
        for desfase in (60, 120):
          for titulo, sel in (("fuera de la caja", [m for m in ms if not en_caja(m)]),
                              ("dentro de la caja", [m for m in ms if en_caja(m)])):
            dmax, dmin = [], []
            for m in sel:
                d = duk.get(m - desfase)
                if d is None:
                    continue
                alto, bajo = grafico[m]
                if alto is not None:
                    dmax.append(abs(alto - d[0]))
                if bajo is not None:
                    dmin.append(abs(bajo - d[1]))
            todos = sorted(dmax + dmin)
            p90 = todos[int(0.9 * (len(todos) - 1))]
            print(f"  eje UTC+{desfase // 60}, {titulo}: {len(sel)} minutos; |dif| maximos "
                  f"mediana {statistics.median(dmax):.1f} max {max(dmax):.1f}; minimos mediana "
                  f"{statistics.median(dmin):.1f} max {max(dmin):.1f}; todos: mediana "
                  f"{statistics.median(todos):.1f}, p90 {p90:.1f}, max {todos[-1]:.1f} puntos")
        # Y todos los desfases de 0 a 180 minutos, maximos y minimos juntos y sin separar la
        # caja: si el eje no fuera una hora entera, el mejor no caeria en 60 ni en 120.
        barrido = []
        for desfase in range(0, 181):
            ds = []
            for m in ms:
                d = duk.get(m - desfase)
                if d is None:
                    continue
                alto, bajo = grafico[m]
                if alto is not None:
                    ds.append(abs(alto - d[0]))
                if bajo is not None:
                    ds.append(abs(bajo - d[1]))
            barrido.append((statistics.median(ds), desfase, len(ds)))
        mejores = sorted(barrido)[:4]
        print("  barrido 0-180 min, los cuatro mejores (mediana |dif|, desfase, n): "
              + "; ".join(f"{a:.1f}, {o} min, {k}" for a, o, k in mejores))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
