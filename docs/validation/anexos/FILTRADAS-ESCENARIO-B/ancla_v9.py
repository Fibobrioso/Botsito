"""Tercera respuesta del consultor, punto 1, SOLO CON MARCAS: el bloque que completa el tramo de v9
0:34:44-0:34:56 y la linea que le sigue, en la filtrada ANTES de v9 y en la A. No imprime texto: de
cada linea, solo su clase (BLOQUE, VISIBLE, «…», SECCION, vacia) y su marca.

- (a) el bloque `[CUARENTENA 34:44–34:56]` existe y termina en la marca 34:56;
- (b) la linea siguiente del fichero es VISIBLE, lleva la marca 34:56 y esta en la misma seccion
  (la filtrada va agrupada por pregunta: solo dentro de una seccion y sin «…» entre medias la linea
  siguiente del fichero es el segmento siguiente de la cruda);
- (c) lo que las marcas pueden decir del ancla de ev-v9-003456-9ef48fb5 (t0 0:34:56, t1 0:35:00):
  que lineas y bloques hay en su ventana de localizacion, con la tolerancia de 2 s de
  `TOLERANCIA_CITA_MS` (0:34:54-0:35:02).

Uso: uv run python docs/validation/anexos/FILTRADAS-ESCENARIO-B/ancla_v9.py
"""

from __future__ import annotations

import re
from pathlib import Path

D = Path(r"C:\Users\USER\Desktop\sesion-03-audio")
FICHEROS = {"ANTES": D / "sesion-03.filtrada-ANTES-condicion.md", "A": D / "sesion-03.filtrada.md"}
_BLOQUE = re.compile(r"^\[CUARENTENA (\d+):(\d\d)–(\d+):(\d\d)\]$")
_MARCA = re.compile(r"^\[(\d+):(\d\d)\] ")
VENTANA = (34 * 60 + 54, 35 * 60 + 2)  # segundos: [t0 - 2 s, t1 + 2 s] del item


def clase(linea: str) -> tuple[str, str]:
    """(clase, marca) de una linea, sin su texto."""
    if m := _BLOQUE.match(linea):
        return "BLOQUE", f"{m.group(1)}:{m.group(2)}–{m.group(3)}:{m.group(4)}"
    if m := _MARCA.match(linea):
        return "VISIBLE", f"{m.group(1)}:{m.group(2)}"
    if linea == "…":
        return "…", ""
    if linea.startswith("## "):
        return "SECCION", ""
    if not linea.strip():
        return "vacia", ""
    return "otra", ""


def segundos(marca: str) -> int:
    m, s = marca.split(":")
    return int(m) * 60 + int(s)


def main() -> None:
    for nombre, ruta in FICHEROS.items():
        lineas = ruta.read_text(encoding="utf-8").splitlines()
        print(f"== {nombre}")
        donde = [i for i, ln in enumerate(lineas) if clase(ln) == ("BLOQUE", "34:44–34:56")]
        print(f"(a) bloques [CUARENTENA 34:44–34:56]: {len(donde)}")
        for i in donde:
            print(f"    linea {i + 1}: BLOQUE 34:44–34:56")
            for k in range(i + 1, min(i + 4, len(lineas))):
                c, mm = clase(lineas[k])
                print(f"    linea {k + 1}: {c} {mm}".rstrip())
        print("(c) en la ventana 34:54-35:02 (por marca de inicio; bloques por solape):")
        seccion = 0
        for i, ln in enumerate(lineas):
            c, mm = clase(ln)
            if c == "SECCION":
                seccion += 1
            if c == "VISIBLE" and VENTANA[0] <= segundos(mm) <= VENTANA[1]:
                print(f"    linea {i + 1} (seccion {seccion}): VISIBLE {mm}")
            if c == "BLOQUE":
                a, b = (segundos(x) for x in mm.split("–"))
                if a <= VENTANA[1] and b >= VENTANA[0]:
                    print(f"    linea {i + 1} (seccion {seccion}): BLOQUE {mm}")


if __name__ == "__main__":
    main()
