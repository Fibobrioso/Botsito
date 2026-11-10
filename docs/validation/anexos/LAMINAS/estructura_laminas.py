"""trabajo/laminas, F4.3: la estructura de las laminas de una carpeta de salida de `motor laminas`,
por sesion. Lee SOLO los HTML (nunca clave.txt) y solo imprime recuentos: cuantas laminas hay de
tipo a (una orden del bot que se lleno: «Coloca la orden» o «Mueve la orden») y de tipo b (el resto),
cuantas llevan cada marca, y si alguna marca pasa del borde derecho del corte.

Uso: uv run python estructura_laminas.py <carpeta de salida>"""

import re
import sys
from pathlib import Path

DERECHA = 1600 - 110  # el borde del corte: ANCHO - MARGEN_DER de engine/laminas_svg.py
MARCAS = ("h4-fija", "h4-saltada", "linea-m15", "toma", "caja", "nivel", "punto", "zona-control",
          "orden", "stop", "objetivo")  # fmt: skip

raiz = Path(sys.argv[1])
total = {"a": 0, "b": 0}
fuera_del_borde = 0
for sesion in sorted(p for p in raiz.iterdir() if p.is_dir()):
    tipos = {"a": 0, "b": 0}
    con = dict.fromkeys(MARCAS, 0)
    for lamina in sorted(sesion.glob("lamina-*.html")):
        texto = lamina.read_text(encoding="utf-8")
        tipo = "a" if re.search(r"<li>(Coloca|Mueve) la orden", texto) else "b"
        tipos[tipo] += 1
        for marca in MARCAS:
            con[marca] += bool(re.search(rf'class="{marca}[ "]', texto))
        for etiqueta in re.findall(r"<(?:line|rect|circle|text)\b[^>]*>", texto):
            if 'class="precio"' in etiqueta or 'width="1600"' in etiqueta:
                continue
            xs = [float(x) for x in re.findall(r'\s(?:x|x1|x2|cx)="([\d.]+)"', etiqueta)]
            ancho = re.search(r'\swidth="([\d.]+)"', etiqueta)
            if ancho and etiqueta.startswith("<rect"):
                xs.append(xs[0] + float(ancho.group(1)))
            fuera_del_borde += any(x > DERECHA + 0.05 for x in xs)
    total["a"] += tipos["a"]
    total["b"] += tipos["b"]
    print(f"{sesion.name}: {tipos['a'] + tipos['b']} laminas, {tipos['a']} de tipo a y "
          f"{tipos['b']} de tipo b; con cada marca: {con}")  # fmt: skip
print(f"total: {total['a']} de tipo a y {total['b']} de tipo b; marcas a la derecha del corte: "
      f"{fuera_del_borde}")  # fmt: skip
